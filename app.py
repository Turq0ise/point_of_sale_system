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
        self.current_page = "landing"
        self.running = True

        self.pages = {
            "landing": self.page_landing,
            "login": self.page_login,
            "sign-up": self.page_signup,
            "dashboard": self.page_dashboard,
            "order": self.page_order,
            "history": self.page_history
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

        self.currentUser = customer_management.createAccount(email, password, name, address)
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

    def page_history(self):
        titlePrint("History")


if __name__ == "__main__":
    app = App()
    app.run()
    print("\nThank You and Goodbye!")