

# web app commands

install-web:
	python -m install virtualenv; \
	virtualenv web-env; \
	pip install -r web/requirements.txt

run-web-server:
	source web-env/bin/activate ;\
	uvicorn web.main:app --reload

web-unit-test:
	source test-env/bin/activate ;\
	export PYTHONPATH=$$PWD ;\
	pytest tests/web


# cli commands

install-cli:
	python -m install virtualenv; \
	virtualenv cli-env; \
	pip install -r cli/requirements.txt

run-cli:
	source cli-env/bin/activate ;\
	export PYTHONPATH=$$PWD ;\
	python cli/quote.py

run-cli-params:
	source cli-env/bin/activate ;\
	export PYTHONPATH=$$PWD ;\
	python cli/quote.py --category sane --grayscale --output- my_quote.txt --output-image my_image.jpg

cli-unit-test:
	source test-env/bin/activate ;\
	export PYTHONPATH=$$PWD ;\
	pytest tests/cli


# run all tests for cli and web

install-unit-test:
	python -m install virtualenv; \
	virtualenv test-env; \
	pip install -r tests/requirements.txt

unit-test:
	source test-env/bin/activate ;\
	export PYTHONPATH=$$PWD ;\
	pytest tests/
