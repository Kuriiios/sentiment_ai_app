#### Installation des bibliothèques
`pip install fastapi uvicorn loguru streamlit requests python-dotenv`

Un mini programme complet:
* **frontend** (streamlit)
  * **pages**
* **backend**:
  * **modules** (contenir nos propres modules)
  * **data** (nos csv)

#### Architecture
```
mon_projet/
├── API
│   ├── __init__.py
│   ├── logs
│   │   └── main.log
│   ├── modules
│   │   ├── __init__.py
│   │   └── db_tools.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── models.py
│   │   └── quotes_db.db
│   └── main.py
├── API_AI
│   ├── logs
│   │   └── sentiment_api.log
│   └── sentiment_api.py
├── APP
│   ├── app.py
│   └── pages
│       ├── 0_insérer.py
│       ├── 1_Afficher.py
│       └── 2_search.py
├── DEV
│   └── dev.ipynb
├── README.md
├── .env
├── .venv
└── .gitignore
```

#### Ma base de données "quotes_db.bd"
Colonnes:
- `id`
- `text`

#### Commande pour lancer le serveur uvicorn

`uvicorn chemin.nom:app --reload --log-level debug`

#### Commandes pour le terminale pour faire un GET

- `Powershell` : `Invoke-WebRequest -Method GET "http://127.0.0.1:8000/citation"`

- `MAC Linux` : `CURL -X GET "http://127.0.0.1:8000/citation"`

#### Commande pour streamlit

`streamlit run chemin.\nom.py`

#### Mes commandes

`python ./API/main.py`
`python ./API_IA/sentiment_api.py`
`streamlit run APP/app.py`

