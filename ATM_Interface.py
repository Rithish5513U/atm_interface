class User:
    def __init__(self, userid, password, balance=0, transactions=None):
        self.userid = userid
        self.password = password
        self.balance = balance
        self.transactions = transactions if transactions else []

    def deposit(self, amount):
        self.balance += amount
        print("Amount deposited successfully !!!")
        self.transactions.append(f'Deposit: ${amount}')

    def check_balance(self):
        print(f"Balance: ${self.balance}")

    def withdraw(self, amount):
        if self.balance < amount:
            print("Insufficient funds in account")
        else:
            self.balance -= amount
            print("Amount withdrawn successfully !!!")
            self.transactions.append(f'Withdraw: ${amount}')

    def transfer(self, receiver, amount):
        if self.balance < amount:
            print("Insufficient funds in account")
        else:
            self.balance -= amount
            receiver.balance += amount
            self.transactions.append(f'Transfer to {receiver.userid}: ${amount}')
            receiver.transactions.append(f'Transfer from {self.userid}: ${amount}')
            print("Amount transferred successfully !!")
            User(self.userid,self.password).check_balance()

    def history(self):
        print("Transaction history : ")
        for transaction in self.transactions:
            print(transaction)

class Atm:
    def __init__(self, user_file='users.txt', transaction_file='transactions.txt'):
        self.users = self.load_users(user_file)
        self.user_file = user_file
        self.transaction_file = transaction_file

    def load_users(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                users = {}
                for line in lines:
                    user_data = line.strip().split(',')
                    userid, password, balance, transactions = user_data
                    user = User(userid, password, float(balance), transactions.split(';'))
                    users[user.userid] = user
                return users
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.user_file, 'w') as file:
            for user in self.users.values():
                file.write(f"{user.userid},{user.password},{user.balance},{';'.join(user.transactions)}\n")

    def add_user(self, userid, password):
        if userid not in self.users:
            self.users[userid] = User(userid, password)
            print("Account created successfully !!!")
            self.save_users()
        else:
            print("User already registered !!!")

    def authorize(self, userid, password):
        if userid in self.users and password == self.users[userid].password:
            return self.users[userid]
        else:
            print("User id or password is invalid !!!")
            return None

    def save_transaction(self, user):
        with open(self.transaction_file, 'a') as file:
            file.write(f"User: {user.userid}, Transaction History: {user.transactions}\n")

    def retrieve_balance_and_history(self, userid):
        user = self.users.get(userid)
        if user:
            return user.balance, user.transactions
        else:
            return None

atm = Atm()

while True:
    print("Enter choice:")
    print("1. Create account")
    print("2. Login")
    print("3. Quit")

    choice = input("Choice: ")
    
    if choice == "1":
        userid = input("Enter userid: ")
        password = input("Enter password: ")
        atm.add_user(userid, password)
        print("")

    elif choice == "2":
        userid = input("Enter userid: ")
        password = input("Enter password: ")
        user = atm.authorize(userid, password)

        if user:
            while True:
                print("Enter your purpose:")
                print("1. Deposit")
                print("2. Transfer")
                print("3. Withdraw")
                print("4. Transaction History")
                print("5. Check Balance")
                print("6. Quit")
                
                ch = input("Choice: ")

                if ch == "1":
                    amount = int(input("Enter amount to deposit: $"))
                    user.deposit(amount)
                    atm.save_users()
                    print("")

                elif ch == "2":
                    recipient_user = input("Enter Recipient id to transfer: ")
                    amount = int(input("Enter amount to transfer: $"))
                    recipient = atm.users.get(recipient_user)
                    
                    if recipient:
                        user.transfer(recipient, amount)
                        atm.save_users()
                        print("")
                    else:
                        print("Recipient not found.")

                elif ch == "3":
                    amount = int(input("Enter amount to withdraw: $"))
                    user.withdraw(amount)
                    atm.save_users()
                    print("")

                elif ch == "4":
                    user.history()
                    print("")

                elif ch == "5":
                    balance, history = atm.retrieve_balance_and_history(userid)
                    print(f"Balance: ${balance}")
                    print("")

                elif ch == "6":
                    atm.save_transaction(user)
                    print("Transaction saved.")
                    break

    elif choice == "3":
        print("\nHave a nice day !!!")
        break

    else:
        print("Invalid choice. Please try again.\n")
