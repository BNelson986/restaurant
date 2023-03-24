import mysql.connector
import random
import datetime

#   Parameters for random date generation
startDate = datetime.date(2020, 1, 1)
endDate = datetime.date(2023,3, 22)

delta = endDate - startDate


'''                             Orders Table Columns
    Order ID   |   Customer ID   |   Order Date   |   Order Details   |   Order Total   
'''

#   Create connection to database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='restaurant'
)

#   Create cursor object
cursor = conn.cursor()

#   SAME CUSTOMER CAN HAVE MULTIPLE ORDERS

#   ORDER CAN INCLUDE MULTIPLE ITEMS AND DUPLICATES

#   customerID = random customer
#   orderDate = random date
#   items = random item + random quantity
#   orderDetails = "QTY1 x item1, QTY2 x item2, QTYn x itemn" 
#   orderTotal = (QTY1 x price1) + (QTY2 x price2) + ... + (QTYn x itemn)


#   CUSTOMER INDEX : 1 <= x <= 10000

#   ITEM INDEX : 1 <= x <= 14

#   ONLY USE TO RESET TABLE
#*********************************************

#   Reset auto-incrementing key
query = "ALTER TABLE orders AUTO_INCREMENT = 0"
cursor.execute(query)

query = "TRUNCATE TABLE orders"
cursor.execute(query)

#*********************************************

for order in range(1, 10000):
    #   Generate random Customer ID
    custID = random.randint(1, 10000)

    #   Generate random Order Date
    orderDate = startDate + datetime.timedelta(days=random.randrange(delta.days))
    print(orderDate)
    #   Create empty orderTotal variable
    orderTotal: float = 0.00

    #   Create list to store ordered items
    orderItems = []
    for items in range(1, random.randint(2, 10)):
        item = random.randint(1, 14)
        qty = random.randint(1, 6)

        #   Traverse list to find duplicate Items, if found increment qty by qty
        for i, row in enumerate(orderItems):
            if row[0] == item:
                orderItems[i] = (row[0], row[1] + qty)
                break
        else:
            orderItems.append((item, qty))

    #   Find all items in database and calculate total and details
    orderDetails = ""
    for row in orderItems:
        #   Execute a query to find the name of the item
        query = f"SELECT item_name, item_price FROM menu WHERE item_id = {row[0]}"
        cursor.execute(query)
        queriedItem = cursor.fetchone()
        itemName, itemPrice = queriedItem

        orderTotal += (row[1] * itemPrice)

        orderDetails += f"{row[1]} x {itemName}, "

    #   Query to insert each order into table
    insertQuery = f"INSERT INTO orders(customer_id, order_date, order_details, order_total)\
                    VALUES ('{custID}', '{orderDate}', '{orderDetails}', '{orderTotal}')"

    cursor.execute(insertQuery)

#   Query all inserted items for verification before commiting changes
checkQuery = "SELECT * FROM orders"
cursor.execute(checkQuery)

data = cursor.fetchall()

for row in data:
    print(row)

#   Ask for user confirmation before commiting changes
isGood = bool(input("Does everything appear in order? (1 = Yes, 0 = No)"))
if isGood:
    conn.commit()
    
