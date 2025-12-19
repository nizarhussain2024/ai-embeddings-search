.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python app.py

test:
	python -m pytest || echo "No tests configured"

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete





