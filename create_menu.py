import mysql.connector
import random


#   ONLY USE TO RESET TABLE
'''
#   Reset auto-incrementing key
query = "ALTER TABLE menu AUTO_INCREMENT = 0"
cursor.execute(query)

query = "TRUNCATE TABLE menu"
cursor.execute(query)
'''


#   Creation of menu items and prices
mainItems = (
    "14oz Dry-Aged New York Strip", "18oz Dry-Aged Ribeye", "22oz Bone-In Dry-Aged Porterhouse",
    "Dry-Aged Tomahawk Ribeye", "8oz Wagyu Filet Mignon", "12oz Wagyu Strip Loin",
    "Dry-Aged Beef Tartare", "Lobster Bisque",
    "Charred Octopus"
)
sideItems = ("Truffle Mashed Potatoes", "Creamed Spinach", "Creamed Corn", "Grilled Asparagus",
    "Roasted Mushrooms"
)

prices = (65.0, 85.0, 110.0, 175.0, 120.0, 145.0, 25.0, 18.0, 22.0, 12.0, 10.0, 12.0, 14.0, 16.0)

items = (mainItems + sideItems)

menu = tuple(zip(items, prices))

#   Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='restaurant'
)

#   Create cursor object
cursor = conn.cursor()

#   Generate Query to insert each item into the table
table_name = "menu"

for row in menu:
    item = row[0]
    price = row[1]
    query = f"INSERT INTO {table_name}(item_name, item_price) VALUES ('{item}', '{price}')"

    cursor.execute(query)

#   Print results to verify correct insertion
query = f"SELECT * FROM {table_name}"
cursor.execute(query)
results = cursor.fetchall()

for row in results:
    print(row)

#   Ask for user confirmation before commiting changes
isGood = bool(input("Does everything appear in order? (1 = Yes, 0 = No)"))
if isGood:
    conn.commit()
    



