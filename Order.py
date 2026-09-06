class Order:
    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.items = []
        self.total_amount = 0

    def add_item(self, item_name, price, quantity):
        subtotal = price * quantity

        self.items.append({
            "name": item_name,
            "price": price,
            "quantity": quantity,
            "subtotal": subtotal
        })

        self.total_amount += subtotal

    def display_order(self):
        print("\nOrder Details: ")
        print("Order ID:", self.order_id)
        print("Customer:", self.customer)

        print("\nItems:")
        for item in self.items:
            print(
                item["name"],
                "x", item["quantity"],
                "= PHP", item["subtotal"]
            )

        print("\nTotal Amount: PHP", self.total_amount)
