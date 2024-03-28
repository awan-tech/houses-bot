import requests
import beautifulsoup4 as bs
data_source_1 = "https://costellomanagementllc.managebuilding.com/Resident/public/rentals" # Costello management
res = requests.get(data_source_1).text
# print(res.text)
