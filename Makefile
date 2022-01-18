# .PHONY: prepare_venv setup build test

# VENV_NAME?=venv
# PYTHON=${VENV_NAME}/bin/python

# prepare_venv: $(VENV_NAME)/bin/activate


# $(VENV_NAME): requirements.txt
# 	python3 -m venv $(VENV_NAME)
# 	./$(VENV_NAME)/bin/pip install -r requirements.txt

# setup: $(VENV_NAME)/bin/activate
# 	export PYTHONPATH=.
# 	. ./venv/bin/activate

# # run tests
# test: setup
# 	python -m pytest tests

# clean:
# 	rm -rf __pycache__
# 	rm -rf venv


# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(VENV)/bin

# make it work on windows too
ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
endif

$(VENV): requirements.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt

test: $(VENV)
# export PYTHONPATH=.
	$(BIN)/python -m unittest discover

# .PHONY: lint
# lint: $(VENV)
#     $(BIN)/flake8

# .PHONY: release
# release: $(VENV)
#     $(BIN)/python setup.py sdist bdist_wheel upload


clean:
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	rm -rf tests/.pytest_cache

.PHONY: clean test 
