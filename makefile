# ex Makefile
.PHONY: install format lint test sec

install:
	@poetry install
format:
	@blue .
	@isort .
lint:
	@blue . --check
	@isort . --check
pep:
	@prospector
	@prospector --with-tool pep257
test:
	@pytest -v
sec:
	@pip-audit