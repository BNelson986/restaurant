import mysql.connector
import random
from faker import Faker

#****************************************************************
#   ONLY USE THESE LINES TO ERASE THE TABLE DATA!!!!!!!!!
'''
query = "ALTER TABLE customers AUTO_INCREMENT = 0"
cursor.execute(query)

query = "TRUNCATE TABLE customers"
cursor.execute(query)
'''
#****************************************************************

#   Open MySQL database
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'restaurant'
)

table_name = 'customers'


#   Create cursor object
cursor = conn.cursor()

#   Instantiate Faker object
fake = Faker()

#   Generate and store fake name, email, and address
firstName: str = ""
lastName: str = ""
email: str = ""
address: str = ""
person = (firstName, lastName, email, address)

customer = []

customer = set()

while len(customer) < 10000:
    name = fake.name()
    address = fake.address().replace('\n', ' ')


    #   Split names into components
    first_name, *last_name = name.split(maxsplit=1)

    #   Join any remaining last name components
    last_name = " ".join(last_name)


    #   Removes any prefixes and suffixes
    if first_name.startswith(('Mr.', 'Mrs.', 'Ms.')):
        first_name = first_name.split('.')[1]
    if last_name.endswith(('Jr.', 'Sr.', 'PHD', 'III', 'DDS', 'DVM', 'II')):
        last_name = last_name[:-3]

    rand = random.randrange(0,999)

    email = f"{first_name.lower()}.{last_name.lower()}{rand}@example.com"
    
    if (first_name, last_name) not in customer:
        customer.add((first_name, last_name, email, address))
    

#   Traverse customers adding each line to table
ind: int = 0
for row in customer:
    first_name = row[0]
    last_name = row[1]
    email = row[2]
    address = row[3]

    #   Add name to database
    query = f"INSERT INTO {table_name}(first_name, last_name, email, address) \
        VALUES ('{first_name}', '{last_name}', '{email}', '{address}')"
    cursor.execute(query)

#   Verify proper insertion before commiting
check = f"SELECT * FROM {table_name}"
cursor.execute(check)

data = cursor.fetchall()
print(data)

good = bool(input("Does this insertion look good? (1 = Yes, 0 = No)"))
if good:
    conn.commit()
else:
    exit()