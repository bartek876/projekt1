class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['price'], data['quantity'])

    def update_quantity(self, quantity):
        self.quantity = quantity

    def order(self, amount):
        """Zamówienie produktu - zwiększa ilość produktu."""
        self.quantity += amount

    def sell(self, amount):
        """Sprzedaż produktu - zmniejsza ilość produktu, jeśli ilość jest wystarczająca."""
        if self.quantity >= amount:
            self.quantity -= amount
            return True  # Pomyślna sprzedaż
        else:
            return False  # Niewystarczająca ilość produktu