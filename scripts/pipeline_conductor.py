# The path to packages on the C: drive
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'

# Add the path to the Python system path
if c_path not in sys.path:
    sys.path.append(c_path)

from utils import (get_last_refresh, update_last_refresh,
                   save_raw_data, to_universal_format)

SOURCE_REGISTRY = [
    clinical_trials.METADATA
]

'''
Orchestrates pipeline. Loops through registered sources with process:
1. Fetch new data, 2. Save raw data, 3. Transform to rehab-research.com format
Then consolidates results and generates embeddings.
'''
def main():
    last_refresh = get_last_refresh()
    all_records = []
    print("\n STARTING PIPELINE \n")
    print(f"Grabbing data since: {last_refresh}")

    for source in SOURCE_REGISTRY:
        source_name = source['name']
        raw_path = source['path']
        print(f"Beginning source: {source_name}")

        try:
            raw_results = source['fetch_func'](source['search_terms'], last_refresh)
            if raw_results:
                save_raw_data(raw_results, raw_path)
            else:
                print(f"No new data for {source_name")

        except Exception as e:
            print(f"CRITICAL ERROR during {source_name} fetch stage: {e}")
            continue

        try:
            universal_data = to_universal_format(raw_path, source['transform_fn'])
            all_records.extend(universal_data)
        except Exception as e:
            print(f"CRITICAL ERROR during {source_name} transform stage: {e}")
            continue

    print("\n PIPELINE ENDED")
    print(f"Retrieved {len(all_records)} rows")
    if len(all_records) > 0:
        update_last_refresh()
    else:
        print("No new data across ALL sources. No updates")

if __name__ == "__main__":
    main()
