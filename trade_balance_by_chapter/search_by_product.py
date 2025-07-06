import pandas as pd
import os

def search_by_product(product_name, data):
    search_data = data[data["Products"].str.contains(product_name.lower())]
    return search_data

data = pd.read_excel("import_data.xlsx")
product = input("Search a product: ")

print(search_by_product(product, data).head())
