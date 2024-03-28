import requests

data_source_1 = "https://costellomanagementllc.managebuilding.com/Resident/public/rentals" # Costello management
res = requests.get(data_source_1)
# print(res.text)