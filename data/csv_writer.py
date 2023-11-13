import csv

# Data to be written to the CSV file
input_data = [
    ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
    ['Acquisition costs', 'Land acquisition costs','', '1000000', '01/01/2020', '01/01/2020'],
    ['Construction costs', 'Build costs', 'builder1', '2000000','01/04/2020', '01/05/2022'],
    ['Construction costs', 'Contingency', 'builder1', '200000', '01/05/2020', '01/07/2022'],
    ['Professional fees','DM', 'Development management fee', '500000', '01/08/2020', '01/11/2022'],
    ['Professional fees', 'Consultants','consultant1', '50000', '01/12/2020', '24/01/2022'],
]


# Writing to the CSV files
file_name = 'data/input_data.csv'
with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(input_data)
        
