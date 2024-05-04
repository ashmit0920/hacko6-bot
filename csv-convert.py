import csv
import json

data = [
    ['Team Name', 'Member 1', 'Member 2', 'Member 3', 'Member 4', 'Member 5']
]

with open("teams2.json", "r") as f:
    teams = json.load(f)

for i in teams.keys():
    lst = [i]
    for j in teams[i]:
        lst.append(j)
    data.append(lst)

file_name = 'teams2.csv'

with open(file_name, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(data)

print(f"CSV file created successfully.")