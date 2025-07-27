
## instalacion docker mediante terminal


````bash
docker pull localstack/localstack
docker run -d --name localstackdev -p 4566:4566 -p 4571:4571 -v localstack-data:/var/lib/localstack -v /var/run/docker.sock:/var/run/docker.sock  localstack/localstack
````

