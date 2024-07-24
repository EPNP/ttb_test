import pandas as pd


def convert_excel_to_txt(
    input_excel_file, sheet_name, output_txt_file, header_prefix, trailer_prefix
):

    df = pd.read_excel(input_excel_file, sheet_name=sheet_name, engine="openpyxl")

    with open(output_txt_file, "w") as txt_file:

        header = f"{header_prefix}|" + "|".join(df.columns)
        txt_file.write(header + "\n")

        for index, row in df.iterrows():
            data = f"D|{'|'.join(map(str, row))}"
            txt_file.write(data + "\n")

        trailer = f"{trailer_prefix}|{len(df)}"
        txt_file.write(trailer + "\n")


convert_excel_to_txt(
    "/Users/napatsineepuangbubpa/ttb_test/data/excel/Input_Customer.xlsx",
    "Sheet1",
    "/Users/napatsineepuangbubpa/ttb_test/data/Input_Customer.txt",
    "H",
    "T",
)
convert_excel_to_txt(
    "/Users/napatsineepuangbubpa/ttb_test/data/excel/Input_Order.xlsx",
    "Sheet1",
    "/Users/napatsineepuangbubpa/ttb_test/data/Input_Order.txt",
    "H",
    "T",
)
convert_excel_to_txt(
    "/Users/napatsineepuangbubpa/ttb_test/data/excel/Input_Product.xlsx",
    "Sheet1",
    "/Users/napatsineepuangbubpa/ttb_test/data/Input_Product.txt",
    "H",
    "T",
)
