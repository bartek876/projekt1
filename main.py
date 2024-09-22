from data_menager import load_users, save_users, load_products, save_products, load_financial_transactions, save_financial_transactions
from admin import Admin
from product import Product
from financial import FinancialTransaction
from raport import generate_report

def main():
    users = load_users('users.json')
    products = load_products('products.json')
    financial_transactions, balance = load_financial_transactions('financial.json')

    # Dodanie domyślnego admina, jeśli go nie ma
    if 'admin' not in users:
        users['admin'] = Admin('admin', 'adminadmin')

    save_users('users.json', users)

    print("Prosimy o podanie loginu i hasła")
    loget = False
    while not loget:
        login = input("Podaj login: ")
        password = input("Podaj hasło: ")
        if login in users and users[login].password == password:
            loget = True
            current_user = users[login]
        else:
            print("Błędny login lub hasło.")

    while loget:
        print("Jaką operację chcesz wykonać?")
        if isinstance(current_user, Admin):
            print("add - dodaj nowego użytkownika")
            print("change role - zmiana roli użytkownika")
            print("remove - usuń użytkownika")
            print("view balance - wyświetl saldo")
            print("update balance - zaktualizuj saldo")
        print("products - zarządzaj produktami")
        print("order - zamów produkt")
        print("sell - sprzedaj produkt")
        print("financials - wyświetl historię finansową")
        print("change password - zmiana hasła")
        print("raport - wygeneruj raport")
        print("logout - wyloguj się")
        choice = input().lower()

        if choice == "add" and isinstance(current_user, Admin):
            new_login = input("Podaj login: ")
            new_password = input("Podaj hasło: ")
            new_role = input("Podaj rolę: ")
            current_user.add_user(users, new_login, new_password, new_role)
            save_users('users.json', users)
        elif choice == "change role" and isinstance(current_user, Admin):
            target_login = input("Podaj login użytkownika: ")
            if target_login in users:
                new_role = input("Podaj nową rolę: ")
                current_user.change_user_role(users[target_login], new_role)
                save_users('users.json', users)
            else:
                print("Nie znaleziono użytkownika.")
        elif choice == "remove" and isinstance(current_user, Admin):
            target_login = input("Podaj login użytkownika do usunięcia: ")
            current_user.remove_user(users, target_login)
            save_users('users.json', users)
        elif choice == "view balance" and isinstance(current_user, Admin):
            print(f"Obecne saldo firmy: {balance:.2f} zł")
        elif choice == "update balance" and isinstance(current_user, Admin):
            try:
                update_amount = float(input("Podaj kwotę do zaktualizowania salda (+/-): "))
                balance += update_amount
                transaction = FinancialTransaction(current_user.login, 'balance_update', 0, update_amount)
                financial_transactions.append(transaction)
                save_financial_transactions('financial.json', financial_transactions, balance)
                print(f"Saldo zostało zaktualizowane o {update_amount:.2f} zł. Nowe saldo: {balance:.2f} zł.")
            except ValueError:
                print("Nieprawidłowa wartość, podaj liczbę.")
        elif choice == "products":
            print("Zarządzanie produktami:")
            print("list - wyświetl wszystkie produkty")
            print("add - dodaj nowy produkt")
            print("remove - usuń produkt")
            product_choice = input("Wybierz operację: ").lower()

            if product_choice == "list":
                for product in products:
                    print(f"Nazwa: {product.name}, Cena: {product.price}, Ilość: {product.quantity}")
            elif product_choice == "add" and isinstance(current_user, Admin):
                product_name = input("Podaj nazwę produktu: ")
                product_price = float(input("Podaj cenę produktu: "))
                product_quantity = int(input("Podaj ilość produktu: "))
                new_product = Product(product_name, product_price, product_quantity)
                products.append(new_product)
                save_products('products.json', products)
                print(f"Produkt {product_name} został dodany.")
            elif product_choice == "remove" and isinstance(current_user, Admin):
                product_name = input("Podaj nazwę produktu do usunięcia: ")
                product_found = False
                for product in products:
                    if product.name == product_name:
                        products.remove(product)
                        save_products('products.json', products)
                        print(f"Produkt {product_name} został usunięty.")
                        product_found = True
                        break
                if not product_found:
                    print(f"Produkt {product_name} nie został znaleziony.")
        elif choice == "order":
            product_name = input("Podaj nazwę produktu, który chcesz zamówić: ")
            order_quantity = int(input("Podaj ilość, którą chcesz zamówić: "))
            product_found = False
            for product in products:
                if product.name == product_name:
                    product.order(order_quantity)
                    cost = product.price * order_quantity
                    transaction = FinancialTransaction(current_user.login, 'order', order_quantity, cost)
                    financial_transactions.append(transaction)
                    balance -= cost  # Aktualizacja salda po zamówieniu
                    save_products('products.json', products)
                    save_financial_transactions('financial.json', financial_transactions, balance)
                    print(f"Zamówiono {order_quantity} sztuk {product_name} za {cost:.2f} zł. Nowe saldo: {balance:.2f} zł.")
                    product_found = True
                    break
            if not product_found:
                print(f"Produkt {product_name} nie został znaleziony.")
        elif choice == "sell":
            product_name = input("Podaj nazwę produktu, który chcesz sprzedać: ")
            sell_quantity = int(input("Podaj ilość, którą chcesz sprzedać: "))
            product_found = False
            for product in products:
                if product.name == product_name:
                    if product.sell(sell_quantity):
                        cost = product.price * sell_quantity
                        transaction = FinancialTransaction(current_user.login, 'sell', sell_quantity, cost)
                        financial_transactions.append(transaction)
                        balance += cost  # Aktualizacja salda po sprzedaży
                        save_products('products.json', products)
                        save_financial_transactions('financial.json', financial_transactions, balance)
                        print(f"Sprzedano {sell_quantity} sztuk {product_name} za {cost:.2f} zł. Nowe saldo: {balance:.2f} zł.")
                    else:
                        print(f"Brak wystarczającej ilości produktu {product_name} w magazynie.")
                    product_found = True
                    break
            if not product_found:
                print(f"Produkt {product_name} nie został znaleziony.")
        elif choice == "financials":
            print("Historia transakcji finansowych:")
            for transaction in financial_transactions:
                print(f"Operator: {transaction.operator}, Operacja: {transaction.operation}, "
                      f"Ilość: {transaction.amount}, Koszt: {transaction.cost}, Data: {transaction.date}")
        elif choice == "change password":
            new_password = input("Podaj nowe hasło: ")
            current_user.change_password(new_password)
            save_users('users.json', users)
        elif choice == "raport" and isinstance(current_user, Admin):
            generate_report('users.json', 'products.json', 'financial.json', 'raport_firmy.txt')
        elif choice == "logout":
            loget = False

if __name__ == "__main__":
    main()