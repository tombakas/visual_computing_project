VIRTUALENV = venv
BIN = $(VIRTUALENV)/bin
PIP = $(BIN)/pip
FLASK = $(BIN)/flask

.PHONY: api
api: $(FLASK)
	FLASK_ENV=dvelopment FLASK_APP=backend $(FLASK) run

$(FLASK): $(VIRTUALENV)
	$(PIP) install -r backend/requirements.txt

$(VIRTUALENV):
	virtualenv --python=python3 venv

serve:
	cd frontend && yarn serve

build:
	cd frontend && yarn build
