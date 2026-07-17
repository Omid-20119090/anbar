import os,csv
import matplotlib.pyplot as plt
DATA_FILE = os.path.join("data" , "transactions.csv")

def main():
    while True:
        ch = input("please choose from 1 , 2 , 3 , 4 , 5 , 6 or 7")
        if ch == "1":
            add_transactions()
        elif ch == "2":
            view_transactions()
        elif ch == "3":
            show_summary()
        elif ch == "4":
            filter_transactions()
        elif ch == "5":
            save_report()
        elif ch == "6":
            show_chart()
        elif ch == "7":
            print("see you soon !")
            break
        else:
            print("your number should be from 1 , 2 , 3 , 4 , 5 , 6, 7 " )
def show_menu():
    print("1 = add_transaction")
    print("2 = view_transaction")
    print("3 = summary")
    print("4 = filter")
    print("5 = save report")
    print("6 = exit")
    return

def add_transactions():
    t_type = input("which one? (income , expense)")
    if t_type not in ("income,expense"):
        print("your choose should be from income or expense ")
        return
    amount = input("amount = ")
    try :
        amount = float(amount)
    except ValueError:
        print("enter the number")

    date = input("please enter s date (yyyy/mm/dd)")

    category = input("category = ")

    transaction = {
        "type" : t_type,
        "amount" : amount,
        "date" : date,
        "category" : category
    }

    save_transaction(transaction)
    print("transactions are succesfuly saved !")

def save_transaction(transaction):
    file_exist = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, "a" , newline="" , encoding="utf-8") as fhand:
        writer = csv.writer(fhand)
        if not file_exist:
            writer.writerow(["type","amount","date","category"])
        writer.writerow([
            transaction["type"],
            transaction["amount"],
            transaction["date"],
            transaction["category"]
        ])

def view_transactions():
    if not os.path.isfile(DATA_FILE):
        print("there are no transactions. please add one first !")
        return
    with open(DATA_FILE, "r" , newline="" , encoding="UTF-8") as fhand :
        reader = csv.reader(fhand)
        header = next(reader,None)
        rows = list(reader)

        if not rows:
            print("no transaction to show ")
            return
        
        print()
        print(f"{header[0]:<12} , {header[1]:<12} , {header[2]:<12} , {header[3]:<12}")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]:<12} , {float(row[1]):<12} , {row[2]:<12} , {row[3]:<12}")

def load_transactions():
    if not os.path.isfile(DATA_FILE):
        print("no transactions to load ")
    transactions = []
    with open (DATA_FILE , "r" , newline="" , encoding="{utf-8}") as fhand:
        reader = csv.DictReader(fhand)
        for row in reader :
            row["amount"] = float(row["amount"])
            transactions.append(row)
    return transactions

def show_summary():
    transactions = load_transactions()
    if not transactions:
        print("no transactions to summary")
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")

    print("\n >>> transactions summary <<<")
    print(f"total_income:{total_income:,.2f}")
    print(f"total_expense:{total_expense:,.2f}")
    print(f"net_balance:{total_income - total_expense:,.2f}")

def filter_transactions():
    transactions = load_transactions()
    if not transactions :
        print("no any transactions")
    print("filter :")
    print("1 = type")
    print("2 = category")
    print("3 = date range")

    choice = input("which one from 1 , 2 and 3 ?")

    if choice == "1":
        t_type = input("income or expense ?")
        filtered = list(filter(lambda t: t["type"] == t_type , transactions))

    elif choice == "2" :
        category = input("which category ?")
        filtered = list(filter(lambda t: t["category"] == category , transactions))

    elif choice == "3" :
        start =  input("start date = (yyyy-mm-dd)")
        end = input("end date = (yyyy-mm-dd)")
        filtered = list(filter(lambda t : start <= t["date"] <= end, transactions))

    else:
        print("invalid filtered transactions ")
        return
    
    if not filtered :
        print("no filtered transactions")
        return
    
    print(f"\n --- filtered transactions {len(filtered)} --- ")
    print(f"{'t_type':<12} , {'amount':<12} , {'category':<12} , {'date':<12}")
    print("✨" * 20)
    for t in filtered :
        print(f"{t['type']:<12} , {t['amount']:<12} , {t['category']:<12} , {t['date']:<12}")

def save_report():
    transactions = load_transactions()
    if not transactions:
        print("no transactions to save")

    report_file = os.path.join("data" , "report.txt")
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")


    with open (report_file , "w" , encoding="utf-8") as fhand:
        fhand.write("=== FINANCE REPORT ===\n\n")
        fhand.write(f"total_income = {total_income}\n")
        fhand.write(f"total_expense = {total_expense}\n")
        fhand.write(f"net_balance = {total_income - total_expense}\n")
        fhand.write("🎃" * 20 + "\n")
        fhand.write(f"{'t_type':<12} , {'amount':<12} , {'category':<12} , {'date':<12}")
        for t in transactions :
            fhand.write(f"{t['type']:<12} , {t['amount']:<12.2f}, {t['category']:<12} , {t['date']:<12}\n")

def show_chart():
    transactions = load_transactions()
    if not transactions :
        print("no transactions to draw a chart ")
        return
    
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income" )
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense ")

    labels = ["total income" , "total expense "] 
    values = [total_income , total_expense]
    colors = ["#19DB20" , "#F41D1D"  ]

    plt.figure(figsize=(4,7))
    plt.bar(labels , values , color = colors)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__" :
    main()

