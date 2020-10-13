import matplotlib.pyplot as plt
import numpy as np
import json
from itertools import chain
from uuid import uuid4 as get_uuid
from src.extract import csv_import


def _remove_duplicate_products(li: list) -> list:
    dumped_set = set([json.dumps(d, sort_keys=True) for d in li])
    return [json.loads(s) for s in dumped_set]


def _basket(order: list) -> list:
    result = []
    for i in range(0, len(order), 3):
        product = {}

        if "-" in order[i + 1]:
            product_split = order[i + 1].split(" - ")
            product["Name"] = product_split[0]
            product["Flavour"] = product_split[1]
        else:
            product["Name"] = order[i + 1]
            product["Flavour"] = "NULL"

        product["Size"] = None if not order[i] else order[i]
        product["Price"] = float(order[i + 2])

        product["Iced"] = False
        for remove in ["Flavoured ", "Speciality ", "Iced "]:
            if remove in product["Name"]:
                product["Name"] = product["Name"].replace(remove, "").capitalize()
                if remove == "Iced ":
                    product["Iced"] = True

        result.append(product)

    return result


def _get_transactions() -> list:
    transactions = []  # Each transaction contains a basket

    # TODO Each row is a new transaction
    for row in csv_import:
        order = row["Orders"].split(",")
        basket = _basket(order)

        transactions.append(
            {
                "Transaction_ID": get_uuid(),
                "Basket": basket,
                "DateTime": row["Timestamp"],
                "Location": row["Location"],
            }
        )

    return transactions


def _get_unique_products(transactions: list) -> list:
    return [
        dict(d, **{"Product_ID": get_uuid()})
        for d in _remove_duplicate_products(
            list(chain.from_iterable([d["Basket"] for d in transactions]))
        )
    ]

    #all my extra code!
def get_info_items_bought():
    items = []
    for transaction in transactions:
        items.append(transaction["Basket"])
    return items

def names_only(information = list):
    names_list = []
    for line in information:
        index = 0
        while index != len(line):
            row = line[index]
            names_list.append(row["Name"])
            index += 1
    return names_list

def count_how_many_times_drink_bought(sales_information = list):
    drink_types = set(sales_information)
    count = {}
    for drink_type in drink_types:
        number_of_drinks_sold_of_type = sales_information.count(drink_type)
        count.update({f"{drink_type}": number_of_drinks_sold_of_type})
    return count

def count_values(sales_information = dict):
    count = []
    for value in sales_information.values():
        count.append(value)
    return count

def get_flavours(sales_information = list):
    flavour_list = []
    for line in sales_information:
        index = 0
        while index != len(line):
            row = line[index]
            flavour = row["Flavour"]
            if flavour != "NULL":
                flavour_list.append(row)
                index += 1
            else:
                index += 1
    return flavour_list

def get_flavoured_drink(flavours_information = list, drink_type = str):
    flavour_drink_type_list = []
    for line in flavours_information:
        if line["Name"] == drink_type:
            flavour_drink_type_list.append(line)
        else:
            pass
    return flavour_drink_type_list

def get_the_flavours_of_each_drink_type(list_of_flavs_1_drink_type = list):
    flavs_1_drink_type = []
    for line in list_of_flavs_1_drink_type:
        flavs_1_drink_type.append(line["Flavour"])
    return flavs_1_drink_type

def count_how_many_times_flavour_bought(sales_information = list):
    flavour_types = set(sales_information)
    count = {}
    for flavour_type in flavour_types:
        number_of_flavours_sold_of_type = sales_information.count(flavour_type)
        count.update({f"{flavour_type}": number_of_flavours_sold_of_type})
    return count

if __name__ == "__main__":
    transactions = _get_transactions()
    unique_products = _get_unique_products(transactions)

    print(f"Number of transactions: {len(transactions)}")
    print(
        f"Number of drinks ordered: {sum([len(transaction['Basket']) for transaction in transactions])}"
    )
    print(f"Number of unique products: {len(unique_products)}")

    # #
    # all_items = get_info_items_bought()
    # names_of_drinks = names_only(all_items)
    # #print(len(names_only(all_items)))
    # count = count_how_many_times_drink_bought(names_of_drinks)
    # flavours = get_flavours(all_items)
    # #print(flavours)
    # #print(len(flavours))
    # flavoured_lattes = get_flavoured_drink(flavours, "Latte")
    # latte_flavours = get_the_flavours_of_each_drink_type(flavoured_lattes)
    # #print(latte_flavours)
    # count_flav_lattes = count_how_many_times_flavour_bought(latte_flavours)
    # print(count_flav_lattes)
    # #print(flavoured_lattes)
    # #print(len(flavoured_lattes)
    # flavoured_teas = get_flavoured_drink(flavours, "Tea")
    # tea_flavours =get_the_flavours_of_each_drink_type(flavoured_teas)
    # #print(tea_flavours)
    # count_flav_teas = count_how_many_times_flavour_bought(tea_flavours)
    # print(count_flav_teas)
    # #print(flavoured_teas)
    # #print(len(flavoured_teas))
    # #print(count)
    flavoured_hot_chocolates = get_flavoured_drink(flavours, "Hot chocolate")


    # plt.rcdefaults()
    # fig, ax = plt.subplots()


    # # DATA
    # drink_types = set(names_of_drinks)
    # y_pos = np.arange(len(drink_types))
    # number_of_drinks_sold_each_type = count_values(count)
    # number_drinks_array = np.array(number_of_drinks_sold_each_type)
    # error = np.random.rand(len(drink_types))

    # #this gives you a horizontal bar chart so y/vertical is the x axis (independent axis i.e. the once that does not depend on the other axis) and 
    # #the x axis is the y axis (the dependent variables - it's values depend on the other axis) 
    # ax.barh(y_pos, number_drinks_array , xerr=error, align='center') 
    # ax.set_yticks(y_pos) #this says how many "sections"/bars/what the bars are
    # ax.set_yticklabels(drink_types) #this puts the names of the drinks from the drink types list on each of the vertical axis "sections"/bars
    # ax.invert_yaxis()  # labels read top-to-bottom
    # ax.set_xlabel("Quantity Sold")
    # ax.set_title("Sale Volumes for Each Type of Drink Sold at Inifity Works Isle of Wight on 01/10/2020")

    # plt.show()

all_items = get_info_items_bought()
names_of_drinks = names_only(all_items)
#print(len(names_only(all_items)))
count = count_how_many_times_drink_bought(names_of_drinks)
flavours = get_flavours(all_items)
#print(flavours)
#print(len(flavours))
flavoured_lattes = get_flavoured_drink(flavours, "Latte")
latte_flavours = get_the_flavours_of_each_drink_type(flavoured_lattes)
#print(latte_flavours)
count_flav_lattes = count_how_many_times_flavour_bought(latte_flavours)
print(count_flav_lattes)
#print(flavoured_lattes)
#print(len(flavoured_lattes)
flavoured_teas = get_flavoured_drink(flavours, "Tea")
tea_flavours =get_the_flavours_of_each_drink_type(flavoured_teas)
#print(tea_flavours)
count_flav_teas = count_how_many_times_flavour_bought(tea_flavours)
print(count_flav_teas)
#print(flavoured_teas)
#print(len(flavoured_teas))
#print(count)


plt.rcdefaults()
fig, ax = plt.subplots()

# # # DATA
# # flavours = set(latte_flavours)
# # y_pos = np.arange(len(flavours))
# # number_of_flavours_sold_each_type = count_values(count_flav_lattes)
# # number_flavours_array = np.array(number_of_flavours_sold_each_type)
# # error = np.random.rand(len(flavours))

# # #this gives you a horizontal bar chart so y/vertical is the x axis (independent axis i.e. the once that does not depend on the other axis) and 
# # #the x axis is the y axis (the dependent variables - it's values depend on the other axis) 
# # ax.barh(y_pos, number_flavours_array, xerr=error, align='center') 
# # ax.set_yticks(y_pos) #this says how many "sections"/bars/what the bars are
# # ax.set_yticklabels(flavours) #this puts the names of the drinks from the drink types list on each of the vertical axis "sections"/bars
# # ax.invert_yaxis()  # labels read top-to-bottom
# # ax.set_xlabel("Quantity Sold")
# # ax.set_title("Sale Volumes for Each Flavour of All Flavoured Lattes (Includes Hot and Iced) Sold at Inifity Works Isle of Wight on 01/10/2020")

# # plt.show()


# DATA
flavours = set(tea_flavours)
y_pos = np.arange(len(flavours))
number_of_flavours_sold_each_type = count_values(count_flav_teas)
number_flavours_array = np.array(number_of_flavours_sold_each_type)
error = np.random.rand(len(flavours))

#this gives you a horizontal bar chart so y/vertical is the x axis (independent axis i.e. the once that does not depend on the other axis) and 
#the x axis is the y axis (the dependent variables - it's values depend on the other axis) 
ax.barh(y_pos, number_flavours_array, xerr=error, align='center') 
ax.set_yticks(y_pos) #this says how many "sections"/bars/what the bars are
ax.set_yticklabels(flavours) #this puts the names of the drinks from the drink types list on each of the vertical axis "sections"/bars
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel("Quantity Sold")
ax.set_title("Sale Volumes for Each Flavour of All Flavoured Teas Sold at Inifity Works Isle of Wight on 01/10/2020")

plt.show()