from flask import Blueprint, request, jsonify,Flask
from models import Wallet, Transaction
from datetime import datetime
from functools import wraps
wallet_bp = Blueprint('wallet', __name__, url_prefix='/wallet')
app=Flask(__name__)

KEY='OTESTkey'
def api_key_required(api_key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            provided_key = request.headers.get('API-Key')

            if not provided_key or provided_key != api_key:
                return jsonify({'error': 'Unauthorized'}), 401

            return func(*args, **kwargs)

        return wrapper
    return decorator
@wallet_bp.route('/create', methods=['POST'])
def create_wallet():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    try:
        wallet = Wallet.create(username=username)
        return jsonify({'message': 'Wallet created successfully', 'wallet_id': wallet.id}), 201
    except :
        return jsonify({'error': 'Username already exists'}), 400

@wallet_bp.route('/add_credit/<int:wallet_id>', methods=['POST'])
@api_key_required(KEY)
def add_credit(wallet_id):
    data = request.json
    amount = data.get('amount')
    description = data.get('description')
    if not amount or not description:
        return jsonify({'error': 'Amount and description are required'}), 400
    
    try:
        wallet = Wallet.get_by_id(int(wallet_id))
        wallet.balance += amount
        wallet.save()
        Transaction.create(wallet=wallet, description=description, amount=amount, timestamp=datetime.now())
        return jsonify({'message': 'Credit added successfully'}), 200
    except Wallet.DoesNotExist:
        return jsonify({'error': 'Wallet not found'}), 404

@wallet_bp.route('/decrease_credit/<int:wallet_id>', methods=['POST'])
@api_key_required(KEY)
def decrease_credit(wallet_id):
    data = request.json
    amount = data.get('amount')
    description = data.get('description')
    if not amount or not description:
        return jsonify({'error': 'Amount and description are required'}), 400
    
    try:
        wallet = Wallet.get_by_id(int(wallet_id))
        if wallet.balance < amount:
            return jsonify({'error': 'Insufficient funds'}), 400
        wallet.balance -= amount
        wallet.save()
        Transaction.create(wallet=wallet, description=description, amount=-amount, timestamp=datetime.now())
        return jsonify({'message': 'Credit decreased successfully'}), 200
    except Wallet.DoesNotExist:
        return jsonify({'error': 'Wallet not found'}), 404
@wallet_bp.route('/balance/<int:wallet_id>', methods=['GET'])
def get_balance(wallet_id):
    try:
        wallet = Wallet.get_by_id(int(wallet_id))
        return jsonify({'balance': wallet.balance}), 200
    except Wallet.DoesNotExist:
        return jsonify({'error': 'Wallet not found'}), 404
app.register_blueprint(wallet_bp)
if __name__=="__main__":
    app.run()