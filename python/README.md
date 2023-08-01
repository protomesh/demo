# Build Lambda Zip

```bash
rm -rf dist package
poetry install --only main --sync
poetry build
poetry run pip install --upgrade -t package dist/*.whl
cd package; mkdir -p out; zip -r -q out/lambda.zip . -x '*.pyc'
```

```bash
poetry install --only main --sync
mkdir -p dist/lambda-package
cp --recursive .venv/lib/python*/site-packages/* dist/lambda-package/
cp --recursive petstore/ dist/lambda-package/
cd dist/lambda-package
zip -r ../lambda.zip ./
```