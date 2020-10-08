import json
from uuid import uuid4 as get_uuid
from src.extract import csv_import

#print(csv_import)


# #'Timestamp': '2020-10-01 09:00:00', 'Location': 'Isle of Wight', 'Name': 'John Whitmire', 'Orders': ',Mocha,
# # #2.3,,Speciality Tea - Fruit,1.3,,Flavoured iced latte - Vanilla,2.75,,Frappes - Chocolate Cookie,2.75,Large,Filter coffee,1.8', 
# # #'Payment Type': 'CARD', 'Cost': 10.9, 'Card Details': 'americanexpress,379663269694145'} 

# return [
    #     dict(d, **{"Product_ID": get_uuid()})
    #     for d in _remove_duplicate_products(products)
    # ]


def _remove_duplicate_products(li: list) -> list:
    dumped_set = set([json.dumps(d, sort_keys=True) for d in li])
    return [json.loads(s) for s in dumped_set]


# def get_location_table():
#     location_dict = {}
#     for row in csv_import:
#         location_dict["Location_UUID"] = get_uuid()
#         location_dict["Location_Name"] = row["Location"]
#     return location_dict

# print(get_location_table())

def create_product_list() -> list:
    products = []
    for row in csv_import:
        order = row["Orders"].split(",")

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

            product["Iced"] = False
            for remove in ["Flavoured ", "Speciality ", "Iced "]:
                if remove in product["Name"]:
                    product["Name"] = product["Name"].replace(remove, "").capitalize()
                    if remove == "Iced ":
                        product["Iced"] = True

            products.append(product)

    return products

            
    return [
        dict(d, **{"Product_ID": get_uuid()})
        for d in _remove_duplicate_products(products)
    ]

if __name__ == "__main__":
    
    products = create_product_list()
    # for p in products:
    #     print(p)
    def make_basket():
        basket = {}
        baskets = []
        index = 0
        for row in csv_import:
            row = csv_import[index]
            order = row["Orders"].split(",")
            number_of_items = int(len(order)/3)
            basket["Basket_Number"] = index
            basket["Basket_Contents"] = order
            basket["Number_of_Items_In_Basket"] = number_of_items
            baskets.append(basket)
            index += 1
        return baskets

    print(make_basket())

    
    

    # ind = 0
    # ind_1 = my_basket[0].get("Number_of_Items_In_Basket")
    # print(ind_1)
    # ind_2 = 0
    # for line in my_basket:
    #     while ind_1<
        
  
                
        
    
        
        
        



    # products = create_product_list()
    # my_products = products[0]
    # for p in products(range(0,number_of_items,1)):
    #     print(p)






#print(num_items_order[3])

    #print(len(products))