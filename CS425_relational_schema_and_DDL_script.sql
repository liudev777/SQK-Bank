DROP TABLE IF EXISTS Employee CASCADE;
DROP TABLE IF EXISTS Branch CASCADE;
DROP TABLE IF EXISTS Customer CASCADE;
DROP TABLE IF EXISTS Account CASCADE;
DROP TABLE IF EXISTS AccountTypes CASCADE;
DROP TABLE IF EXISTS Loans CASCADE;
DROP TABLE IF EXISTS Transactions CASCADE;

CREATE TABLE Branch (
	Branch_name			varchar(30) PRIMARY KEY,
	Baddress			varchar(50)
);

CREATE TABLE Employee (
	SSN					char(9),
	Name				varchar(30),
	Salary				int,
	Specialization		varchar(30),
	Eaddress			varchar(50),
	Branch_name			varchar(30),
	Username			varchar(20),
	PRIMARY KEY (SSN),
	FOREIGN KEY (Branch_name) REFERENCES Branch
);

CREATE TABLE Customer (
	Email				varchar(30) PRIMARY KEY,
	Branch_name			varchar(30),
	Name				varchar(30),
	Caddress			varchar(50),
	FOREIGN KEY (Branch_name) REFERENCES Branch
);

CREATE TABLE AccountTypes (
	Type_ID				varchar(10),
	Type				varchar(30),
	Interest_Rate		decimal(4,2),
	MinBalance			int,
	Monthly_Fee			int,
	OverDraft_Fee		int,
	CanGoNegative		boolean,
	PRIMARY KEY (Type_ID)
);

CREATE TABLE Account (
	AccountID			int,
	Balance         	int,
	Type_ID				varchar(10),
	Email				varchar(30),
	PRIMARY KEY (AccountID),
	FOREIGN KEY (Email) REFERENCES Customer,
	FOREIGN KEY (Type_ID) REFERENCES AccountTypes
);

CREATE TABLE Transactions (
	TransID				int,
	Description			varchar(50),
	Amount				int,
	Time				timestamp,
	Transaction_type	varchar(20),
	AccountID			int NOT NULL,
	Status				varchar(20),
	BalanceAfter		int,
	PRIMARY KEY (TransID, AccountID),
	FOREIGN KEY (AccountID) REFERENCES Account
);
CREATE TABLE Loans (
	Amount				int,
	Starttime			date,
	Endtime				date,
	Loan_ID				varchar(10),
	Interest_Schedule	varchar(10),
	AccountID			int,
	PRIMARY KEY (Loan_ID),
	FOREIGN KEY (AccountID) REFERENCES Account
);


INSERT INTO Branch VALUES ('J.D MORMAN North', '123 S Poplar');
INSERT INTO Branch VALUES ('J.D MORMAN East', '215 S Laflin');
INSERT INTO Branch VALUES ('J.D MORMAN West', '997 S Parnell');
INSERT INTO Branch VALUES ('J.D MORMAN South', '383 S Emerald');

INSERT INTO Employee VALUES ('312000123', 'Bob', '80000', 'Teller', '321 S Wallace', 'J.D MORMAN North');
INSERT INTO Employee VALUES ('312541123', 'Alice', '80000', 'Loan Specialist', '335 S Normal', 'J.D MORMAN West');
INSERT INTO Employee VALUES ('312321321', 'Rick', '80000', 'Manager', '222 S Normal', 'J.D MORMAN East');
INSERT INTO Employee VALUES ('312123123', 'Barbara', '30000', 'Manager', '990 S Archer', 'J.D MORMAN South');

INSERT INTO Customer VALUES ('wojtek@gmail.com', 'J.D MORMAN North', 'Wojtek', '583 S Cermak');
INSERT INTO Customer VALUES ('mcneil@yahoo.com', 'J.D MORMAN East', 'McNeil', '182 S Michigan');
INSERT INTO Customer VALUES ('guerrero@aol.com', 'J.D MORMAN West', 'Guerrero', '281 S Halsted');

INSERT INTO AccountTypes VALUES ('11', 'Checking', '0.01', '100', '4', '10', 'true');
INSERT INTO AccountTypes VALUES ('12', 'Checking', '0.05', '600', '10', '0', 'false');
INSERT INTO AccountTypes VALUES ('21', 'Savings', '0.50', '1000', '15', '20', 'false');
INSERT INTO AccountTypes VALUES ('22', 'Savings', '0.75', '2000', '20', '0', 'false');

INSERT INTO Account VALUES ('10001', '100000', '11', 'wojtek@gmail.com');
INSERT INTO Account VALUES ('10011', '100000', '12', 'wojtek@gmail.com');
INSERT INTO Account VALUES ('10002', '200', '12', 'mcneil@yahoo.com');
INSERT INTO Account VALUES ('10003', '800', '21', 'guerrero@aol.com');

INSERT INTO Transactions VALUES ('50001', 'Deposited a whole lotta money', '50000', '2022-10-15 3:12:50', 'Deposit', '10001');
INSERT INTO Transactions VALUES ('50002', 'Withdrew a money', '-5000', '2008-03-02 15:01:00', 'Withdraw', '10002');
INSERT INTO Transactions VALUES ('50003', 'Transfer money to Guerrero', '-1337', '2010-08-25 21:58:13', 'Transfer', '10002');
INSERT INTO Transactions VALUES ('50004', 'Transfer money to McNeil', '-1337', '2010-08-25 21:59:33', 'Transfer', '10003');
INSERT INTO Transactions VALUES ('50005', 'Transfer money to Bank of The United State', '-2000', '2015-03-11 18:23:56', 'External Transfer', '10001');

INSERT INTO Loans VALUES ('50000', '2010-08-25', '2015-08-25', '32138', 'Annual', '10001');
INSERT INTO Loans VALUES ('1000000', '2020-02-10', '2021-02-10', '51238', 'Annual', '10001');
INSERT INTO Loans VALUES ('100', '2000-01-07', '2020-01-07', '09321', 'Quarterly', '10002');
INSERT INTO Loans VALUES ('9999999', '2005-03-07', '205-05-07', '54313', 'Daily', '10003');
INSERT INTO Loans VALUES ('73812', '2016-02-10', '2021-02-10', '39786', 'Monthly', '10011');

-- ROLE CREATION

DROP ROLE IF EXISTS ManagerRole;
CREATE ROLE ManagerRole WITH SUPERUSER;

DROP ROLE IF EXISTS LoanManagerRole;
CREATE ROLE LoanManagerRole;
GRANT SELECT, UPDATE ON Account TO LoanManagerRole;
GRANT SELECT, INSERT ON Loans TO LoanManagerRole;

DROP ROLE IF EXISTS TellerRole;
CREATE ROLE TellerRole;
GRANT SELECT, UPDATE ON Account TO TellerRole;
GRANT SELECT, INSERT ON Transactions TO TellerRole;
GRANT SELECT ON AccountTypes TO TellerRole;

DROP ROLE IF EXISTS CustomerRole;
CREATE ROLE CustomerRole;
GRANT SELECT ON Customer TO CustomerRole;
GRANT SELECT, INSERT ON Account TO CustomerRole;
GRANT SELECT ON AccountTypes TO CustomerRole;
GRANT SELECT, INSERT ON Transactions TO CustomerRole;

DROP ROLE IF EXISTS GuestRole;
CREATE ROLE GuestRole SUPERUSER;
GRANT INSERT ON Customer TO GuestRole;
GRANT INSERT ON Account TO GuestRole;

-- POLICY CREATION

/*
ALTER TABLE Customer ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS CustomerView ON Customer;
CREATE POLICY CustomerView ON Customer TO CustomerRole USING (Email = current_user);

ALTER TABLE Account ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS AccountView ON Account;
CREATE POLICY AccountView ON Account TO CustomerRole USING (Email = current_user);
*/

-- USER CREATION

-- MANAGERS
DROP USER IF EXISTS "312321321";
CREATE USER "312321321" WITH LOGIN PASSWORD 'rick' SUPERUSER;
GRANT ManagerRole TO "312321321";

DROP USER IF EXISTS "312123123";
CREATE USER "312123123" WITH LOGIN PASSWORD 'barbara' SUPERUSER;
GRANT ManagerRole TO "312123123";

-- LOAN MANAGERS
DROP USER IF EXISTS loanmanager1;
CREATE USER loanmanager1 WITH LOGIN PASSWORD 'loanmanager1' BYPASSRLS;
GRANT LoanManagerRole TO loanmanager1;

-- TELLERS
DROP USER IF EXISTS teller1;
CREATE USER teller1 WITH LOGIN PASSWORD 'teller1' BYPASSRLS;
GRANT TellerRole TO teller1;

-- CUSTOMERS
DROP USER IF EXISTS "wojtek@gmail.com";
CREATE USER "wojtek@gmail.com" WITH LOGIN PASSWORD 'wojtek';
GRANT CustomerRole TO "wojtek@gmail.com";

DROP USER IF EXISTS "mcneil@yahoo.com";
CREATE USER "mcneil@yahoo.com" WITH LOGIN PASSWORD 'mcneil';
GRANT CustomerRole TO "mcneil@yahoo.com";

DROP USER IF EXISTS "guerrero@aol.com";
CREATE USER "guerrero@aol.com" WITH LOGIN PASSWORD 'guerrero';
GRANT CustomerRole TO "guerrero@aol.com";

-- GUEST (for registering customers)
DROP USER IF EXISTS guest1;
CREATE USER guest1 WITH LOGIN PASSWORD 'guest1' CREATEROLE SUPERUSER;
GRANT GuestRole TO guest1;