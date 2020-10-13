import mysql.connector
import matplotlib.pyplot as plt 
import numpy as np

my_database = mysql.connector.connect(
    port = "33066",
    user = "root",
    password = "password",
    database = "dev"
)


def read_db():
    my_cursor = my_database.cursor()
    my_query = "SELECT transaction.id as transaction_id, transaction.datetime, location.name as location, product.name, basket.quantity FROM transaction LEFT JOIN basket ON basket.transaction_id = transaction.id LEFT JOIN product ON basket.product_id = product.id LEFT JOIN location ON transaction.location_id = location.id GROUP BY transaction.id, basket.id"
    #got rid of distint 
    my_cursor.execute(my_query)
    result = my_cursor.fetchall()
    return result 

my_db = read_db()

def just_drink_names():
    drink_names = []
    for line in my_db: 
        drink_names.append(line[3])
    return drink_names

every_drink = just_drink_names()
drink_names = set(every_drink)

def count_products_bought_1_day():
    count = {}
    for drink in drink_names:
        number_sold_of_type = every_drink.count(drink)
        count.update({f"{drink}": number_sold_of_type})
    return count

def count_dict_values(dictionary_name = dict):
    count = []
    for value in dictionary_name.values():
        count.append(value)
    return count


plt.rcdefaults()
fig, ax = plt.subplots()


#DATA
y_pos = np.arange(len(drink_names))
number_of_each_drink_sold = count_dict_values(count_products_bought_1_day())
number_sold_array = np.array(number_of_each_drink_sold)
error = np.random.rand(len(drink_names))

#this gives you a horizontal bar chart so y/vertical is the x axis (independent axis i.e. the once that does not depend on the other axis) and 
#the x axis is the y axis (the dependent variables - it's values depend on the other axis) 
ax.barh(y_pos, number_sold_array, xerr=error, align='center') 
ax.set_yticks(y_pos) #this says how many "sections"/bars/what the bars are
ax.set_yticklabels(drink_names) #this puts the names of the drinks from the drink types list on each of the vertical axis "sections"/bars
ax.invert_yaxis() # labels read top-to-bottom
ax.set_xlabel("Quantity Sold")
ax.set_title("Sale Volumes for Each Drink Type Inifity Works Cafe, Isle of Wight on 01/10/2020")

plt.show()
