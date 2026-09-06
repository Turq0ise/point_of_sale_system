from MODULES import customer_management
import MODULES.payment_delivery as payment_delivery
import MODULES.menu_management as menu_management
import MODULES.order_processing as order_processing

def titlePrint(text):
    print("==============================")
    print(text)
    print("==============================")

class App:
    def __init__(self):
        self.current_user: customer_management.Customer | None = None
        self.current_order: order_processing.Order | None = None
        self.current_page = "landing"
        self.running = True

        self.pages = {
            "landing": self.page_landing,
            "login": self.page_login,
            "sign-up": self.page_signup,
            "dashboard": self.page_dashboard,
            "order": self.page_order,
            "history": self.page_history,
            "payment": self.page_payment
        }

    def clear_screen(self):
        print("\033[2J\033[H", end="", flush=True)

    def run(self):
        while self.running:
            self.clear_screen()
            page_handler = self.pages.get(self.current_page)

            if page_handler:
                self.current_page = page_handler()
            else:
                self.current_page = "landing"

    def page_landing(self):
        titlePrint("Delivery System POS")
        print("1. Login")
        print("2. Sign Up")
        print("0. Exit")

        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            return "login"
        elif choice == "2":
            return "sign-up"
        elif choice == "0":
            self.running = False
            return ""
        else:
            input("Invalid choice! Press Enter to retry...")
            return "landing"

    def page_login(self):
        titlePrint("Login")
        email = input("Email: ")
        password = input("Password: ")
        
        emailStatus = customer_management.checkIfEmailTaken(email)
        while(emailStatus == True):
            print("Email does not exist")
            print("1. Try Again")
            print("0 (or any other input). Go Back")
            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                return "login"
            else:
                return "landing"
            
        credentialsStatus = customer_management.checkUserCredentials(email, password)
        while(credentialsStatus == False):
            print("Email and password does not match")
            print("1. Try Again")
            print("0 (or any other input). Go Back")
            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                return "login"
            else:
                return "landing"
    
        self.current_user = customer_management.getAccount(email, password)
        return "dashboard"

    def page_signup(self):
        titlePrint("Sign Up")
        email = input("Email: ")
        password = input("Password: ")
        
        status = customer_management.checkIfEmailTaken(email)
        while(status == False):
            print("Email already used")
            print("1. Try Again")
            print("0 (or any other input). Go Back")
            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                return "sign-up"
            else:
                return "landing"
            
        name = input("Username: ")
        address = input("Address: ")

        self.current_user = customer_management.createAccount(email, password, name, address)
        return "dashboard"

    def page_dashboard(self):
        titlePrint(f"Welcome, {self.current_user.name}")
        print("1. New Order")
        print("2. View Orders")
        print("0. Exit")

        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            return "order"
        elif choice == "2":
            return "history"
        elif choice == "0":
            self.running = False
            return ""
        else:
            input("Invalid choice! Press Enter to retry...")
            return "dashboard"

    def page_order(self):
        titlePrint("Order")
        storeMenu = menu_management.Menu()
        storeMenu.display_menu()
        menu_items = [item for item in storeMenu.items]

        self.current_order = order_processing.Order(order_id="ORD-001", customer=self.current_user.name)
        while True:
            try:
                choice = int(input("\nEnter item number to order (1-5) or type 0 to finish: "))
                if choice == 0:
                    break
                if choice > 0 and choice <= 5:
                    choice = choice - 1
                    item_name = menu_items[choice].name
                    item_price = menu_items[choice].price
                    qty = int(input(f"Enter quantity for {item_name}: "))
                    self.current_order.add_item(item_name, item_price, quantity=qty)
                    print(f"Added {qty}x {item_name} to your order.")
                else:
                    print("Invalid item number. Please choose between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        self.current_order.display_order()
        self.current_user.orders.append(self.current_order.order_id)
        input("Press Enter to proceed to payment...")
        return "payment"

    def page_history(self):
        titlePrint("History")
        for order in self.current_user.orders:
            print(order)

        input("Press Enter to go back...")
        return "dashboard"

    def page_payment(self):
        titlePrint("Payment")
        print("Choose Payment Method:")
        print("[1] GCash")
        print("[2] Cash on Delivery (COD)")
        pay_choice = int(input("Enter choice (1 or 2): "))

        subtotal = self.current_order.total_amount

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
            my_delivery = payment_delivery.ExpressDelivery(self.current_user.address)
        else:
            my_delivery = payment_delivery.StandardDelivery(self.current_user.address)

        my_payment.process_payment()
        delivery_fee = my_delivery.calculate_fee()

        print(f"\nSubtotal: ₱{subtotal:.2f}")
        print(f"Delivery Fee: ₱{delivery_fee:.2f}")
        print(f"Total Amount Due: ₱{subtotal + delivery_fee:.2f}")

        my_delivery.update_status("Dispatched")
        my_delivery.track_order()

        customer_management.updateFile(self.current_user)

        return "dashboard"


if __name__ == "__main__":
    app = App()
    app.run()
    print("\nThank You and Goodbye!")