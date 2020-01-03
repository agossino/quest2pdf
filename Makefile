test:
	PYTHONPATH=src/quest2pdf pytest tests/

clean:
	find . -name '*.pyc' -execdir rm -f {} +
	find . -type d -name '__pycache__' -execdir rm -rf {} +
	find . -name '*.log' -execdir rm -f {} +

build:
	python3 setup.py sdist bdist_wheel

.PHONY: test clean build
