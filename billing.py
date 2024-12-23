import csv
from datetime import datetime

def display_menu():
    print(f"{35*'*'} GOSSIP STATION MENU {35*'*'}")
    print("\n")
    try:
        with open("menu.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                item_code = row[0]
                item_name = row[1]
                item_price = row[2]
                print(f"{item_code:<4}  {item_name:<30}  RS.{item_price:<7}")
    except FileNotFoundError:
        print("No menu available")
def display_topping_menu():
    print(f"What toppings would you like to add? Enter the item code: ")
    try:
        with open("topping_menu.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                item_code = row[0]
                item_name = row[1]
                item_price = row[2]
                print(f"{item_code:<4}  {item_name:<30}  RS.{item_price:<7}")
    except FileNotFoundError:
        print("No menu available")

def generate_invoice(items):
    print("\nGenerating invoice...\n")
    subtotal_amount = 0
    print(f"{20*'='} INVOICE {20*'='}")

    current_datetime = datetime.now()
    invoice_id = f"{current_datetime.strftime('%M%S')}"
    print(f"Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Invoice ID: {invoice_id}\n")
    print(f"{49*'-'}")
    
    for item in items:
        item_code, item_name, item_price = item
        print(f"{item_name:<30}  RS.{item_price:<7}")
        subtotal_amount += float(item_price)

    service_charge = round(subtotal_amount * 0.10,2)
    VAT =  round(subtotal_amount * 0.13,2)
    total_amount = round((subtotal_amount + service_charge + VAT),2)

    print(f"{49*'-'}")
    print(f"{'Subtotal':<30} RS.{subtotal_amount:<7.2f}")
    print(f"{'Service Charge (10%)':<30} RS.{service_charge:<7.2f}")
    print(f"{'VAT (13%)':<30} RS.{VAT:<7.2f}")
    print(f"{49*'='}")
    print(f"{'Total Amount':<30} RS.{total_amount:<7.2f}")
    print(f"{49*'='}\n")
    print("Thank you for your purchase!\n")

    with open("report.csv", mode="a", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([invoice_id, current_datetime.strftime('%Y-%m-%d %H:%M:%S'),subtotal_amount,service_charge,VAT,total_amount])
    
    with open("Inventory.csv", mode="a") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([invoice_id,])

def display_report():
    try:
        with open("report.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            print(f"{35*'='} DAILY SALES REPORT {35*'='}")
            print("\n")
            for row in csv_reader:
                invoice_id, date, subtotal, service_charge, VAT, total_amount = row
                print(f"{invoice_id:<10} {date:<20} {subtotal:>10} {service_charge:>18} {VAT:>12} {total_amount:>13}")
    except FileNotFoundError:
        print("No report available")
    

def order_placement():
    items = []
    while True:
        try:
            item_id = input("Enter item id you want to add to basket (or 'Enter' to finish): ")
            if item_id == "":
                break
            with open("menu.csv", mode="r") as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row[0] == item_id:
                        items.append(row)
                        print(f"Added {row[1]} to the basket.")
            topping_id = input("Do you want to add any toppings (Y/N)? ")
            if topping_id.upper() == "Y":
                display_topping_menu()
                topping_id = input("Enter topping id: ")
                with open("topping_menu.csv", mode="r") as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if row[0] == topping_id:
                            items.append(row)
                            print(f"Added {row[1]} to the basket.")
        except ValueError:
            print("Invalid input. Please enter a valid item id.")
    return items

def admin_menu():
    print("Admin Menu:")
    print("1. Add item to menu")
    print("2. Remove item from menu")
    choice = input("Please select an option: ")
    if choice == "1":
        item_code = input("Enter item code: ")
        item_name = input("Enter item name: ")
        item_price = input("Enter item price: ")
        with open("menu.csv", mode="a", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([item_code, item_name, item_price])
        print(f"Added {item_name} to the menu.")
    elif choice == "2":
        item_code = input("Enter item code to remove: ")
        items = []
        with open("menu.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            items = [row for row in csv_reader if row[0] != item_code]
        with open("menu.csv", mode="w", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(items)
        print(f"Removed item with code {item_code} from the menu.")
    else:
        print("Invalid choice. Returning to main menu.")

def main():
    print("Gossip Station Billing System.")
    print("\n")
    print("1. Generate invoice")
    print("2. Go to Admin Panel")
    print("3. Exit")
    print("\n")
    while True:
        choice = input("Please select an option from the menu: ")
        try:
            if choice == "1":
                display_menu()
                items = order_placement()
                generate_invoice(items)
                break
            elif choice == "2":
                print("Gossip Station Billing System. [ADMIN PANEL]")
                print("\n")
                print("1. View Sales Report")
                print("2. Viewz Inventory Report")
                print("3. Exit")
                print("\n")
                while True:
                    admin_choice = input("Please select an option from the menu: ")
                    if admin_choice == "1":
                        display_report()
                    elif admin_choice == "2":
                        print("Inventory Report")
                    elif admin_choice == "3":
                        print("Exiting the system. Goodbye!")
                        exit()
                    else:
                        print("Invalid choice. Please select a valid option.")

            elif choice == "3":
                print("Exiting the system. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid choice. Please select a valid option from the menu.")

main()