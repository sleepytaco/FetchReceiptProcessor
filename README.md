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

You can now POST a receipt payload to `0.0.0.0:8888/receipts/process` which will process the receipt, compute the points, and return a response with the receipt ID. You can then send a GET request to `0.0.0.0:8888/receipts/<id>/points` with the received receipt ID to find out the points given to that receipt.
