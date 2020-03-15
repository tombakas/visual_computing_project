VIRTUALENV = venv
BIN = $(VIRTUALENV)/bin
PIP = $(BIN)/pip
FLASK = $(BIN)/flask

.PHONY: api
api: $(FLASK)
	FLASK_ENVIRONMENT=development FLASK_APP=backend venv/bin/flask run

$(FLASK): $(VIRTUALENV)
	$(PIP) install -r backend/requirements.txt

$(VIRTUALENV):
	virtualenv --python=python3 venv

serve:
	cd frontend && yarn serve

build:
	cd frontend && yarn build
