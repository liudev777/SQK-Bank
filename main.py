from decimal import Decimal
import random
import psycopg2
import os
import getpass
import datetime
from dotenv import load_dotenv
from misc import *
from asc import *

"""
Establishes connection to local db
"""

load_dotenv()
PASSWORD = os.getenv('PASSWORD')
DBNAME = os.getenv('DBNAME')

def clear():
    print("attempted to clear")
    os.system('cls')
    pass

class App():
    def __init__(self):
        self.stayInApp = True
        self.role = None
        self.identity = None
        self.menu = {}

    class Cust():
        def __init__(self, email, cur) -> None:
            cur.execute(f"SELECT accountid FROM Account WHERE Email = '{email}'")
            allAccId = cur.fetchall()
            self.allAccounts = []

            for accId in allAccId:
                acc = self.Acc(accId[0], cur)
                self.allAccounts.append(acc)
            self.customerEmail = email
            pass

        def __repr__(self) -> str:
            return 'I am a customer'

        def viewAccounts(self, transaction):
            if self.allAccounts:
                # for acc in self.allAccounts:
                #     print(acc)
                transaction()
            else:
                clear()
                print("You don't have any accounts")
            pass

        class Acc():
            def __init__(self, accountID, cur):
                try:
                    cur.execute(f"SELECT balance FROM Account WHERE AccountID = {accountID}")
                    self.balance = cur.fetchall()[0][0]

                    # self.cur.execute(f"SELECT AccountID FROM Account WHERE CustomerID = {accountID}")
                    self.accountId = accountID
                    cur.execute(f"SELECT Type_ID FROM Account WHERE AccountID = {accountID}")
                    self.typeid = cur.fetchall()[0][0]

                    cur.execute(f"SELECT Type FROM AccountTypes WHERE Type_ID = '{self.typeid}'")
                    self.type = cur.fetchall()[0][0]
                    self.accountId = accountID
                except:
                    print("There was an error with making an account")
                    
                

            def __repr__(self) -> str:
                return f'Routing Number: {self.accountId} - Account Type: {self.type} - Balance: {self.balance}'


    class emp():
        def __init__(self,username, cur) -> None:
            self.ssn = None 
            cur.execute(f"SELECT Branch_name FROM Employee WHERE SSN = '{username}';")
            self.branch = cur.fetchall()[0][0]
            pass

    def prompt_user(self):
        print(pc_ascii)
        # Create a connection

        def attempt_connect():
            self.option()
            """
            SQL CONNECTION
            """

            connection = {
                'dbname': DBNAME,
                'user': self.DBusername,
                'host': '127.0.0.1',
                'password': self.DBpassword,
                'port': 5432
                }
            try:
                # self.conn = psycopg2.connect(dbname="university", user="postgres") 
                self.conn = psycopg2.connect(**connection)
                self.cur = self.conn.cursor()
            except psycopg2.errors.OperationalError:
                print("< wrong email or password >")
                if try_again():
                    attempt_connect()
            except:
                print(f"I am unable to connect to the database with connection parameters:\n{connection}")
                exit(1)

        attempt_connect()

        # Create a cursor


        role = self.showGroupRole()
        print("role: ", role) #delete

        if role == 'customerrole':
            self.identity = self.Cust(self.DBusername, self.cur)
            while self.stayInApp:
            # print("status", self.stayInApp) #delete
            # if (type(self.identity) is self.Cust):
                self.menu = {
                    "0": self.leave,
                    "1": self.account,
                    "2": self.identity.viewAccounts
                }
                flag = True
                while flag:
                    # self.identity.viewAccounts()
                    print( #implement logout
                        """
                        1. Add Account
                        2. View Accounts
                        0. Quit
                        """
                        )
                    response = str(input("Select an Action: "))

                    if response == '0':
                        flag = False
                        self.stayInApp = False
                        clear()

                    if response == "2":
                        self.identity.viewAccounts(self.transaction)

                    else:
                        try:
                            clear()
                            self.menu[response]()
                        except KeyError as e:
                            print('Select A Valid Action!')
                            print(self.menu)
                        except:
                            print("Something Went Wrong Please Try Again (customer app)")

        elif role == 'managerrole':
            self.identity = self.emp(self.DBusername, self.cur)
            print("Logged in as a Manager at", self.identity.branch)
            while self.stayInApp:
                self.menu = {
                    "0": self.leave,
                    "1": self.updateFee,
                    "2": self.add_employee,
                    "3": self.viewAnalytics
                }
                flag = True
                while flag:
                    print(
                        """
                        1. Update fee
                        2. Register New Employee
                        3. View Analytics
                        0. Quit
                        """
                    )
                    response = str(input("Select an Action: "))

                    if response == '0':
                        flag = False
                        self.stayInApp = False
                        clear()
                    else:
                        try:
                            clear()
                            self.menu[response]()
                        except KeyError as e:
                            print('Select A Valid Action!')
                            print(self.menu)
                        except:
                            print("Something Went Wrong Please Try Again (employee app)")
                            raise

        elif role == 'tellerrole':
            
            def teller_options(): # display list of options for tellers
                print(
                        """
                        ----------------------------
                        1. View customer account
                        2. Execute transaction
                        3. Log out
                        ----------------------------
                        """
                    )
                response = str(input("Select an Action: "))

                if response == "1": # view customer account
                    accountID = int(input("Enter the ID of the account you want to view: "))

                    try:
                        self.cur.execute(f"SELECT * FROM Account WHERE AccountID = '{accountID}';")
                        account_info = self.cur.fetchall()
                        print("-----------------------------------")
                        print("Balance: ", account_info[0][1])
                        print("Account Type: ", account_info[0][2])
                        print("Email: ", account_info[0][3])
                        print("-----------------------------------")

                        input("press enter to continue")

                        clear()
                        teller_options()

                    except:
                        print("Invalid account id, try again")
                        input("press enter to continue")

                        clear()
                        teller_options()

                elif response == "2": # execute transactions
                    accountID = int(input("Enter the ID of the account you want to make transactions for: "))

                    try:
                        self.execute_transactions(accountID)
                        print("----------------------------------------------------------------")
                        print(f"All transactions for account {accountID} successfully executed!")
                        input("press enter to continue")

                        clear()
                        teller_options()

                    except:
                        print("Invalid account id, try again")
                        input("press enter to continue")

                        clear()
                        teller_options()


                elif response == "3": # log out
                    clear()
                    print("you've successfully logged out!")
                    self.cur.close()
                    self.conn.close()
                    self.prompt_user()
                    
                else:
                    clear()
                    print("Invalid action")
                    teller_options()
            
            teller_options()

        elif role == 'loanmanagerrole':
            
            def loanmanager_options(): # display list of options for loan managers
                print(
                        """
                        ----------------------------
                        1. View customer account
                        2. View customer loans
                        3. Add loans to customer
                        4. Log out
                        ----------------------------
                        """
                    )
                response = str(input("Select an Action: "))

                if response == "1": # view customer account
                    accountID = int(input("Enter the ID of the account you want to view: "))

                    try:
                        self.cur.execute(f"SELECT * FROM Account WHERE AccountID = '{accountID}';")
                        account_info = self.cur.fetchall()
                        print("-----------------------------------")
                        print("Balance: ", account_info[0][1])
                        print("Account Type: ", account_info[0][2])
                        print("Email: ", account_info[0][3])
                        print("-----------------------------------")

                        input("press enter to continue")

                        clear()
                        loanmanager_options()

                    except:
                        print("Invalid account id, try again")
                        input("press enter to continue")

                        clear()
                        loanmanager_options()

                elif response == "2": # view customer loans
                    accountID = int(input("Enter the ID of the account you want to view loans on: "))

                    try:
                        self.cur.execute(f"SELECT * FROM Loans WHERE AccountID = '{accountID}';")
                        loans_list = self.cur.fetchall()

                        if loans_list == []:
                            print("-----------------------------------")
                            print("This account has no loans on record")
                        else:
                            for loan in loans_list:
                                print("-----------------------------------")
                                print("Loan ID: ", loan[3])
                                print("Amount taken: ", loan[0])
                                print("Date taken: ", loan[1].strftime(" %d %b %Y"))
                                print("Date ending: ", loan[2].strftime(" %d %b %Y"))
                                print("Interest Schedule: ", loan[4])

                        print("-----------------------------------")
                        input("press enter to continue")

                        clear()
                        loanmanager_options()

                    except:
                        print("Invalid account id, try again")
                        input("press enter to continue")
                        clear()
                        loanmanager_options()

                elif response == "3": # add loans to customer
                    accountID = int(input("Enter the ID of the account you want to add loans to: "))
                    amount = int(input("Enter the amount of loan: "))
                    starttime = str(input("Enter the starting date of loan (yyyy-mm-dd): "))
                    endtime = str(input("Enter the ending date of loan (yyyy-mm-dd): "))
                    loanid = random.randint(0,99999)
                    interestschedule = str(input("Enter the interest schedule of loan: "))

                    try:
                        self.cur.execute(f"INSERT INTO Loans VALUES ('{amount}', '{starttime}', '{endtime}', '{loanid}', '{interestschedule}', '{accountID}');")
                        self.cur.execute(f"UPDATE Account SET Balance = Balance + '{amount}' WHERE AccountID = '{accountID}';")
                        self.conn.commit()

                        print("--------------------------------------------------------------")
                        print(f"Loan of ${amount} successfully added to account, {accountID}.")
                        input("press enter to continue")

                        clear()
                        loanmanager_options()

                    except:
                        self.conn.rollback()
                        print("Invalid information, try again")
                        input("press enter to continue")

                        clear()
                        loanmanager_options()

                elif response == "4": # log out
                    clear()
                    print("you've successfully logged out!")
                    self.cur.close()
                    self.conn.close()
                    self.prompt_user()
                else:
                    clear()
                    print("Invalid action")
                    loanmanager_options()

            
            loanmanager_options()

        """
        Close connection
        """
        print("here")
        # close the connection
        self.cur.close()
        # close the connection
        self.conn.close()
        self.leave()

    def option(self):
        selection = (input(
            """
            Select an option by typing in the corresponding number
            1. Login
            2. Register
            3. Quit
            Enter Response: 
            """
            ))
        if selection == '2':
            self.register()
            self.option()
        elif selection == '1':
            self.login()
        elif selection == '3':
            self.leave()
        else:
            clear()
            print("Please enter a valid response")
            self.option()
        pass


    def showGroupRole(self):
        # self.cur.execute('SELECT current_user')
        # for row in self.cur.fetchall():
        #     print('current user: ', row[0])
        # self.cur.execute('SELECT current_user')
        # for row in self.cur.fetchall():
        #     print('current user: ', row[0])
        self.cur.execute('SELECT session_user')
        for row in self.cur.fetchall():
            # print('session user: ', row[0])
            sess_user = row[0]
        self.cur.execute(f"""
            select rolname from pg_user
            join pg_auth_members on (pg_user.usesysid=pg_auth_members.member)
            join pg_roles on (pg_roles.oid=pg_auth_members.roleid)
            where
            pg_user.usename='{sess_user}';
        """)
        for row in self.cur.fetchall():
            return(row[0])


    def register(self):

        connection = {
            'dbname': DBNAME,
            'user': 'guest1',
            'host': '127.0.0.1',
            'password': 'guest1',
            'port': 5432
            }

        # Create a connection
        try:
            self.conn = psycopg2.connect(**connection)
            print(f"Connected with \n{connection}")
        except psycopg2.errors.OperationalError:
            print("< guest user and password is somehow wrong. go figure >")
            exit(1)
        except:
            print(f"I am unable to connect to the database with connection parameters:\n{connection}")
            exit(1)

        # Create a cursor
        self.cur = self.conn.cursor()

        self.add_login('customerrole')
            # self.option()
        self.cur.close()
        self.conn.close()

    def login(self):    

        self.DBusername = str(input("enter username > ")).strip()
        self.DBpassword = str(input("enter password > ")).strip()


    def leave(self):
        print(
            """
            *************************************
                Thank You For Using Our App! 
                We Hope To See You Again Soon
            *************************************
            """
            )
        exit() # if removed, it causes infinite loop if you try logging out and quitting
        self.stayInApp = False

    def transaction(self):
        try:
            for (num, account) in enumerate(self.identity.allAccounts, 1):
                print(f"{num}. {account}\n")
            idx = int(input("Please Select An Acoount: "))
            acc = self.identity.allAccounts[idx-1].accountId
            print("acc is: ", acc) #delete
            self.add_Transactions(acc)
        except IndexError:
            print("Please Select A Valid Response")
            self.transaction()
        pass

    def execute_transactions(self, accountID): 
        try:
            self.cur.execute(f"SELECT * FROM Transactions WHERE AccountID = {accountID};")
            allTransactions = self.cur.fetchall()
            self.cur.execute(f"SELECT Balance, Type_ID FROM Account WHERE AccountID = {accountID};")
            tup = self.cur.fetchall()[0]
            balance = int(tup[0])
            typeID = int(tup[1])
            self.cur.execute(f"SELECT CanGoNegative FROM AccountTypes WHERE Type_ID = '{typeID}';")
            neg = self.cur.fetchall()[0][0]
            idx = 0
            c = "Complete"
            if not neg:
                while idx < len(allTransactions) and allTransactions[idx][6] == "Pending":
                    if balance + int(allTransactions[idx][2]) < 0:
                        break
                    balance += int(allTransactions[idx][2])
                    self.cur.execute(f"UPDATE Transactions SET Status = '{c}' WHERE TransID = {allTransactions[idx][0]} ")
                    idx += 1
                self.cur.execute(f"UPDATE Account SET Balance = {balance} WHERE AccountID = {accountID}")
                self.conn.commit()
            else:
                while idx < len(allTransactions) and allTransactions[idx][6] == "Pending":
                    balance += allTransactions[idx][2]
                    self.cur.execute(f"UPDATE Transactions SET Status = '{c}' WHERE TransID = {allTransactions[idx][0]} ")
                    idx += 1
                self.cur.execute(f"UPDATE Account SET Balance = {balance} WHERE AccountID = {accountID}")
                self.conn.commit()
        except: 
            self.conn.rollback()
            print("Something Went Wrong, Try again?")
            raise
            if try_again():
                self.execute_transactions(self, accountID)
        pass
    
    def showStatement(self, accountID):
        try:
            self.cur.execute(f"SELECT TransID, Description, Amount, Time, Transaction_Type, Status, BalanceAfter FROM Transactions WHERE AccountID = {accountID} ORDER BY Time ")
            allTransactions = self.cur.fetchall()
            print("----Current Statement----")
            for transaction in allTransactions:
                if transaction[5] == 'Complete':
                    if transaction[3].month == datetime.datetime.now().month and transaction[3].year == datetime.datetime.now().year:
                        print("\nID: " + str(transaction[0]) + "\nDesc: " + str(transaction[1]) + "\nAmount: " + str(transaction[2]) + "\nDate: " + str(transaction[3]) + "\nType: " + str(transaction[4]), "\nBalance After: " + str(transaction[6]))
        except:
            raise

    def showPending(self, accountID):
        try:
            self.cur.execute(f"SELECT TransID, Description, Amount, Time, Transaction_Type, Status, BalanceAfter FROM Transactions WHERE AccountID = {accountID} ORDER BY Time ")
            allTransactions = self.cur.fetchall()
            print("----Pending Transactions----")
            for transaction in allTransactions:
                if transaction[5] == "Pending":
                    if transaction[3].month == datetime.datetime.now().month and transaction[3].year == datetime.datetime.now().year:
                        print("\nID: " + str(transaction[0]) + "\nDesc: " + str(transaction[1]) + "\nAmount: " + str(transaction[2]) + "\nDate: " + str(transaction[3]) + "\nType: " + str(transaction[4]), "\nBalance After: " + str(transaction[6]))
        except:
            raise
    def account(self):
        self.add_account(self.identity.customerEmail)
        self.cur.execute(f"SELECT accountid FROM Account WHERE Email = '{self.identity.customerEmail}'")
        allAcemail = self.cur.fetchall()
        self.identity.allAccounts = []
        for acemail in allAcemail:
            acc = self.identity.Acc(acemail[0], self.cur)
            self.identity.allAccounts.append(acc)
        pass

                    
                    
    """
    BRANCH transactions
    """
    def add_branch(self, ):
        branch_name = str(input("Enter New Branch Name: ")).strip()
        branch_address = str(input("Enter New Branch Address: ")).strip()
        self.insert_branch(branch_name, branch_address)
        pass

    def insert_branch(self, branch_name, branch_address):
        try:
            self.cur.execute(f"INSERT INTO Branch VALUES('{branch_name}', '{branch_address}');")
            self.conn.commit()
            print(f"Added New Branch: '{branch_name}', '{branch_address}'")
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()
            print("This Address already exists!")
            if try_again():
                self.add_branch()
        except psycopg2.errors.InsufficientPrivilege as e:
            self.conn.rollback()
            print("You do not have permission to do this!")
            if try_again():
                self.add_branch()
        except:
            self.conn.rollback()
            print("Something Went Wrong. Try Again? (Insert branch)")
            raise
            if try_again():
                self.add_branch()
        pass


    """
    EMPLOYEE transactions
    """
    def add_employee(self):
        eName = str(input("Enter New Employee Name: ")).strip()
        eAddress = str(input("Enter Employee Address: ")).strip()
        eSalary = int(input("Enter Salary: "))
        eSSN = int(input("Enter Employee SSN: "))
        eSpecialization = str(input("Choose A Specialization: (Teller/ Manager/ Loan Specialist)")).strip()
        while (eSpecialization != 'Teller' and eSpecialization != 'Loan Specialist' and eSpecialization != "Manager"):
            eSpecialization = str(input("Please select a correct specialization (Teller/ Manager/ Loan Specialist) "))
        eBranch_address = str(input("Enter The Branch The Employee Is Working At: ")).strip()
        eUsername = str(input("Enter New Employee Email"))
        ePassword = str(input("Input New Employee Password"))
        self.insert_employee(eName, eAddress, eSalary, eSSN, eSpecialization, eBranch_address, eUsername, ePassword)
        pass

    def insert_employee(self, eName, eAddress, eSalary, eSSN, eSpecialization, eBranch_address, eUsername, ePassword):
        try:
            self.cur.execute(f"INSERT INTO Employee VALUES({eSSN}, '{eName}', {eSalary}, '{eSpecialization}', '{eAddress}', '{eBranch_address}', '{eUsername}');")
            self.conn.commit()
            self.conn.rollback()
            print(f"Added New Employee: {eSSN}, '{eName}', {eSalary}, '{eSpecialization}', '{eAddress}', '{eBranch_address}', '{eUsername}'")

            if eSpecialization == 'Manager':
                self.insert_login(eSSN, ePassword, 'ManagerRole')
            elif eSpecialization == 'Teller':
                self.insert_login(eSSN, ePassword, 'TellerRole')
            elif eSpecialization == 'Loan Manager':
                self.insert_login(eSSN, ePassword, 'LoanManagerRole')
                
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()
            print("This employee already exists!")
            if try_again():
                self.add_employee()
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            print("This Branch Doesn't Exist, Try Again?")
            if try_again():
                self.add_employee()
        except:
            self.conn.rollback()
            print("Something Went Wrong. Try Again? (Insert employee)")
            raise
            if try_again():
                self.add_branch()
        pass


    """
    CUSTOMER Transactions
    """

    def add_customer(self, email):
        home_branch = str(input("Enter Your Home Branch: ")).strip()
        cName = str(input("Enter Your Name: ")).strip()
        cAddress = str(input("Enter Your Address: ")).strip()
        self.insert_customer(cName, cAddress, email, home_branch)

    def insert_customer(self, cName, cAddress, email, home_branch):
        try:
            self.cur.execute(f"INSERT INTO Customer VALUES('{email}', '{home_branch}', '{cName}', '{cAddress}');")
            self.cur.execute(f"GRANT CustomerRole TO \"{email}\";")
            self.conn.commit()
            print("Success! You're now registered as ", email)
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            print("This Customer Already Exists!")
            if try_again():
                self.add_customer(email)
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            print("This Branch Doesn't Exist, Try Again?")
            if try_again():
                self.add_customer(email)
        except psycopg2.errors.DuplicateObject:
            self.conn.rollback()
            print(f"User with {email} already exists.")
            if try_again():
                self.add_customer(email)
        except:
            self.conn.rollback()
            print("Something Went Horribly Wrong (Insert Customer)")
            raise
            if try_again():
                self.add_customer(email)

    

    """
    ACCOUNTTYPES Transactions
    """

    def add_accounttype(self):
        typeID = str(input("Enter type ID: ")).strip()
        type = str(input("Checkings or Savings?")).strip()
        interestRate = int(input("Set An Interest Rate"))
        balance = str(input("Minimum balance")).strip()
        monthly_fee = int(input("Enter Monthly Fee"))
        overdraftfee = int(input("Enter Overdraft Fees"))
        canNegative = bool(input("Can the account go negative? (True/False)"))
        
        self.insert_accounttype(typeID, type, interestRate, balance, monthly_fee, overdraftfee, canNegative)

    def insert_accounttype(self, typeID, type, interestRate, balance, monthly_fee, overdraft, canNegative):
        try:
            self.cur.execute(f"INSERT INTO AccountTypes VALUES('{typeID}', '{type}', {interestRate}, {balance}, {monthly_fee}, {overdraft}, {canNegative});")
            self.conn.commit()
            print(f"Added New Account Type: '{typeID}', '{type}', {interestRate}, {balance}, {monthly_fee}, {overdraft}")
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()
            print("This Account Type Already Exists!")
            if try_again():
                self.add_accounttype()
        except:
            self.conn.rollback()
            print("Something Went Wrong. Try Again? (insert accounttypes)")
            raise
            if try_again():
                self.add_accounttype()
        pass

    """
    ACCOUNT Transactions
    """

    def add_account(self, email):
        
        accountID = random.randint(100_000_000, 999_999_999)
        balance = 0
        typeID = int(input(r"""
            1. Checking - 1% ROI - min Balance: $100 - Monthly: $4 - Yes negative
            2. Checking - 5% ROI - min Balance: $600 - Monthly: $10 - No negative
            3. Savings - 50% ROI - min Balance: $1000 - Monthly: $15 - No negative
            4. Savings - 75% ROI - min Balance: $2000 - Monthly: $20 - No negative
            Enter type number: 
                            """))
        self.insert_account(accountID, balance, typeID, email)
        print("New account added!")


    def insert_account(self, accountID, balance, typeID, email):
        result = False
        try:
            self.cur.execute(f"INSERT INTO ACCOUNT VALUES({accountID}, {balance}, '{typeID}', '{email}');")
            self.conn.commit()
            self.conn.rollback()
            print(f"Added New ACCOUNT: {accountID}, {balance}, '{typeID}'{email}'")
            result = True
            return result
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()
            print("This Account Already Exists!")
            if try_again():
                self.add_account(email) 
            #     return result
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            print("This Customer or Type Doesn't Exist, Try Again?")
            raise
            if try_again():
                self.add_account()
            return result
        except:
            self.conn.rollback()
            print("Something Went Wrong. Try Again? (insert account)")
            raise
            if try_again():
                self.add_account()
            return result
        pass

    """
    TRANSACTIONS Transactions
    """

    def add_Transactions(self, accountID):
        try:
            response = str(input("""
                    1. Deposit
                    2. Withdraw
                    3. Transfer
                    4. External Transfer
                    5. Statement
                    6. Pending Transactions
                    7. Quit
                    Select An Option: """))
            if response == "5":
                self.showStatement(accountID)
            elif response == "6":
                self.showPending(accountID)
            elif response == '7':
                return
            else:
                transactionAmount = int(input("Please Enter An Amount: "))
                print("Account ID: ", accountID)
                self.cur.execute(f"SELECT Balance FROM Account WHERE AccountID = {accountID}")
                balance = self.cur.fetchall()[0][0]
                if response == '2' or response == '3' or response == '4':
                    transactionAmount = transactionAmount * (-1.0)
                print(f'balance: {balance}, transaction amount: {transactionAmount}')
                newBalance = balance + transactionAmount
                self.cur.execute(f"SELECT Type_ID FROM Account WHERE AccountID = {accountID}")
                typeID = self.cur.fetchall()[0][0]
                self.cur.execute(f"SELECT CanGoNegative FROM AccountTypes WHERE Type_ID = '{typeID}'")
                neg = self.cur.fetchall()[0][0]
                if not neg and newBalance < 0:
                    print("You Have Insufficient Funds For This Transaction")
                    if try_again():
                        self.add_Transactions(accountID)
                else:
                    description = str(input("Please Enter A Description For This Transaction: "))
                    transactionID = random.randint(100_000_000, 999_999_999)
                    if response == "1":
                        transactionType = "Deposit"
                    elif response == "2":
                        transactionType = "Withdraw"
                    elif response == "3":
                        transactionType = "Transer"
                    elif response == "4":
                        transactionType = "External Transfer"
                    def ins_tran(transactionID):
                        try:
                            if response == "1" or response == "2":
                                self.insert_Transactions(transactionID, description, transactionAmount, datetime.datetime.now(), transactionType, accountID, "Pending", newBalance)
                            elif response == "3" or response == "4":
                                self.transfer(transactionID, description, transactionAmount, datetime.datetime.now(), transactionType, accountID, "Pending", newBalance)
                            else:
                                print("Please Enter a valid Input!")
                                if try_again():
                                    self.add_Transactions(accountID)
                        except psycopg2.errors.UniqueViolation:
                            transactionID = random.randint(100_000_000, 999_999_999)
                            ins_tran(transactionID)
                        except:
                            print("An error has occured")
                            raise
                    
                    ins_tran(transactionID)
        except :
            raise
            print("Something Went Wrong. Try Again? (Add transactions)")
            if try_again():
                self.add_Transactions(accountID)

    def insert_Transactions(self, transID, desc, amount, time, transaction_type, accountID, status, newBalance):
        try:
            print("1")
            self.cur.execute(f"INSERT INTO Transactions VALUES({transID}, '{desc}', {amount}, '{time}', '{transaction_type}', {accountID}, '{status}', {newBalance})")
            print("2")
            if newBalance < 0:
                self.addOverDraftFees(accountID)
            self.conn.commit()
            print(f"Added New Transaction: {transID}, '{desc}', {amount}, '{time}', '{transaction_type}', {accountID}. '{status}', {newBalance}")
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()
            print("This Transaction Already Exists!")
            if try_again():
                self.add_Transactions(accountID)
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            print("This Account Doesn't Exist, Try Again?")
            if try_again():
                self.add_Transactions(accountID)
        except:
            self.conn.rollback()
            print("Something Went Wrong. Try Again? (insert transactions)")
            if try_again():
                self.add_Transactions(accountID)
        pass

    def transfer(self, transactionID, description, transactionAmount, date, transactionType, senderID, status, newBalance):
        try:
            recieverID = str(input("Please Enter The Account Of the Recipient: "))
            secondID = transactionID + 1
            recievedAmount = (-1) * transactionAmount
            self.cur.execute(f"SELECT Balance FROM Account WHERE AccountID = {recieverID}")
            balance = self.cur.fetchall()[0][0]
            print(balance)
            newRecieverBalance = balance + recievedAmount 
            self.cur.execute(f"INSERT INTO Transactions VALUES({transactionID}, '{description}', {transactionAmount}, '{date}', '{transactionType}', {senderID}, '{status}', {newBalance});")
            self.cur.execute(f"INSERT INTO Transactions VALUES({secondID}, '{description}', {recievedAmount}, '{date}', '{transactionType}', {recieverID}, '{status}', {newRecieverBalance});")
            self.conn.commit()
            print(f"Added New Transaction: {transactionID}, '{description}', {transactionAmount}, '{date}', '{transactionType}', {senderID}, '{status}', {newBalance}")
            print(f"Added New Transaction: {secondID}, '{description}', {recievedAmount}, '{date}', '{transactionType}', {recieverID}, '{status}', {newRecieverBalance}")
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()
            print("This Transaction Already Exists!")
            if try_again():
                self.transfer(transactionID, description, transactionAmount, date, transactionType, senderID, status, newBalance)
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            print("This Account Doesn't Exist, Try Again?")
            if try_again():
                self.transfer(transactionID, description, transactionAmount, date, transactionType, senderID, status, newBalance)
        except:
            self.conn.rollback()
            print("Something Went Wrong. Try Again? (insert transactions)")
            if try_again():
                self.transfer(transactionID, description, transactionAmount, date, transactionType, senderID, status, newBalance)
        pass

    """
    LOGININFO Transactions
    """

    def add_login(self, role):
        email = str(input("Your email address: ")).strip()
        password = str(input("Create a Password: ")).strip()
        self.insert_login(email, password, role)
  

    def insert_login(self, email, password, role):
        try:
            if role == 'customerrole':
                self.cur.execute(f"CREATE USER \"{email}\" WITH LOGIN PASSWORD '{password}';")
                self.cur.execute(f"GRANT {role} TO \"{email}\"")
                self.conn.commit()
                self.add_customer(email)
            elif role == 'ManagerRole':
                self.cur.execute(f"CREATE USER \"{email}\" WITH LOGIN PASSWORD '{password}' SUPERUSER;")
                self.cur.execute(f"GRANT {role} TO \"{email}\"")
                self.conn.commit()
            else:
                self.cur.execute(f"CREATE USER \"{email}\" WITH LOGIN PASSWORD '{password}';")
                self.cur.execute(f"GRANT {role} TO \"{email}\"")
                self.conn.commit()

        except psycopg2.errors.DuplicateObject:
            self.conn.rollback()
            print(f"User with {email} already exists.")
            if try_again():
                self.add_login(role)
        except:
            self.conn.rollback()
            print("Something Went Wrong With Inserting Login. Try Again?")
            raise
            if try_again():
                add_login(username)
        
    def updateFee(self):
        branch = self.identity.branch
        allAccountID = []
        self.cur.execute(f"SELECT AccountID FROM Account NATURAL JOIN Customer WHERE Branch_name = '{branch}'")
        accounts = self.cur.fetchall()
        for account in accounts:
            allAccountID.append(int(account[0]))
        for accountId in allAccountID:
            self.addInterest(accountId)
            self.chargeMonthlyFee(accountId)
        pass

    def addInterest(self, accountID):
        self.cur.execute(f"SELECT Balance, Interest_Rate FROM Account NATURAL JOIN AccountTypes WHERE AccountID = {accountID}")
        tup = self.cur.fetchall()[0]
        print(f"tup = {tup}")
        print(f"Account Id = {accountID}")
        balance = Decimal((tup[0][0][1:]).replace(",",""))
        interest = Decimal(tup[1])
        newBal = balance * interest + balance
        print(f"newbalance = {newBal}")
        self.cur.execute(f"UPDATE Account SET Balance = {newBal} WHERE AccountID = {accountID}")
        self.conn.commit()
        print(f"interest: ", interest)
        print(f"Interest added! {newBal}")

    def addOverDraftFees(self, accountID):
        self.cur.execute(f"SELECT OverDraft_Fee FROM Account WHERE AccountID = {accountID}")
        fee = Decimal(self.cur.fetchall()[0][0])
        
        self.cur.execute(f"SELECT Balance FROM Account WHERE AccountID = {accountID}")
        bal = self.cur.fetchall()[0]
        self.cur.execute(f"UPDATE Account SET Balance = {bal - fee} WHERE AccountID ={accountID}")
        self.conn.commit()
        print(f"charged ${fee} in overcharge fee!")
        pass

    def chargeMonthlyFee(self, accountID):
        self.cur.execute(f"SELECT MinBalance FROM AccountTypes NATURAL JOIN Account WHERE AccountID = {accountID}")
        minBal = (self.cur.fetchall()[0][0][1:])
        minBal = Decimal(minBal.replace(",",""))
        self.cur.execute(f"SELECT Balance, Type_ID FROM Account WHERE AccountID = {accountID}")
        balance = Decimal((self.cur.fetchall()[0][0][1:]).replace(",",""))
        if balance < minBal:
            self.cur.execute(f"SELECT Monthly_Fee FROM AccountTypes NATURAL JOIN Account WHERE AccountID = {accountID}")
            monthlyfee = Decimal(self.cur.fetchall()[0][0][1:])
            self.cur.execute(f"UPDATE Account SET Balance = {balance - monthlyfee} WHERE AccountID = {accountID}")
            self.conn.commit()
            print(f"charged ${monthlyfee} in monthly fee!")

    def viewAnalytics(self):
        self.cur.execute(f"SELECT * FROM Branch;")
        branches = self.cur.fetchall()
        for branch in branches:
            # print(branch[0]) #delete
            accountSum = 0
            self.cur.execute(f"SELECT Balance FROM Account NATURAL JOIN Customer WHERE Branch_name = '{branch[0]}'")
            balances = self.cur.fetchall()
            for bal in balances:
                accountSum += int(bal[0])

            print(f"{branch[0]}'s accountSum: {accountSum}")

        pass




 
App().prompt_user()

