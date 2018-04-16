import os
import csv

from main.settings import BASE_DIR


def read_csv(file, fieldnames):
    # return ordered dict
    data = []
    with open(os.path.join(BASE_DIR, "region", file), newline="") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            data.append(row)
    return data


PROVINCES = read_csv("provinces.csv", fieldnames=['id', 'name'])
# REGENCIES = read_csv("regencies.csv", fieldnames=['id', 'ign', 'name'])
# DISTRICTS = read_csv("districts.csv", fieldnames=['id', 'ign', 'name'])
# VILLAGES = read_csv("villages.csv", fieldnames=['id', 'ign', 'name'])
