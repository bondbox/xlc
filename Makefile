MAKEFLAGS += --always-make

VERSION := $(shell python3 -c "from xlc.attribute import __version__; print(__version__)")

all: build reinstall test


release: all
	git tag -a v${VERSION} -m "release v${VERSION}"
	git push origin --tags


clean-cover:
	rm -rf cover .coverage coverage.xml htmlcov
clean-tox:
	rm -rf .stestr .tox
clean: build-clean test-clean clean-cover clean-tox
	make -C xlc-tools clean


upload:
	xpip-upload --config-file .pypirc dist/*
	make -C xlc-tools upload


build-clean:
	xpip-build --debug setup --clean
build-requirements:
	pip3 install -r requirements.txt
build: build-clean build-requirements
	xpip-build --debug setup --all


install:
	pip3 install --force-reinstall --no-deps dist/*.whl
uninstall:
	pip3 uninstall -y xlc
reinstall: uninstall install


test-prepare:
	pip3 install --upgrade mock pylint flake8 pytest pytest-cov
pylint:
	pylint $(shell git ls-files xlc/*.py)
flake8:
	flake8 xlc --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 xlc --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest:
	pytest --cov=xlc --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100
pytest-clean:
	rm -rf .pytest_cache
test: test-prepare pylint flake8 pytest
test-clean: pytest-clean
