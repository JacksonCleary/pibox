import os
from dotenv import load_dotenv
from csv_utils import get_value_from_csv_or_remote, write_to_csv, download_csv

load_dotenv()

REMOTE_CSV_LOCATION = os.getenv('REMOTE_CSV_LOCATION')

# Define the key and value to be updated
key = "key3"
value = "key 3 value"

# write_to_csv(key, value);

# read_value = get_value_from_csv(key)
# if read_value is not None:
#     print(f"The value for {key} is: {read_value}")
# else:
#     print("Key1 not found in the CSV file.")

url = REMOTE_CSV_LOCATION
# csv_content = download_csv(url)

# if csv_content:
#     value = get_value_from_csv("key1", csv_content)
#     if value is not None:
#         print(f"The value for key1 is: {value}")
#     else:
#         print("Key1 not found in the CSV content.")

csv_file = "file.csv"
value = get_value_from_csv_or_remote("key1", csv_file, url)
if value is not None:
    print(f"The value for key1 is: {value}")
else:
    print("Key1 not found.")