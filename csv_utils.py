import csv
import os
import requests
import io

"""
Find the value associated with a given key in a CSV reader object.

Parameters:
    key (str): The key to search for in the CSV reader.
    reader (csv.reader): The CSV reader object to search in.

Returns:
    str or None: The value associated with the key, or None if the key is not found.
"""
def find_value_from_key_in_reader(key, reader):
    for row in reader:
        # Check if the row has at least two elements
        if len(row) >= 2:
            # Check if the key matches the first element of the row
            if row[0] == key:
                # Return the associated value
                return row[1]

"""
Get the value associated with a given key from a CSV file or CSV content.

Parameters:
    key (str): The key to search for in the CSV file or content.
    csv_file_or_content (str or bytes): The path to the CSV file or the CSV content itself.

Returns:
    str or None: The value associated with the key, or None if the key is not found.
"""
def get_value_from_csv(key, csv_file_or_content):
    # Check if csv_file_or_content is a filename
    if isinstance(csv_file_or_content, str):
        # Open the CSV file in read mode
        with open(csv_file_or_content, "r") as file:
            reader = csv.reader(file)
            # Iterate over the rows in the CSV file
            return find_value_from_key_in_reader(key, reader)
    # Check if csv_file_or_content is CSV content
    elif isinstance(csv_file_or_content, bytes):
        # Create a StringIO object from the CSV content
        csv_content = io.StringIO(csv_file_or_content.decode("utf-8"))
        reader = csv.reader(csv_content)
        # Iterate over the rows in the CSV content
        return find_value_from_key_in_reader(key, reader)
    
    # If the key is not found, return None
    return None

"""
Writes a key-value pair to a CSV file. If the key already exists in the file,
the corresponding value is updated. If the key does not exist, a new line is
appended to the file.

:param key: The key to be written or updated in the CSV file.
:type key: str
:param value: The value to be associated with the key.
:type value: str
:return: None
"""
def write_to_csv(key, value):
   # Define the file path
    file_path = "file.csv"

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file
        open(file_path, "w").close()

    # Open the CSV file in read and write mode
    with open(file_path, "r+") as file:
        reader = csv.reader(file)
        lines = list(reader)

        # Find the line with the matching key
        for i, line in enumerate(lines):
            if line[0] == key:
                # Overwrite the value in that line
                lines[i][1] = value
                break
        else:
            # If the key is not found, append a new line
            lines.append([key, value])

        # Rewind the file pointer to the beginning
        file.seek(0)
        # Truncate the file
        file.truncate()

        # Write the updated lines back to the file
        writer = csv.writer(file)
        writer.writerows(lines)

"""
Downloads a CSV file from the given URL and returns its content as bytes.

Parameters:
    url (str): The URL of the CSV file to download.
    
Returns:
    bytes or False: The content of the downloaded CSV file as bytes, or False if the download fails.
"""
def download_csv(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the content of the response
        return response.content
    else:
        # Return False if the download fails
        return False

"""
Retrieves the value associated with a given key from either a local CSV file or a remote CSV file.

Args:
    key (str): The key to search for in the CSV file.
    csv_file (str): The path to the local CSV file.
    remote_url (str): The URL of the remote CSV file.

Returns:
    str or None: The value associated with the key, or None if the key is not found in either the local or remote CSV file.

This function first checks if the key exists in the local CSV file. If it does, the value associated with the key is returned. If the key is not found in the local CSV file, the function downloads the remote CSV file from the specified URL. It then searches for the key-value pair in the downloaded CSV file. If the key is found, the value is inserted into the local CSV file and returned. If the key is not found in either the local or remote CSV file, None is returned.

Note:
    This function assumes that the local CSV file and the remote CSV file have the same structure and contain the same keys.
"""
def get_value_from_csv_or_remote(key, csv_file, remote_url):
    # Check if the key exists in the local CSV file
    value = get_value_from_csv(key, csv_file)
    if value is not None:
        print("value is local.")
        return value

    # If the key does not exist in the local CSV file, download the CSV from the URL
    csv_content = download_csv(remote_url)
    if csv_content:
        # Find the key value pair from the downloaded CSV
        value = get_value_from_csv(key, csv_content)
        if value is not None:
            # Insert the key value pair into the local CSV file
            insert_into_local_csv(key, value, csv_file)
            print("value is remote, inserted into local.")
            return value

    # If the key is not found, return None
    print("value not found.")
    return None

"""
Insert a key-value pair into a local CSV file.

Args:
    key (str): The key to be inserted.
    value (str): The value associated with the key.
    csv_file (str): The path to the local CSV file.

Returns:
    None

This function opens the local CSV file in append mode and writes the key-value pair to the file. The key and value are written as a row in the CSV file.

Example:
    insert_into_local_csv("name", "John Doe", "data.csv")
"""
def insert_into_local_csv(key, value, csv_file):
    # Open the local CSV file in append mode
    with open(csv_file, "a") as file:
        writer = csv.writer(file)
        # Write the key value pair to the CSV file
        writer.writerow([key, value])
