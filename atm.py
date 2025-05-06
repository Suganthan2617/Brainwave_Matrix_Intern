# Simple ATM Interface

class ATM:
    def __init__(self):
        self.balance = 1000  # Default balance
        self.pin = "1234"    # Default PIN

    def authenticate(self):
        entered_pin = input("Enter your 4-digit PIN: ")
        if entered_pin == self.pin:
            print("Login successful!\n")
            self.menu()
        else:
            print("Invalid PIN. Try again.\n")
            self.authenticate()

    def menu(self):
        while True:
            print("----- ATM MENU -----")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.check_balance()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    def check_balance(self):
        print(f"Your current balance is ₹{self.balance}\n")

    def deposit(self):
        amount = float(input("Enter amount to deposit: ₹"))
        if amount > 0:
            self.balance += amount
            print(f"₹{amount} deposited successfully.\n")
        else:
            print("Invalid amount.\n")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: ₹"))
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"₹{amount} withdrawn successfully.\n")
        else:
            print("Insufficient balance or invalid amount.\n")

# Run ATM
atm = ATM()
atm.authenticate()
