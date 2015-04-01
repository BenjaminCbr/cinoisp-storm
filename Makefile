VENV_VERSION=12.0.7

VENV_ACTIVATE=. ./psi_venv/bin/activate &&

venv_install:
	bin/virtenv.sh $(VENV_VERSION)

venv_update:
	$(VENV_ACTIVATE) pip install -r requirements.txt
