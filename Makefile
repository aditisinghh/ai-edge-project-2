PY ?= python3

.PHONY: setup data test app eval

setup:
	$(PY) -m pip install -r requirements.txt

# Rebuild data/ from the Project 1 repo (only needed if Project 1 outputs change)
data:
	$(PY) scripts/build_knowledge_base.py --p1 ../datacenter-siting

test:
	$(PY) -m pytest -q tests

app:
	streamlit run app.py

eval:
	$(PY) eval/run_eval.py
