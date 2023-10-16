import pandas as pd
import os

file_path = "./../../Download/voucher"
# df = pd.read_excel(file_path)

# if "871323584567" in df["Mã Voucher"].values:
#     print("true................................................................")
#
#
# # Now, you can work with the selected column data.
# for column in range(len(df["Mã Voucher"])):
#     print(df["Mã Voucher"][column])


def is_valid_file_path(path):
    return os.path.exists(path)


def is_excel_file(file_path):
    if not is_valid_file_path(file_path):
        print("Not a file")
        return False
    # Get the file extension from the path
    file_extension = os.path.splitext(file_path)[1]

    # Check if the file extension is for Excel files
    if file_extension.lower() in (".xlsx", ".xls"):
        return True
    else:
        return False


print(is_excel_file(file_path))