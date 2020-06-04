test:
	PYTHONPATH=src/ pytest  tests/
	PYTHONPATH=src/ pytest --capture=sys tests/unit/t_quest2pdf.py

clean:
	find . -name '*.pyc' -execdir rm -f {} +
	find . -type d -name '__pycache__' -execdir rm -rf {} +
	find . -name '*.log' -execdir rm -f {} +

black:
	black src/
	black tests/unit/

build:
	python3 setup.py sdist bdist_wheel

.PHONY: test clean black build
