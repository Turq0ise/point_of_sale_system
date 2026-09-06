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

menu_items = {
    1: ("Cheeseburger Meal", 166.00),
    2: ("10Pc Nuggets", 199.00),
    3: ("1Pc Chicken", 99.00),
    4: ("French Fries", 95.00),
    5: ("Spaghetti", 110.00)
}

while True:
    try:
        choice = int(input("\nEnter item number to order (1-5) or type 0 to finish: "))
        if choice == 0:
            break
        if choice in menu_items:
            item_name, item_price = menu_items[choice]
            qty = int(input(f"Enter quantity for {item_name}: "))
            my_order.add_item(item_name, item_price, quantity=qty)
            print(f"Added {qty}x {item_name} to your order.")
        else:
            print("Invalid item number. Please choose between 1 and 5.")
    except ValueError:
        print("Please enter a valid number.")

my_order.display_order()

print("\n--- Proceeding to Payment & Delivery ---")

print("Choose Payment Method:")
print("[1] GCash")
print("[2] Cash on Delivery (COD)")
pay_choice = int(input("Enter choice (1 or 2): "))

subtotal = my_order.total_amount

if pay_choice == 1:
    mobile = input("Enter your GCash mobile number: ")
    my_payment = payment_delivery.GCashPayment(subtotal, mobile)
else:
    my_payment = payment_delivery.CashOnDeliveryPayment(subtotal)

print("\nChoose Delivery Type:")
print("[1] Standard Delivery (₱50.00)")
print("[2] Express Delivery (₱120.00)")
del_choice = int(input("Enter choice (1 or 2): "))

if del_choice == 2:
    my_delivery = payment_delivery.ExpressDelivery(user_address)
else:
    my_delivery = payment_delivery.StandardDelivery(user_address)

my_payment.process_payment()
delivery_fee = my_delivery.calculate_fee()

print(f"\nSubtotal: ₱{subtotal:.2f}")
print(f"Delivery Fee: ₱{delivery_fee:.2f}")
print(f"Total Amount Due: ₱{subtotal + delivery_fee:.2f}")

my_delivery.update_status("Dispatched")
my_delivery.track_order()
