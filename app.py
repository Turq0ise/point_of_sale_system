from MODULES import customer_management

loginInput = int(input("Food Delivery POS\n[1] Login\n[2] Sign Up\n: "))
if loginInput == 1:
    # login
    print("Login")
    email = input("Email: ")
    password = input("Password: ")
    emailStatus = customer_management.checkIfEmailTaken(email)
    while(emailStatus == True):
        print("Email does not exist")
        break
        # sa ui na ayusin
    credentialsStatus = customer_management.checkUserCredentials(email, password)
    while(credentialsStatus == False):
        print("Email and password does not match")
        break
        # sa ui na ayusin

    currentUser = customer_management.getAccount(email, password)
    print(currentUser)
elif loginInput == 2:
    # sign up
    # sign up with customer details > check accounts.json for existing account >  ask for name and address
    print("Sign Up")
    email = input("Email: ")
    password = input("Password: ")
    status = customer_management.checkIfEmailTaken(email)
    while(status == False):
        print("Email already used, please try again")
        email = input("Email: ")
        password = input("Password: ")
    name = input("Username: ")
    address = input("Address: ")

    currentUser = customer_management.createAccount(email, password, name, address)