import json
from user import User
from admin import Admin
from product import Product
from financial import FinancialTransaction
def load_users(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            users = {}
            for user_data in users_data:
                if user_data['role'] == 'admin':
                    users[user_data['login']] = Admin.from_dict(user_data)
                else:
                    users[user_data['login']] = User.from_dict(user_data)
            return users
    except FileNotFoundError:
        return {}

def save_users(filename, users):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([user.to_dict() for user in users.values()], f, ensure_ascii=False, indent=4)

def load_products(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
            return [Product.from_dict(product) for product in products_data]
    except FileNotFoundError:
        return []

def save_products(filename, products):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([product.to_dict() for product in products], f, ensure_ascii=False, indent=4)


def load_financial_transactions(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [FinancialTransaction.from_dict(item) for item in data['transactions']], data['balance']
    except FileNotFoundError:
        return [], 0.0  # Jeśli plik nie istnieje, zaczynamy z pustą listą transakcji i zerowym saldem

def save_financial_transactions(filename, transactions, balance):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'transactions': [transaction.to_dict() for transaction in transactions],
            'balance': balance
        }, f, ensure_ascii=False, indent=4)