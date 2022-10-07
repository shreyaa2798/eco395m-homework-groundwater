import os
import csv
import pprint
import requests
import json

from clean_data import extract_data


def request_raw_data():

    """Requests the groundwater levels
    for summer of 2022 (Jun 6th to Sept 22)
    for Texas
    in a JSON format.
    Allows gzip compression in transit.
    Returns a dictionary representing the JSON response.
    """
    url = 'https://waterservices.usgs.gov/nwis/gwlevels'
    params = {'format' : 'json',
                'stateCd':'tx',
                'startDT':'2022-06-21',
                'endDT' :'2022-09-22',
                'siteStatus':'all'}

    resp = requests.get(url, params = params)
    # pprint.pprint(resp.json())
    data = resp.json()
    return data


def sort_data(data):
    """Sort the data lexicographically by "variable_name", "site_name" and then "datetime"."""
    sorted_data = sorted(data, key = lambda x: (x["variable_name"], x["site_name"],x["datetime"]) )
    return sorted_data

def write_data_to_csv(data, path):
    """Write the data to the csv.
    The columns should be in the order:
        "variable_name",
        "site_name",
        "datetime",
        "value",
        "longitude",
        "latitude"
    """
    with open(path, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=["variable_name",
        "site_name",
        "datetime",
        "value",
        "longitude",
        "latitude"])
        fc.writeheader()
        fc.writerows(data)

    return


if __name__ == "__main__":

    BASE_DIR = "artifacts"
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")

    os.makedirs(BASE_DIR, exist_ok=True)

    raw_data = request_raw_data()
    clean_data = extract_data(raw_data)
    sorted_data = sort_data(clean_data)

    write_data_to_csv(sorted_data, CSV_PATH)