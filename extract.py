import requests
import beautifulsoup4 as bs

data_source_1 = "https://costellomanagementllc.managebuilding.com/Resident/public/rentals" # Costello management
res = requests.get(data_source_1).text
soup = bs(res, 'html.parser')

list_street = []
list_state = []
list_adress = []

for street in soup.find_all(class_="featured-listing__title"): # Street information
    list_street.append(street.text)

for state in soup.find_all(class_="featured-listing__address"): # State information
    list_state.append(state.text)

for i in range(len(list_street)):
    list_adress.append(list_street[i]+ ' ' + list_state[i])  # Combine street and state

## House type's class = featured-listing__features
list_ht = []
for house_type in soup.find_all(class_='featured-listing__features'):
    list_ht.append(house_type.text)

## Price's class = featured-listing__price accent-color
list_price = []
for price in soup.find_all(class_="featured-listing__price accent-color"):
    list_price.append(price.text)

## Avaliable Data's class = featured-listing__availability hide--mobile
list_date = []
for date in soup.find_all(class_="featured-listing__availability hide--mobile"):
    list_date.append(date.text)

dic_date = {  # Create a dictionary to match all the months
    "January": "1",
    "February": "2",
    "March": "3",
    "April": "4",
    "May": "5",
    "June": "6",
    "July": "7",
    "August": "8",
    "September": "9",
    "October": "10",
    "November": "11",
    "December": "12",
}

list_date = [items.replace("\n", '') for items in list_date]
list_date = [items.replace("\r", '') for items in list_date]
list_date = [items.replace(" ", '') for items in list_date]
list_date = [items.replace("available", '') for items in list_date] # Temporaly remove the strings

def convert(ele):  # Create a function to convert month into numbers
    letter = ''.join(filter(str.isalpha, ele))
    digit = ''.join(filter(str.isdigit, ele))

    letter = dic_date[letter] + '/'
    digit = digit + '/2024'
    return letter + digit

list_date = [convert(items) for items in list_date] # Call the function

add_str = "AVALIABLE "
list_date = [add_str + element for element in list_date] # Add up AVALIABLE

## Description Class = featured-listing__description hide--mobile
list_des = []
for item in soup.find_all(class_="featured-listing__description hide--mobile"):
    list_des.append(item.text)

## Merge all the datas
list_total = []
list_tool = []
list_names = [list_adress,list_ht,list_price,list_date,list_des]

for i in range(len(list_adress)):
    for n in list_names:
        list_tool.append(n[i])
    list_total.append(list_tool)
    list_tool = [] # Reset

print(list_total[0])