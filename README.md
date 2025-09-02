```markdown
# 🚀 Fast-Checker

**Fast-Checker** est une API construite avec **FastAPI** qui permet de :  

- Pinger des services **locaux ou externes** (une seule fois ou en boucle).  
- Gérer une liste d’URLs (ajout, mise à jour, suppression).  
- Planifier des pings via un **scheduler activable/désactivable**, qui exécute des pings automatiques toutes les **10 secondes**.  

👉 La base de données utilisée est **SQLite** pour la simplicité et le côté pratique (aucune configuration supplémentaire nécessaire).  

---

## 📂 Structure du projet

.
├── database.py        # Configuration de la base de données SQLite
├── models.py          # Modèles SQLAlchemy
├── schemas.py         # Schémas Pydantic pour la validation
├── main.py            # Entrée principale de l’application FastAPI
├── scripts/           # Scripts internes
│   ├── fixture.py     # Chargement de données initiales
│   ├── pinger.py      # Fonction principale de ping
│   └── pingScheduler.py # Gestion du scheduler automatique
├── fast-checker.db    # Base SQLite locale
├── requirements.txt   # Dépendances Python
├── Dockerfile         # Build de l’image Docker
└── README.md          # Documentation

````

## ⚡ Installation & Lancement

### 1. Lancer en local (avec venv)
```bash
# Créer un environnement virtuel
python -m venv env
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000 

ou 

fastapi dev main.py
````

👉 L’API sera dispo sur : [http://localhost:8000](http://localhost:8000)
👉 La doc Swagger auto-générée : [http://localhost:8000/docs](http://localhost:8000/docs)

ℹ️ **SQLite est utilisé par défaut** : la base est stockée dans le fichier `fast-checker.db`.
Cela rend l’utilisation très simple sans besoin d’installer ou configurer un serveur de base de données.

---

### 2. Lancer avec Docker

```bash
# Build de l’image
docker build -t checker .

# Lancer le conteneur
docker run -d --name checkerContainer -p 80:80 checker
```

👉 L’API sera dispo sur : [http://127.0.0.1](http://127.0.0.1)

👉 La doc sera dispo sur : [http://127.0.0.1/docs](http://127.0.0.1/docs)

---

## 🔌 Endpoints principaux

### 🌍 Gestion des URLs

* **POST** `/url` → Ajouter une URL
* **GET** `/urls` → Lister toutes les URLs
* **PUT** `/url/{id}` → Modifier une URL
* **DELETE** `/url/{id}` → Supprimer une URL

### 📡 Pings

* **GET** `/ping-url/{id}` → Pinger une URL enregistrée par son ID
* **POST** `/ping-url` → Pinger une URL donnée (sans l’enregistrer)
* **GET** `/pings` → Lister tous les pings réalisés

### ⏱️ Scheduler

* **POST** `/schedule` → Ajouter une URL au scheduler
* **GET** `/schedule/urls` → Lister toutes les URLs avec leurs schedules
* **PATCH** `/auto-schedule` → Activer/Désactiver le scheduler (ping auto toutes les 10s)
* **DELETE** `/schedule/{id}` → Supprimer une tâche planifiée

---

## 🛠 Exemple d’utilisation (via Swagger ou `curl`)

### Ajouter une URL

```bash
curl -X POST "http://localhost/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "name": "Example"}'
```

### Pinger une URL donnée

```bash
curl -X POST "http://localhost/ping-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```

### Activer le scheduler

```bash
curl -X PATCH "http://localhost/auto-schedule"
```

---

## 📖 Notes

* Base de données : **SQLite** → fichier `fast-checker.db`.
* Scheduler : ping automatique toutes les **10 secondes** des URLs enregistrées.
* Documentation interactive : [Swagger UI](http://localhost:8000/docs).

---
