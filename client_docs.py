import Pyro5.api


SERVICE_NAME = "bank.documents.service"
TOKEN = "secret-tp10-2024"


def call_safely(description: str, function, *args):
    """
    Exécute un appel distant et affiche proprement le résultat ou l'erreur.
    """
    print(f"\n--- {description} ---")

    try:
        result = function(*args)
        print("Résultat :", result)

    except PermissionError as error:
        print("Erreur d'accès :", error)

    except TypeError as error:
        print("Erreur de type :", error)

    except ValueError as error:
        print("Erreur de validation :", error)

    except KeyError as error:
        print("Erreur document :", error)

    except Exception:
        print("Erreur de service. Contactez l'administrateur.")


def main() -> None:
    """
    Client Pyro5 qui récupère le service distant et appelle ses méthodes.
    """
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup(SERVICE_NAME)

    print("Service trouvé :", SERVICE_NAME)
    print("URI :", uri)

    with Pyro5.api.Proxy(uri) as document_service:
        document_service._pyroTimeout = 5

        call_safely(
            "Liste des documents",
            document_service.list_documents,
            TOKEN
        )

        call_safely(
            "Lecture d'un document valide doc_001",
            document_service.get_document_content,
            "doc_001",
            TOKEN
        )

        call_safely(
            "Métadonnées du document doc_002",
            document_service.get_document_metadata,
            "doc_002",
            TOKEN
        )

        call_safely(
            "Document inexistant doc_999",
            document_service.get_document_content,
            "doc_999",
            TOKEN
        )

        call_safely(
            "Tentative path traversal ../../etc",
            document_service.get_document_content,
            "../../etc",
            TOKEN
        )

        call_safely(
            "Mauvais type : entier au lieu de str",
            document_service.get_document_content,
            12345,
            TOKEN
        )

        call_safely(
            "Mauvais token",
            document_service.get_document_content,
            "doc_001",
            "wrong-token"
        )


if __name__ == "__main__":
    main()