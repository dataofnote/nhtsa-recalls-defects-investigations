

fetch:
	python wrangle/scripts/fetch_data.py


compile:
	python wrangle/scripts/compile.py investigations
	python wrangle/scripts/compile.py recalls
	python wrangle/scripts/compile.py recalls_quarterly_reports
	python wrangle/scripts/compile.py technical_service_bulletins
	# python wrangle/scripts/compile.py complaints
