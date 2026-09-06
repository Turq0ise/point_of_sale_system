#  

import json
import uuid
from pathlib import Path
ACCOUNTS_DATA_FILE_NAME = "DATA/accounts.json"
ACCOUNTS_DATA_FILE_PATH = Path(ACCOUNTS_DATA_FILE_NAME)

class Customer:
    def __init__(self, email, password, customerId, name, address, orders):
        self.email = email
        self.password = password
        self.customerId = customerId
        self.name = name
        self.address = address
        self.orders = orders

def getFileContents():
    fileContents = []
    if ACCOUNTS_DATA_FILE_PATH.is_file(): 
        if ACCOUNTS_DATA_FILE_PATH.stat().st_size != 0: 
            with open(ACCOUNTS_DATA_FILE_NAME, "r") as file:
                fileContents = json.load(file)
    else:
        with open(ACCOUNTS_DATA_FILE_NAME, "w") as file:
            json.dump(fileContents, file, indent=4)
    return fileContents 

def writeToFile(object):
    data = getFileContents()
    data.append(object)
    with open(ACCOUNTS_DATA_FILE_NAME, "w") as file:
        json.dump(data, file, default=vars, indent=4)

def checkIfEmailTaken(email):
    data = getFileContents()
    for user in data:
        if user["email"] == email: return False
    return True

def checkUserCredentials(email, password):
    data = getFileContents()
    for user in data:
        if user["email"] == email and user["password"] == password: return True
    return False

def createAccount(email, password, name, address):
    newCustomer = Customer(
        email=email,
        password=password,
        customerId=str(uuid.uuid5(uuid.NAMESPACE_DNS, email)),
        name=name,
        address=address,
        orders=[]
    )

    writeToFile(newCustomer)

    return newCustomer

def getAccount(email, password):
    data = getFileContents()
    for user in data:
        if user["email"] == email and user["password"] == password: 
            return Customer(
                email=user["email"],
                password=user["password"],
                customerId=user["customerId"],
                name=user["name"],
                address=user["address"],
                orders=user["orders"]
            )