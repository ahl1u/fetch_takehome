from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict, deque

app = Flask(__name__)

# stores transactions and payer balances
transactions = deque([])
balance = defaultdict(int)

# endpoint to add points for a specific payer
@app.route('/add', methods=['POST'])
def add_points():
    data = request.json

    payer = data['payer']
    points = data['points']
    timestamp_raw = data['timestamp']

    # convert timestamp to datetime format
    timestamp = datetime.fromisoformat(timestamp_raw.replace('Z', '+00:00'))

    # check if payer has enough points to deduct
    if points < 0 and balance[payer] + points < 0:
        return "not enough points to deduct", 400

    # record transaction and update balance
    transaction = (payer, points, timestamp)
    transactions.append(transaction)

    balance[payer] += points
    return "", 200

# endpoint to spend points, spending oldest points first
@app.route('/spend', methods=['POST'])
def spend_points():
    global transactions
    data = request.json

    points_spend = data['points']
    total_spend = defaultdict(int)

    # check if user has enough total points to spend
    if points_spend > sum(balance.values()):
        return "User doesn't have enough points", 400

    # sort transactions by timestamp to prioritize oldest points
    temp = sorted(transactions, key=lambda x: x[2])
    transactions = deque(temp)

    # spend points while ensuring no payer goes negative
    while transactions and points_spend > 0:
        recent = transactions.popleft()
        payer, points, time = recent

        # spend as much as possible from current transaction
        difference = min(points, points_spend)

        balance[payer] -= difference
        total_spend[payer] -= difference

        points_spend -= difference

        # re-add remaining points if not all spent
        if points > difference:
            transactions.appendleft((payer, points - difference, time))
    
    # prepare response with points spent per payer
    output = []
    for key,value in total_spend.items():
        output.append({"payer": key, "points" : value})
    
    return jsonify(output), 200

# endpoint to get the current balance per payer
@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify(balance), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)