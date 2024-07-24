import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb://mongoadmin:mongoadmin@localhost:27017/?authSource=admin")
db = client["test_ttb"]

orders = list(db.orders.find())
products = list(db.products.find())

df_orders = pd.DataFrame(orders)
df_products = pd.DataFrame(products)

result = pd.merge(df_orders, df_products, on='Product_Id')
result['Summary_price'] = result['numberOfOrders'].astype(int) * result['Price'].astype(float)

output_file_path = '/Users/napatsineepuangbubpa/ttb_test/data/Output_Bill.txt'

with open(output_file_path, 'w') as file:

    file.write('H\tCustomer.Cust_ID\tOrder.Order_ID\tProduct.Product Name\tOrder.numberOfOrders\tSummary price\n')
    
    for index, row in result.iterrows():
        file.write(f"D\t{row['Cust_ID']}\t{row['Order_ID']}\t{row['Product Name']}\t{row['numberOfOrders']}\t{row['Summary_price']:.2f}\n")
    
    total_lines = len(result)
    file.write(f"T\t{total_lines}\n")
    file.write(f"T\t{total_lines + 1}\n")

for index, row in result.iterrows():
    db.products.update_one(
        {"Product_Id": row['Product_Id']},
        {"$inc": {"Stock Quantity": -int(row['numberOfOrders'])}}
    )
