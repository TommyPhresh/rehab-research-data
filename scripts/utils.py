
import sys
# The path to packages on the C: drive
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'

# Add the path to the Python system path
if c_path not in sys.path:
    sys.path.append(c_path)

import json, os
from datetime import datetime

'''
Loads the timestamp of last successful refresh
() -> ()
'''
def get_last_refresh():
    try:
        with open("data/last_pull_date.txt", 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "1900-01-01"
    except Exception as e:
        print(f"Error: {e}")
        return "1900-01-01"

'''
Updates the timestamp of last successful refresh
() -> ()
'''
def update_last_refresh():
    with open("data/last_pull_date.txt", 'w') as file:
        file.write(datetime.now().strftime("%Y-%m-%d"))

'''
Appends new search results to JSONL file (raw data) defined for clinicaltrials.
`(list[dict], str) -> ()`
Params:
* `results`: List of JSON documents, each JSON document is a study
* `path`: Destination filepath
'''
def save_raw_data(results, path):
    if not results:
        print("No raw data to save")
        return
    try:
        with open(path, 'w') as file:
            for study in results:
                json.dump(study, file)
                file.write('\n')
        print(f"Saved {len(results)} new studies.")
    except Exception as e:
        print(f"Error: {e}")

'''
Saves rehab-research.com formatted data.
`(list[dict[Any]], str) -> ()`
Params:
    `data: list[dict[Any]]`. List of JSON documents
    `path: str`. Dest filepath.
'''
def save_processed_data(data, path):
    if not data:
        print("No processed data to save")
        return
    try:
        with open(path, 'w') as file:
            for row in data:
                json.dump(row, file)
                file.write('\n')
        print(f"Saved {len(data)} rows to {path}")
    except Exception as e:
        print("Error:", e)

'''
Pulls data from raw JSONL file to be processed.
`str -> list[dict]`
Params:
* `path`: Source filepath
Return:
* `documents`: JSON data
'''
def read_jsonl_file(path):
    documents = []
    if not os.path.exists(path):
        print(f"{path} does not exist.")
        return documents
    try:
        with open(path, 'r') as file:
            for line in file:
                if line.strip():
                    documents.append(json.loads(line))
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return []
    except IOError as e:
        print("I/O error:", e)
        return []
    return documents

'''
Formats results from raw JSONL into rehab-research.com universal format.
`(str, Callable) -> list[dict]`
Params:
* `path`: Source filepath
* `transform_fn`: transformation function
Return:
* Processed JSON data
'''
def to_universal_format(path, transform_fn):
    raw_data = read_jsonl_file(path)
    if not raw_data:
        print(f"No data from {path} found.")
        return []
    return transform_fn(raw_data)
