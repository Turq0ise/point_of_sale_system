class MenuItem:
    def __init__(self, item_num, name, price):
        self.item_num = item_num
        self.name = name
        self.price = price

class Menu:
    def __init__(self):
        self.items = [
            MenuItem(1, "Cheeseburger Meal", 166.00),
            MenuItem(2, "10Pc Nuggets", 199.00),
            MenuItem(3, "1Pc Chicken ", 99.00),
            MenuItem(4, "French Fries", 95.00),
            MenuItem(5, "Spaghetti", 110.00),
        ]

    def display_menu(self):
        print("\n========== FOOD MENU ==========")

        for item in self.items:
            print(f"{item.item_num}. {item.name} - ₱{item.price:.2f}")

menu = Menu()
menu.display_menu()
