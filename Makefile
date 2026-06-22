.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python src/run_pipeline.py

test:
	pytest tests

clean:
	rm -f data/raw/fred_*.csv data/raw/gdelt_*.csv data/processed/*.csv reports/figures/*.png reports/maps/*.html
