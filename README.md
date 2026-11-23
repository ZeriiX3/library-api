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

L'API est alors disponible sur http://127.0.0.1:8000, avec la documentation Swagger sur http://127.0.0.1:8000/docs.

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

Test rapide (PowerShell : `curl.exe`, pas `curl`) :

```powershell
curl.exe http://127.0.0.1:8000/health         # {"status":"ok"}
curl.exe http://127.0.0.1:8000/books          # [] (liste vide au départ)
curl.exe -i http://127.0.0.1:8000/books/999   # HTTP 404 + {"detail":"Book not found"}
```

## Tests

```powershell
python -m pytest
```

6 tests d'API (avec `TestClient`) :
- `/health` répond `200`
- ajout d'un livre : `201` avec un `id`
- titre vide : `422`
- liste des livres : `200`
- détail d'un livre : `200`
- id inexistant : `404`

Ils utilisent une base temporaire (`test.db`), recréée avant chaque test, et ne touchent pas à la vraie base.

## CI/CD

GitHub Actions : les tests tournent sur chaque Pull Request vers `main`. Après un merge sur `main`, l'image Docker est construite et publiée sur Docker Hub (`zeriix3/library-api`).