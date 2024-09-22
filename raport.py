from data_menager import load_users, load_products, load_financial_transactions
from datetime import datetime


def generate_report(users_file, products_file, financial_file, report_file):
    # Ładujemy dane z plików JSON
    users = load_users(users_file)
    products = load_products(products_file)
    financial_transactions, balance = load_financial_transactions(financial_file)

    # Tworzymy raport
    report_lines = []
    report_lines.append("RAPORT FIRMY".center(50, "="))
    report_lines.append(f"Data raportu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("\n")

    # Sekcja użytkowników
    report_lines.append("UŻYTKOWNICY".center(50, "="))
    for username, user in users.items():
        report_lines.append(f"Login: {username}, Rola: {user.role}")
    report_lines.append("\n")

    # Sekcja produktów
    report_lines.append("PRODUKTY".center(50, "="))
    if products:
        for product in products:
            report_lines.append(f"Nazwa: {product.name}, Cena: {product.price:.2f} zł, Ilość: {product.quantity}")
    else:
        report_lines.append("Brak produktów w magazynie.")
    report_lines.append("\n")

    # Sekcja transakcji finansowych
    report_lines.append("TRANSAKCJE FINANSOWE".center(50, "="))
    if financial_transactions:
        for transaction in financial_transactions:
            report_lines.append(f"Operator: {transaction.operator}, Operacja: {transaction.operation}, "
                                f"Ilość: {transaction.amount}, Koszt: {transaction.cost:.2f} zł, Data: {transaction.date}")
    else:
        report_lines.append("Brak transakcji finansowych.")
    report_lines.append(f"\nSaldo firmy: {balance:.2f} zł")
    report_lines.append("\n")

    # Zapis raportu do pliku tekstowego
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

    print(f"Raport został wygenerowany i zapisany w pliku {report_file}")