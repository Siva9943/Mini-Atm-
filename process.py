import psycopg2
import datetime
mydb = psycopg2.connect(
    dbname="atmdb",
    user="postgres",
    password="Siva123",
    host="localhost",
    port="5432"
)
cur = mydb.cursor()

class Atm:
    def __init__(self, user):
        self.user = user
        self.balance = user["balance"]
        self.transactions = []
        mydb.commit()

    def check_balance(self):
        """Displays current balance."""
        print(f"Current balance: Rs{self.balance}")

    def deposit(self, amount):
        """Deposits money into the account."""
        try:
            amount = float(amount)
            if amount > 0:
                self.balance += amount

                cur.execute("UPDATE atm_databases SET balance = %s WHERE user_name = %s",
                            (self.balance, self.user["user_name"]))
                mydb.commit()

                print(f"You have deposited Rs{amount}. Main Balance: Rs{self.balance}")
            else:
                print("Deposit amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def withdraw(self, amount):
        """Withdraws money from the account."""
        try:
            amount = float(amount)
            if 0 < amount <= self.balance:
                self.balance -= amount

       
                cur.execute("UPDATE atm_databases SET balance = %s WHERE user_name = %s",
                            (self.balance, self.user["user_name"]))
                mydb.commit()

                print(f"You have withdrawn Rs:{amount}. Your remaining balance is: Rs:{self.balance}")
            elif amount <= 0:
                print("Withdrawal amount must be greater than zero.")
            else:
                print("Insufficient funds.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def exit(self):
        print("*************************************")
        print("Thank you for using the ATM. Goodbye!")
        print("*************************************")



def atm_menu():
    name = input("Enter your name: ")
    cur.execute("SELECT * FROM atm_databases WHERE user_name = %s", (name,))
    user_data = cur.fetchone()

    if not user_data:
        print("User not found.")
        return

    pin = int(input("Enter your PIN: "))
    if pin != user_data[2]:  
        print("Incorrect PIN.")
        return

    user = {"id": user_data[0], "user_name": user_data[1], "pin_no": user_data[2], "balance": user_data[3]}
    atm = Atm(user)

    while True:
        print("\nATM Menu:")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            atm.check_balance()
        elif choice == '2':
            amount = input("Enter amount to deposit: ")
            atm.deposit(amount)
        elif choice == '3':
            amount = input("Enter amount to withdraw: ")
            atm.withdraw(amount)
        elif choice == '4':
            atm.exit()
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Run ATM Menu
atm_menu()
