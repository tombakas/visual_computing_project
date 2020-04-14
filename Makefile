DB_URL = 'https://docs.google.com/uc?export=download&id=16AX0srj2p-UIPpN3pF2BdtBVna4oSANi'

VIRTUALENV = venv
BIN = $(VIRTUALENV)/bin
PIP = $(BIN)/pip
FLASK = $(BIN)/flask

.PHONY: api
api: $(FLASK) db/database.db
	FLASK_ENV=development FLASK_APP=backend $(FLASK) run

$(FLASK): $(VIRTUALENV)
	$(PIP) install -r backend/requirements.txt

$(VIRTUALENV):
	virtualenv --python=python3 venv

serve: frontend/node_modules
	cd frontend && yarn serve

build:
	cd frontend && yarn build

frontend/node_modules:
	cd frontend && yarn install

db/database.db: db
	wget -O db/database.db $(DB_URL)

db:
	mkdir -p db
