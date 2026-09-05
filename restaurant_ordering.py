import csv
import os


ORDER_FILE = "orders.csv"


class MenuItem:
    """Represent one item available in the restaurant menu."""

    def __init__(
        self,
        item_id: int,
        name: str,
        category: str,
        price: float
    ) -> None:
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price

    def display(self) -> None:
        """Display the details of the menu item."""
        print(
            f"{self.item_id:<5}"
            f"{self.name:<25}"
            f"{self.category:<15}"
            f"₹{self.price:.2f}"
        )


class Order:
    """Manage the customer's shopping cart and order."""

    TAX_RATE = 0.05
    DISCOUNT_THRESHOLD = 500
    
    def __init__(self) -> None:
        self.__items = []
        self.order_id = None
        self.status = "Pending"

    def add_item(self, item: MenuItem, quantity: int) -> None:
        """Add a menu item and quantity to the cart."""
        for cart_item in self.__items:
            if cart_item["item"].item_id == item.item_id:
                cart_item["quantity"] += quantity
                print(f"{item.name} quantity updated in cart.")
                return

        self.__items.append(
            {
                "item": item,
                "quantity": quantity
            }
        )

        print(f"{quantity} x {item.name} added to cart.")

    def remove_item(self, item_id: int) -> bool:
        """Remove an item from the cart using its ID."""
        for cart_item in self.__items:
            if cart_item["item"].item_id == item_id:
                self.__items.remove(cart_item)
                return True

        return False

    def calculate_subtotal(self) -> float:
        """Calculate the subtotal of all cart items."""
        total = 0.0

        for cart_item in self.__items:
            item = cart_item["item"]
            quantity = cart_item["quantity"]
            total += item.price * quantity

        return total

    def calculate_discount(self) -> float:
        """Calculate a 10 percent discount for orders of ₹500 or more."""
        subtotal = self.calculate_subtotal()

        if subtotal >= self.DISCOUNT_THRESHOLD:
            return subtotal * 0.10

        return 0.0

    def calculate_tax(self) -> float:
        """Calculate 5 percent tax after applying the discount."""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        taxable_amount = subtotal - discount

        return taxable_amount * self.TAX_RATE

    def calculate_total(self) -> float:
        """Calculate the final amount including tax and discount."""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        tax = self.calculate_tax()

        return subtotal - discount + tax

    def display_cart(self) -> None:
        """Display all items currently in the cart."""
        if not self.__items:
            print("\nYour cart is empty.")
            return

        print("\n" + "=" * 60)
        print("YOUR CART")
        print("=" * 60)

        for cart_item in self.__items:
            item = cart_item["item"]
            quantity = cart_item["quantity"]
            total = item.price * quantity

            print(
                f"{item.name:<25}"
                f"x {quantity:<5}"
                f"₹{total:.2f}"
            )

        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        tax = self.calculate_tax()
        total = self.calculate_total()

        print("-" * 60)
        print(f"{'Subtotal:':<45} ₹{subtotal:.2f}")
        print(f"{'Discount:':<45} ₹{discount:.2f}")
        print(f"{'Tax:':<45} ₹{tax:.2f}")
        print(f"{'Final Total:':<45} ₹{total:.2f}")

    def is_empty(self) -> bool:
        """Return True if the cart contains no items."""
        return len(self.__items) == 0

    def place_order(self) -> float:
        """Mark the order as completed and return its total."""
        if self.is_empty():
            return 0.0

        self.status = "Completed"
        return self.calculate_total()

    def get_items(self) -> list:
        """Return the items in the cart."""
        return self.__items


class Restaurant:
    """Manage the restaurant menu and order history."""

    TAX_RATE = 0.05
    DISCOUNT_THRESHOLD = 500

    restaurant_name = "Foodie's Corner"

    def __init__(self) -> None:
        self.menu = []
        self.orders = []
        self.next_order_id = 1001

        self.load_menu()
        self.initialize_order_file()

    def load_menu(self) -> None:
        """Create the restaurant menu using MenuItem objects."""
        self.menu = [
            MenuItem(
                1,
                "Veg Burger",
                "Main Course",
                150.00
            ),
            MenuItem(
                2,
                "Chicken Burger",
                "Main Course",
                200.00
            ),
            MenuItem(
                3,
                "Margherita Pizza",
                "Main Course",
                250.00
            ),
            MenuItem(
                4,
                "French Fries",
                "Starters",
                100.00
            ),
            MenuItem(
                5,
                "Chicken Wings",
                "Starters",
                180.00
            ),
            MenuItem(
                6,
                "Coke",
                "Beverages",
                50.00
            ),
            MenuItem(
                7,
                "Fresh Lime",
                "Beverages",
                70.00
            ),
            MenuItem(
                8,
                "Chocolate Cake",
                "Desserts",
                120.00
            )
        ]

    def initialize_order_file(self) -> None:
        """Create the CSV file with a header if needed."""
        if not os.path.exists(ORDER_FILE):
            try:
                with open(
                    ORDER_FILE,
                    "w",
                    newline="",
                    encoding="utf-8"
                ) as file:
                    writer = csv.writer(file)

                    writer.writerow(
                        [
                            "order_id",
                            "item_name",
                            "category",
                            "quantity",
                            "amount",
                            "status"
                        ]
                    )

            except PermissionError:
                print(
                    "Error: Permission denied while creating "
                    "the order file."
                )

    def display_menu(self) -> None:
        """Display all food items in the restaurant menu."""
        print("\n" + "=" * 60)
        print(self.restaurant_name.upper())
        print("RESTAURANT MENU")
        print("=" * 60)

        print(
            f"{'ID':<5}"
            f"{'Food':<25}"
            f"{'Category':<15}"
            f"Price"
        )

        print("-" * 60)

        for item in self.menu:
            item.display()

    def find_item(self, item_id: int) -> MenuItem | None:
        """Find a menu item using its ID."""
        for item in self.menu:
            if item.item_id == item_id:
                return item

        return None

    def search_food(self) -> None:
        """Search for food items by name."""
        keyword = input(
            "\nEnter food name to search: "
        ).strip().lower()

        if not keyword:
            print("Search term cannot be empty.")
            return

        found = False

        print("\nSearch Results")
        print("-" * 60)

        for item in self.menu:
            if keyword in item.name.lower():
                item.display()
                found = True

        if not found:
            print("No matching food item found.")

    def show_categories(self) -> None:
        """Display all unique food categories."""
        categories = set()

        for item in self.menu:
            categories.add(item.category)

        print("\nAvailable Categories:")

        for number, category in enumerate(
            sorted(categories),
            start=1
        ):
            print(f"{number}. {category}")

    def show_category_items(self) -> None:
        """Display food items belonging to a selected category."""
        self.show_categories()

        category = input(
            "\nEnter category name: "
        ).strip().lower()

        found = False

        print("\nCategory Items")
        print("-" * 60)

        for item in self.menu:
            if item.category.lower() == category:
                item.display()
                found = True

        if not found:
            print("Category not found.")

    def get_positive_integer(self, message: str) -> int:
        """Read and validate a positive integer."""
        while True:
            try:
                value = int(input(message))

                if value <= 0:
                    print("Please enter a number greater than 0.")
                    continue

                return value

            except ValueError:
                print("Invalid input. Please enter a whole number.")

    def add_to_cart(self, order: Order) -> None:
        """Ask for an item and quantity and add it to the cart."""
        self.display_menu()

        item_id = self.get_positive_integer(
            "\nEnter item ID: "
        )

        item = self.find_item(item_id)

        if item is None:
            print("Invalid item ID.")
            return

        quantity = self.get_positive_integer(
            "Enter quantity: "
        )

        order.add_item(item, quantity)

    def remove_from_cart(self, order: Order) -> None:
        """Remove a selected item from the cart."""
        if order.is_empty():
            print("\nYour cart is empty.")
            return

        order.display_cart()

        item_id = self.get_positive_integer(
            "\nEnter item ID to remove: "
        )

        if order.remove_item(item_id):
            print("Item removed from cart.")
        else:
            print("Item not found in cart.")

    def save_order(self, order: Order) -> None:
        """Save the completed order to the CSV file."""
        try:
            with open(
                ORDER_FILE,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)

                for cart_item in order.get_items():
                    item = cart_item["item"]
                    quantity = cart_item["quantity"]
                    amount = item.price * quantity

                    writer.writerow(
                        [
                            order.order_id,
                            item.name,
                            item.category,
                            quantity,
                            f"{amount:.2f}",
                            order.status
                        ]
                    )

        except PermissionError:
            print(
                "Error: Permission denied while saving "
                "the order."
            )

    def place_order(self, order: Order) -> None:
        """Complete the current order and save it to the CSV file."""
        if order.is_empty():
            print("\nCannot place an empty order.")
            return

        order.order_id = self.next_order_id
        total = order.place_order()

        self.save_order(order)
        self.orders.append(order)
        self.next_order_id += 1

        print("\n" + "=" * 60)
        print("ORDER PLACED SUCCESSFULLY")
        print("=" * 60)
        print(f"Order ID: {order.order_id}")
        print(f"Total Amount: ₹{total:.2f}")
        print(f"Status: {order.status}")
        print(
            f"\nThank you for ordering from "
            f"{self.restaurant_name}!"
        )

    def view_order_history(self) -> None:
        """Display completed orders stored in the CSV file."""
        try:
            with open(
                ORDER_FILE,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:
                reader = csv.reader(file)

                # Skip the header
                next(reader, None)

                found = False

                print("\n" + "=" * 60)
                print("ORDER HISTORY")
                print("=" * 60)

                for row in reader:
                    if len(row) != 6:
                        continue

                    (
                        order_id,
                        item_name,
                        category,
                        quantity,
                        amount,
                        status
                    ) = row

                    print(
                        f"Order {order_id} | "
                        f"{item_name} | "
                        f"Qty: {quantity} | "
                        f"₹{amount} | "
                        f"{status}"
                    )

                    found = True

                if not found:
                    print("No previous orders found.")

        except FileNotFoundError:
            print("No order history file found.")

        except PermissionError:
            print(
                "Error: Permission denied while reading "
                "the order file."
            )


def display_menu_options() -> None:
    """Display the main application menu."""
    print("\n" + "=" * 60)
    print("FOODIE'S CORNER - RESTAURANT ORDERING SYSTEM")
    print("=" * 60)
    print("1. View Menu")
    print("2. Search Food")
    print("3. View Categories")
    print("4. View Category Items")
    print("5. Add Item to Cart")
    print("6. View Cart")
    print("7. Remove Item from Cart")
    print("8. Place Order")
    print("9. View Order History")
    print("10. Exit")


def main() -> None:
    """Run the Restaurant Ordering System."""
    restaurant = Restaurant()
    current_order = Order()

    while True:
        display_menu_options()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            restaurant.display_menu()

        elif choice == "2":
            restaurant.search_food()

        elif choice == "3":
            restaurant.show_categories()

        elif choice == "4":
            restaurant.show_category_items()

        elif choice == "5":
            restaurant.add_to_cart(current_order)

        elif choice == "6":
            current_order.display_cart()

        elif choice == "7":
            restaurant.remove_from_cart(current_order)

        elif choice == "8":
            restaurant.place_order(current_order)

            if current_order.is_empty():
                continue

            current_order = Order()

        elif choice == "9":
            restaurant.view_order_history()

        elif choice == "10":
            print("\nThank you! Goodbye.")
            break

        else:
            print(
                "Invalid choice. Please enter a number "
                "from 1 to 10."
            )


if __name__ == "__main__":
    main()