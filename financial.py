import json
from datetime import datetime

class FinancialTransaction:
    def __init__(self, operator, operation, amount, cost):
        self.operator = operator  # Kto wykonał operację
        self.operation = operation  # Typ operacji: "order", "sell", "balance_update"
        self.amount = amount  # Ilość produktów (lub w przypadku aktualizacji salda może być 0)
        self.cost = cost  # Koszt operacji (dodatni lub ujemny w przypadku modyfikacji salda)
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Data operacji

    def to_dict(self):
        return {
            'operator': self.operator,
            'operation': self.operation,
            'amount': self.amount,
            'cost': self.cost,
            'date': self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['operator'], data['operation'], data['amount'], data['cost'])
    