import logging
import re

import Pyro5.api


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


_DOCUMENTS = {
    "doc_001": "Rapport annuel 2024 — données confidentielles",
    "doc_002": "Politique de sécurité — version 3.2",
    "doc_003": "Guide d'utilisation — accès public",
}


@Pyro5.api.expose
class DocumentService:
    """
    Service distant de gestion de documents.
    Les méthodes exposées peuvent être appelées par un client Pyro5.
    """

    _VALID_TOKEN = "secret-tp10-2024"

    def _check_token(self, token: str) -> None:
        """
        Méthode interne : vérifie le token.
        Elle n'est pas destinée à être appelée directement par le client.
        """
        if token != self._VALID_TOKEN:
            logger.warning("Tentative d'accès avec token invalide")
            raise PermissionError("Accès refusé")

    def _validate_doc_id(self, doc_id: str) -> None:
        """
        Valide strictement l'identifiant du document.
        Protection contre path traversal, injection et mauvais types.
        """
        if not isinstance(doc_id, str):
            logger.warning("Type invalide pour doc_id : %s", type(doc_id))
            raise TypeError("Paramètre invalide")

        if not 3 <= len(doc_id) <= 32:
            logger.warning("Longueur invalide pour doc_id : %r", doc_id)
            raise ValueError("Identifiant invalide")

        if not re.match(r"^[a-zA-Z0-9_]+$", doc_id):
            logger.warning("Format invalide pour doc_id : %r", doc_id)
            raise ValueError("Identifiant invalide")

        forbidden_values = ["..", "/", ";"]
        if any(value in doc_id for value in forbidden_values):
            logger.warning("Valeur interdite dans doc_id : %r", doc_id)
            raise ValueError("Identifiant invalide")

    def list_documents(self, token: str) -> list:
        """
        Retourne la liste des identifiants de documents disponibles.
        """
        self._check_token(token)
        logger.info("Appel distant : list_documents()")
        return list(_DOCUMENTS.keys())

    def get_document_content(self, doc_id: str, token: str) -> str:
        """
        Retourne le contenu d'un document après validation stricte.
        """
        self._check_token(token)
        self._validate_doc_id(doc_id)

        if doc_id not in _DOCUMENTS:
            logger.info("Document introuvable : %s", doc_id)
            raise KeyError("Document introuvable")

        logger.info("Document servi : %s", doc_id)
        return _DOCUMENTS[doc_id]

    def get_document_metadata(self, doc_id: str, token: str) -> dict:
        """
        Retourne des métadonnées simples sur un document.
        """
        self._check_token(token)
        self._validate_doc_id(doc_id)

        if doc_id not in _DOCUMENTS:
            logger.info("Métadonnées demandées pour document introuvable : %s", doc_id)
            raise KeyError("Document introuvable")

        content = _DOCUMENTS[doc_id]

        return {
            "doc_id": doc_id,
            "length": len(content),
            "type": "text",
        }

    def _reload_index(self) -> None:
        """
        Méthode interne non exposée volontairement.
        Elle représente une opération d'administration.
        """
        logger.info("Index rechargé")


def main() -> None:
    """
    Lance le serveur Pyro5 et publie DocumentService dans le Name Server.
    """
    with Pyro5.api.Daemon() as daemon:
        ns = Pyro5.api.locate_ns()

        uri = daemon.register(DocumentService)
        ns.register("bank.documents.service", uri)

        print("DocumentService prêt.")
        print(f"URI : {uri}")
        print("Nom logique : bank.documents.service")
        print("Serveur en attente d'appels... Ctrl+C pour arrêter.")

        daemon.requestLoop()


if __name__ == "__main__":
    main()