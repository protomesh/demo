#!/bin/bash

rm -rf dist
poetry install --only main --sync
mkdir -p dist/lambda-package
cp --recursive .venv/lib/python*/site-packages/* dist/lambda-package/
cp --recursive petstore/ dist/lambda-package/
cd dist/lambda-package || exit
zip -r ../lambda.zip ./