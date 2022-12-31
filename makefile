# ex Makefile
.PHONY: install format lint test sec

install:
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt
format:
	@blue .
	@isort .
lint:
	@blue . --check
	@isort . --check
	@prospector
test:
	@pytest -v
sec:
	@pip-audit