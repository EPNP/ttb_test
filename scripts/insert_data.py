import pymongo
import pandas as pd

client = pymongo.MongoClient(
    "mongodb://mongoadmin:mongoadmin@localhost:27017/?authSource=admin"
)
db = client["test_ttb"]


def insert_data_to_mongodb(file_path, collection_name):
    with open(file_path, "r") as file:
        lines = file.readlines()

    header = None
    data_lines = []

    for line in lines:
        line = line.strip()
        if line.startswith("H"):
            header = line.split("|")[1:]
        elif line.startswith("D"):

            if line.startswith("D|T|"):
                continue

            data_values = line.split("|")[1:]

            if len(data_values) != len(header):
                num_expected_cols = len(header)
                data_values = data_values[:num_expected_cols]
                data_values += ["-"] * (num_expected_cols - len(data_values))

            processed_values = []
            for value in data_values:
                value = value.strip()
                if value.lower() == "nan" or value == "":
                    processed_values.append("-")
                else:
                    try:

                        processed_values.append(float(value))
                    except ValueError:

                        processed_values.append(value)

            data_lines.append(processed_values)
        elif line.startswith("T"):
            continue

    df = pd.DataFrame(data_lines, columns=header)

    data_dicts = df.to_dict(orient="records")

    collection = db[collection_name]
    collection.drop()
    collection.insert_many(data_dicts)
    print(f"Inserted {len(data_dicts)} documents into {collection_name} collection.")


insert_data_to_mongodb(
    "/Users/napatsineepuangbubpa/ttb_test/data/Input_Customer.txt", "customers"
)
insert_data_to_mongodb(
    "/Users/napatsineepuangbubpa/ttb_test/data/Input_Order.txt", "orders"
)
insert_data_to_mongodb(
    "/Users/napatsineepuangbubpa/ttb_test/data/Input_Product.txt", "products"
)
