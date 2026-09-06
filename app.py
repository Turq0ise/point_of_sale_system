from MODULES import customer_management
import payment_delivery
import menu
import Order

loginInput = int(input("Food Delivery POS\n[1] Login\n[2] Sign Up\n: "))

if loginInput == 1:
    print("Login")
    email = input("Email: ")
    password = input("Password: ")
    
    emailStatus = customer_management.checkIfEmailTaken(email)
    while(emailStatus == True):
        print("Email does not exist")
        break
        
    credentialsStatus = customer_management.checkUserCredentials(email, password)
    while(credentialsStatus == False):
        print("Email and password does not match")
        break

    currentUser = customer_management.getAccount(email, password)
    print("Logged in successfully:", currentUser)

elif loginInput == 2:
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
    print("Account created successfully!")

print("\n--- Proceeding to Menu & Order ---")

store_menu = menu.Menu()
store_menu.display_menu()

user_name = currentUser["name"] if isinstance(currentUser, dict) else currentUser.name
user_address = currentUser["address"] if isinstance(currentUser, dict) else currentUser.address

my_order = Order.Order(order_id="ORD-001", customer=user_name)
my_order.add_item("Cheeseburger Meal", 166.00, quantity=2)
my_order.display_order()

print("\n--- Proceeding to Payment & Delivery ---")
my_payment = payment_delivery.GCashPayment(my_order.total_amount, "09123456789")
my_delivery = payment_delivery.StandardDelivery(user_address)

my_payment.process_payment()
delivery_fee = my_delivery.calculate_fee()

print(f"Delivery Fee: ₱{delivery_fee:.2f}")
print(f"Total Amount Due: ₱{my_order.total_amount + delivery_fee:.2f}")

my_delivery.update_status("Dispatched")
my_delivery.track_order()
