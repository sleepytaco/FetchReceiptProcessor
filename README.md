# Fetch Receipt Processor

This project contains code for the [Receipt Processor challenge](https://github.com/fetch-rewards/receipt-processor-challenge) for Fetch Rewards.

## Overview

I set up a Flask API to handle two endpoints: one to process receipts (`/receipts/process`) and one to view a receipt's points (`/receipts/<id>/points`). To simplify the receipt processing to compute points, I use the `pydantic` library to convert the receipt JSON payload into a Pythonic object. The code for this can be found in `reciept.py` (which also contains a function to compute receipt points).

## Running the Code

I have dockerized my code. Please ensure to have Docker installed and open before running the commands below.

Run the following command in your terminal to build the docker container:

```shell
docker build -t receipt-api .
```

Once the container is built, run the following to boot up the web service:

```shell
docker run --rm -p 8888:8888 receipt-api
```

The Flask API should now be served on host `0.0.0.0` and port `8888`. You can quickly confirm this by visiting `0.0.0.0:8888` to receive a JSON response with a welcome message.

## Example Run

I used curl to test the API functionality.

First, I send a POST request with a receipt JSON payload to `0.0.0.0:8888/receipts/process`. The `/receipts/process` endpoint will process the receipt, compute the receipt ID and points, store the points in memory, and return a response with the receipt ID.

```shell
> curl -X POST http://0.0.0.0:8888/receipts/process -H "Content-Type: application/json" -d '{
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
      {
        "shortDescription": "Gatorade",
        "price": "2.25"
      },{
        "shortDescription": "Gatorade",
        "price": "2.25"
      },{
        "shortDescription": "Gatorade",
        "price": "2.25"
      },{
        "shortDescription": "Gatorade",
        "price": "2.25"
      }
    ],
    "total": "9.00"
  }'


{"id":"0d3335a2-7fce-4497-8b53-f0974815d0f7"}
```

The curl command returns a response of the form `{"id": "<hash>"}`. Then, I send a GET request with the received receipt ID `0d3335a2-7fce-4497-8b53-f0974815d0f7` to `0.0.0.0:8888/receipts/0d3335a2-7fce-4497-8b53-f0974815d0f7/points`. The `/receipts/<id>/points` endpoint returns a response containing the points given to the receipt with id `<id>`.

```shell
> curl -X GET http://0.0.0.0:8888/receipts/0d3335a2-7fce-4497-8b53-f0974815d0f7/points


{"points":109}
```

