# TP10 - Invocation d'Objets Distants en Python avec Pyro5

## Objectif

Ce TP a pour objectif de mettre en œuvre un service distant orienté objet en Python avec Pyro5.

Le service `DocumentService` est publié par un serveur, enregistré dans un Name Server, puis utilisé par un client à travers un proxy.

Le client peut donc appeler les méthodes d'un objet distant comme si cet objet était local.

---

## Fichiers du projet

```text
.
├── server_docs.py
├── client_docs.py
└── README.md
```

- `server_docs.py` : serveur qui expose l'objet distant `DocumentService`
- `client_docs.py` : client qui appelle les méthodes distantes
- `README.md` : description du projet

---

## Fonctionnement général

Le projet repose sur trois éléments principaux :

1. **Name Server** : annuaire qui permet de retrouver l'objet distant grâce à un nom logique.
2. **Serveur** : programme qui contient et expose l'objet distant `DocumentService`.
3. **Client** : programme qui récupère l'objet distant via un proxy et appelle ses méthodes.

Schéma simplifié :

```text
Client
  ↓
Proxy Pyro5
  ↓
Réseau local / localhost
  ↓
Serveur Pyro5
  ↓
DocumentService
```

---

## Méthodes exposées

Le service expose les méthodes suivantes :

- `list_documents(token)` : retourne la liste des documents disponibles.
- `get_document_content(doc_id, token)` : retourne le contenu d'un document.
- `get_document_metadata(doc_id, token)` : retourne les métadonnées d'un document.

---

## Sécurité

Le projet intègre plusieurs mesures de sécurité :

- validation des entrées côté serveur ;
- vérification d'un token d'accès ;
- refus des entrées invalides comme `../../etc` ou `doc;DROP` ;
- messages d'erreur génériques côté client ;
- journalisation des événements côté serveur ;
- non-exposition des méthodes internes ;
- absence d'utilisation de `pickle`.

Les méthodes internes comme `_check_token()`, `_validate_doc_id()` et `_reload_index()` ne sont pas destinées à être appelées directement par le client.

---

## Installation

Installer Pyro5 :

```bash
python -m pip install Pyro5
```

---

## Exécution

### 1. Lancer le Name Server

Dans un premier terminal :

```bash
python -m Pyro5.nameserver
```

### 2. Lancer le serveur

Dans un deuxième terminal :

```bash
python server_docs.py
```

### 3. Lancer le client

Dans un troisième terminal :

```bash
python client_docs.py
```

---

## Résultats attendus

Le client doit afficher des résultats similaires à ceux-ci :

```text
Service trouvé : bank.documents.service
URI : PYRO:obj_xxxxx@localhost:xxxxx

--- Liste des documents ---
Résultat : ['doc_001', 'doc_002', 'doc_003']

--- Lecture d'un document valide doc_001 ---
Résultat : Rapport annuel 2024 — données confidentielles

--- Métadonnées du document doc_002 ---
Résultat : {'doc_id': 'doc_002', 'length': 36, 'type': 'text'}

--- Document inexistant doc_999 ---
Erreur document : 'Document introuvable'

--- Tentative path traversal ../../etc ---
Erreur de validation : Identifiant invalide

--- Mauvais type : entier au lieu de str ---
Erreur de type : Paramètre invalide

--- Mauvais token ---
Erreur d'accès : Accès refusé
```

---

## Conclusion

Ce TP permet de comprendre le principe de l'invocation d'objets distants.

L'objet réel `DocumentService` est exécuté côté serveur, tandis que le client utilise un proxy local pour appeler ses méthodes à travers le réseau.

Le TP montre aussi l'importance de la sécurité dans les architectures distribuées : validation des entrées, contrôle d'accès, limitation des méthodes exposées et gestion propre des erreurs.

---

## Auteur

Yassine