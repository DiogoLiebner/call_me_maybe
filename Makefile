VENV:= venv
PYTHON:= $(venv)/bin/python3
PIP:= $(venv)/bin/pip

$(VENV):
		python3 -m venv $(VENV)
		$(VENV)/bin/pip install -e
		$(VENV)/bin/pip install flake8 mypy numpy pydantic uv


install: $(VENV)


clean:
	rm -f $(OUTPUT_NAME)
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true


lint:
	python3 -m flake8 a_maze_ing.py mazegen
	python3 -m mypy a_maze_ing.py mazegen --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 a_maze_ing.py mazegen
	python3 -m mypy a_maze_ing.py mazegen --strict


.PHONY: all install run debug clean lint lint-strict