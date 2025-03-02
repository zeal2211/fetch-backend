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

 You can curl or use postman to interact with the API.

 ### Process a Receipt

`curl -H 'Content-Type: application/json' -d @samples/input1.json -X POST http://localhost:8000/receipts/process`

This will return a JSON reponse containing an id for the processed receipt. 

Example Response: {"id":"c8d1e276-ae28-4853-aa21-9de9cbf5d7ea"}

### Retrieve Points for a Receipt

`curl http://localhost:8000/receipts/<receipt_id>/points`

Replace <receipt_id> with the ID received from the previous request.

This will return the points associated with that receipt id.

Example Usage:

`curl http://localhost:8000/receipts/c8d1e276-ae28-4853-aa21-9de9cbf5d7ea/points`

Example Response:
{"points": 28}

## Test Cases

If you want to run the test cases, you will need to install python and in a different terminal put the following commands:

```
pip install requirements.txt
python manage.py test
```

Expected Response:

Found 2 test(s).

Creating test database for alias 'default'...

System check identified no issues (0 silenced).

..

----------------------------------------------------------------------

Ran 2 tests in 0.022s

OK




