PY = python3
VENV = venv
BIN=$(VENV)/bin

$(VENV): requirements.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt

test: $(VENV)
	$(BIN)/python -m unittest discover

stage1: $(VENV)
	$(BIN)/python vesting_program/main.py data/example1.csv 2020-04-01

stage2: $(VENV)
	$(BIN)/python vesting_program/main.py data/example2.csv 2021-01-01

stage3: $(VENV)
	$(BIN)/python vesting_program/main.py data/example3.csv 2021-01-01 1

clean:
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	rm -rf tests/.pytest_cache

.PHONY: clean test stage1 stage2 stage3
