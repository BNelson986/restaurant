import mysql.connector
import datetime
import time
import os

#   GOALS
#   1. WRITE TO FILE ALL MENU ITEMS AND THEIR PRICES
#   2. WRITE TO FILE ALL CUSTOMER ORDERS AND THEIR CONTENT
#   3. RETURN THE TOTAL REVENUE GENERATED ON A CERTAIN DAY
#   4. WRITE TO FILE LIST OF ALL MENU ITEMS AND QUANTITIES NEEDED TO FULFILL ALL ORDERS


#   Establish connection
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'restaurant'
)

cursor = conn.cursor()


#   1. WRITE TO FILE ALL MENU ITEMS AND PRICES
#   Gather all data from menu 
table_name = "menu"
query = f"SELECT * FROM {table_name}"
cursor.execute(query)

results = cursor.fetchall()

#   Open file to write into
with open(f"{table_name}.txt", 'w') as file:
    for row in results:
        file.write(f"{row}\n")


#   2. WRITE TO FILE ALL CUSTOMER ORDERS AND THEIR CONTENT
#   Gather all data from menu 
table_name = "orders"
query = f"SELECT * FROM {table_name}"
cursor.execute(query)

results = cursor.fetchall()

#   Open file to write into
with open(f"{table_name}.txt", 'w') as file:
    for row in results:
        file.write(f"{row}\n")


#   3. RETURN THE TOTAL REVENUE GENERATED ON A CERTAIN DAY

#   Function for takinguser input and verifying that it falls within specified ranges
def dateEntry():
    #   For LINUX users
    os.system("clear")

    #   For WINDOWS users
    #os.system("cls")

    date = input("Please choose a date you want to see the revenue from: (YYYY-MM-DD) \n") 

    if date < "2022-1-1" or date > "2023-3-22":
        print("Store was not open for that date, please try again.")
        time.sleep(2)
        dateEntry()
    else:
        return date


table_name = "orders"
col_name = "order_total"

again:bool = True
while again:

    userDate = dateEntry()

    query = f"SELECT SUM({col_name}) FROM {table_name} WHERE order_date = '{userDate}'"
    cursor.execute(query)
    total_revenue = cursor.fetchone()
    total_revenue = str(total_revenue)
    total_revenue = total_revenue.replace(",", "")
    total_revenue = total_revenue.replace("(", "")
    total_revenue = total_revenue.replace(")", "")

    print(f"Total Revenue on {userDate} was: ${total_revenue}")
    check = input("Would you like to check another date? (1 = Yes)\n")
    if check == '1':
        again = True
    else:
        again = False
        print("Ok, Thank you")

    cursor.reset()
    


#   4. WRITE TO FILE LIST OF ALL MENU ITEMS AND QUANTITIES NEEDED TO FULFILL ALL ORDERS

#   Return all rows from the 'order_details' column of the orders table
table_name = "orders"
col_name = "order_details"
query = f"SELECT {col_name} FROM {table_name}"
cursor.execute(query)

list_of_orders = cursor.fetchall()

#   Create a list of items and quantity from the menu query earlier
query = "SELECT item_name FROM menu"
cursor.execute(query)
menuItems = cursor.fetchall()
items = []
for row in menuItems:
    qty = 0
    row = str(row)
    row = row.replace("(", "")
    row = row.replace(")", "")
    row = row.replace(",", "")
    row = row.replace("'", "")
    items.append((row, qty))

#   Traverse list of orders, split into individual items and quantities
#   Add quantities to correct row of 'items'
for row in list_of_orders:
    row = str(row)
    orderItems = row.split(", ")
    orderItems.remove("',)")

    #   Traverse orderItems to split again and use quantity and name
    for item in orderItems:
        quantity, itemName = item.split(" x ")
        #   Convert to int for math operations
        quantity = quantity.replace("(", "")
        quantity = quantity.replace("'", "")
        quantity = int(quantity)

        #   Search results for a name match and increase qty by amount used in the order
        for i, ITEM in enumerate(items):
            if ITEM[0] == itemName:
                items[i] = (ITEM[0], ITEM[1] + quantity)
                break


with open("item_totals.txt", "w") as file:
    for row in items:
        file.write(f"The {row[0]} was orderd: {row[1]} times. \n")
