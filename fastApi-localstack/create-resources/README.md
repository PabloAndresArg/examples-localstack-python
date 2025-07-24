# Comandos para crear recursos desde la terminal

````bash
source /Users/pargueta/Desktop/PRUEBAS/.venv/bin/activate
pip install awscli-local
brew install watch
````

## crear un S3 y listar

````bash
awslocal s3 mb s3://user-files
awslocal --endpoint-url=http://localhost:4566 s3 ls
awslocal --endpoint-url=http://localhost:4566 s3 ls user-files
````

