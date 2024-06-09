from flask import Flask, request, jsonify
from receipt import Receipt, calculate_points
import uuid

app = Flask(__name__)
receipt_points_db = {}  # This acts as the in-memory db


@app.route('/', methods=['POST', 'GET'])
def home():
    return jsonify({"message": "Welcome to the Receipt Processor API! You can POST your receipt data to the "
                               "/receipts/process endpoint which will compute and store the points for that receipt. "
                               "You can use the receipt ID returned by the process endpoint in a GET request to the "
                               "/receipts/<id>/points endpoint to view the points given to the receipt."})


# Endpoint to process receipt
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    # Get JSON payload from the request and convert it into a Receipt object
    receipt_json = request.json
    try:
        receipt = Receipt(**receipt_json)
    except Exception as e:
        print(e)
        res = jsonify({"error": "Error validating the receipt payload."})
        res.status = 500
        return res

    # Generate a unique id for the receipt
    receipt_id = str(uuid.uuid4())

    # Compute points for this receipt and store it in-memory
    receipt_points_db[receipt_id] = {"receipt": receipt, "points": calculate_points(receipt)}

    # Return a JSON response containing the receipt id
    return jsonify({"id": receipt_id})  # Defaults to status 200 response


# Endpoint to return points for a receipt
@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    if id not in receipt_points_db:
        res = jsonify({"error": f"Receipt ID {id} not found in the database."})
        res.status = 404
        return res

    return jsonify({"points": receipt_points_db[id]["points"]})  # Defaults to status 200 response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)
