# Library API

API REST de gestion de bibliothèque, en Python avec FastAPI et SQLite.

## Fonctionnalités

| Méthode | Route | Description | Codes |
|---|---|---|---|
| POST | `/books` | Ajouter un livre | 201, 422 |
| GET | `/books` | Lister les livres | 200 |
| GET | `/books/{id}` | Détail d'un livre | 200, 404 |
| GET | `/health` | État de l'API | 200 |

Un livre a trois champs : `title` (texte non vide), `author` (texte non vide), `year` (entier entre 0 et 2100). L'`id` est généré par la base.

## Lancer en local

Prérequis : Python 3.13.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

L'API est disponible sur http://127.0.0.1:8000. La base SQLite (`library.db`) est créée automatiquement au premier lancement.

## Lancer avec Docker

Prérequis : Docker.

Avec l'image publiée sur Docker Hub :

```powershell
docker run -p 8000:8000 -v library-data:/data zeriix3/library-api:latest
```

Ou en construisant l'image soi-même, à partir du repo GitHub :

```powershell
docker build -t library-api .
docker run -p 8000:8000 -v library-data:/data library-api
```

Le volume `library-data` conserve la base SQLite entre deux lancements du container.

## Utiliser l'API

Le plus simple : ouvrir la documentation interactive Swagger sur http://127.0.0.1:8000/docs, choisir une route, cliquer sur **Try it out** puis **Execute**.

Exemple de corps pour `POST /books` :

```json
{
  "title": "Dune",
  "author": "Frank Herbert",
  "year": 1965
}
```

Réponse attendue : `201` avec le livre et son `id`. Un titre vide renvoie `422` (validation).

En ligne de commande (PowerShell, `curl.exe` et non `curl`, qui est un alias de `Invoke-WebRequest`) :

```powershell
curl.exe -i http://127.0.0.1:8000/health
curl.exe http://127.0.0.1:8000/books
curl.exe -i http://127.0.0.1:8000/books/999
```

## Tests

```powershell
python -m pytest
```

Les tests utilisent une base temporaire (`test.db`) et ne touchent pas à la vraie base.

## CI/CD

GitHub Actions : les tests tournent sur chaque Pull Request vers `main`. Après un merge sur `main`, l'image Docker est construite et publiée sur Docker Hub (`zeriix3/library-api`).