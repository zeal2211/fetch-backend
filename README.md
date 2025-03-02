# Receipt Processor
This project provides a Django-based receipt processing API, containerized using Docker. Follow the instructions below to setup and run the service.

## Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/products/docker-desktop/)

## Setup Instructions

1. Clone the repository
```
git clone https://github.com/zeal2211/fetch-backend.git
cd fetch-backend
```

2. Start Docker

Ensure docker is running on your machine before proceeding.

3. Build and run the Docker Container
```
docker build -t django-app .
docker run -p 8000:8000 django-app
```

 ## API Usage

 You can curl or postman to interact with the API.

 ### Process a Receipt

`curl -H 'Content-Type: application/json' -d @input.json -X POST http://localhost:8000/receipts/process`

This will return a JSON reponse containing an id for the processed receipt.

### Retrieve Points for a Receipt

`curl http://localhost:8000/receipts/<receipt_id>/points`

Replace <receipt_id> with the ID received from the previous request.

