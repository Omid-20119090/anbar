import os,csv
DATA_FILE = os.path.join("data" , "transaction.csv")

def main():
    while True:
        show_menu()
        choice = input("choose from 1,2,3")
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transaction()
        elif choice == "3":
            print("see you soon !!")
            break
        else :
            print("your choice should be from 1,2 or 3")
def show_menu():
    print("\n <<<< personal finance tracker >>>>")
    print("1 = add transaction")
    print("2 = view ttransaction")
    print("3 = exit")

def add_transaction():
    t_type = input ("write (income,expense)")
    if t_type not in ("income","expense") :
        print("t_type can be 'income' and 'expense' !")
        return
    
    amount = input("amount: ")
    try:
        amount = float(amount)
    except ValueError:
        print("your amount should be a float")
        return
    
    category = input("category = ")

    date = input(" date : __yyyy__mm__dd")

    transaction = {
        "type" : t_type,
        "amount" : amount,
        "category" : category,
        "date" : date
        }
    
    save_transaction(transaction)
    print("_____done_____")



def save_transaction(transaction):
    file_exist = os.path.isfile(DATA_FILE)
    with open (DATA_FILE, "a" , newline="" , encoding="utf-8") as fhand:
        writer = csv,writer(fhand)
        if not file_exist:
            writer.writerow(["TYPE" , "AMOUNT" , "CATEGORY" , "DATE"])
        writer.writerow([
            transaction["type"],
            transaction["amount"],
            transaction["category"],
            transaction["date"]
        ])

def view_transaction():
    if not os.path.isfile(DATA_FILE):
        print("there are no transaction...")
        return
    with open (DATA_FILE,newline="",encoding="ytf-8") as fhand:
        reader = csv.reader(fhand)
        header = next(reader,None)
        rows = list(reader)
    if not rows:
        print("no transaction")
        return
    print()
    print(f"{header[0] :<15} , {header[1] :<15} , {header[2] :<15} , {header[3] :<15}")
    print("[]" * 50)
    for row in rows :
        print(f"{row[0] :<15} , {row[1] :<15} , {row[2] : 15} , {row[3] :<15}")



if __name__=="__main__" :
    main() 
    
