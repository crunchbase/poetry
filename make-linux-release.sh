#!/bin/bash
PYTHON_VERSIONS="cp27-cp27m cp34-cp34m cp35-cp35m cp36-cp36m cp37-cp37m cp38-cp38"

cd /io
/opt/python/cp37-cp37m/bin/pip install pip -U
/opt/python/cp37-cp37m/bin/pip install poetry -U --pre
/opt/python/cp37-cp37m/bin/poetry config virtualenvs.create false
/opt/python/cp37-cp37m/bin/poetry install --no-dev
/opt/python/cp37-cp37m/bin/python sonnet make release --ansi \
    -P "3.6:/opt/python/cp36-cp36m/bin/python"
cd -
