import requests
from bs4 import BeautifulSoup as bs
from parameter_store import para_store 


def convert(ele):  # Create a function to convert month into numbers
    dic_date = {  
    "January": "1","February": "2","March": "3","April": "4","May": "5","June": "6","July": "7","August": "8","September": "9",
    "October": "10","November": "11","December": "12"}
    letter = ''.join(filter(str.isalpha, ele))
    digit = ''.join(filter(str.isdigit, ele))

    letter = dic_date[letter] + '/'
    digit = digit + '/2024'

    return letter + digit

def address():  ## Get address
    list_street = []
    list_state = []
    list_address = []

    url = para_store('url')
    res = requests.get(url)
    content = res.text
    soup = bs(content, 'html.parser')

    for street in soup.find_all(class_="featured-listing__title"): # Street information
        list_street.append(street.text)

    for state in soup.find_all(class_="featured-listing__address"): # State information
        list_state.append(state.text)

    for i in range(len(list_street)):
        list_address.append(list_street[i]+ ' ' + list_state[i])  # Combine street and state

    return list_address


def house_type(): ## Get house type
    list_ht = []

    url = para_store('url')
    res = requests.get(url)
    content = res.text
    soup = bs(content, 'html.parser')

    for house_type in soup.find_all(class_='featured-listing__features'):
        list_ht.append(house_type.text)

    return list_ht

def price(): ## Get price
    list_price = []

    url = para_store('url')
    res = requests.get(url)
    content = res.text
    soup = bs(content, 'html.parser')

    for price in soup.find_all(class_="featured-listing__price accent-color"):
        list_price.append(price.text)

    return list_price

def avaliable_date(): ## Get date
    list_date = []

    url = para_store('url')
    res = requests.get(url)
    content = res.text
    soup = bs(content, 'html.parser')

    for date in soup.find_all(class_="featured-listing__availability hide--mobile"):
        list_date.append(date.text)

    list_date = [items.replace("\n", '') for items in list_date]
    list_date = [items.replace("\r", '') for items in list_date]
    list_date = [items.replace(" ", '') for items in list_date]
    list_date = [items.replace("available", '') for items in list_date] 

    list_date = [convert(items) for items in list_date] ## Call 'convert' function
    add_str = "AVALIABLE "
    list_date = [add_str + element for element in list_date] 

    return list_date

def get_des(): # Get description in the second layer
    list_link = []
    list_des = []

    url_head = para_store('url_head')
    url = para_store('url')
    res = requests.get(url)
    content = res.text
    soup = bs(content, 'html.parser')

    for link in soup.find_all('a', class_='featured-listing accent-color-border-on-hover'): # Get all link in the first layer
        list_link.append(link.get('href'))

    for link in list_link:
        url_des = url_head + link
        res_des = requests.get(url_des)
        content = res_des.text 
        soup_des = bs(content, 'html.parser')
        for description in soup_des.find_all('p', class_='unit-detail__description'):
            list_des.append(description.text)

    list_des = [' '.join(list_des[i:i+2]) for i in range(0, len(list_des), 2)]

    ## Data cleaning
    for i in range(len(list_des)):
        list_des[i] = list_des[i].replace("\no\t", "")
        list_des[i] = list_des[i].replace("\n", "")
        list_des[i] = list_des[i].replace("\t", "")
        list_des[i] = list_des[i].replace("w/", "")
    return list_des

def extract_main():
    ## Merge all the datas
    list_total = []
    list_tool = []
    list_names = [address(),house_type(),price(),avaliable_date(),get_des()]
    for i in range(len(address())):
        for n in list_names:
            list_tool.append(n[i])
        list_total.append(list_tool)
        list_tool = [] # Reset

    return list_total

# ## Now all the data is in the list_total, each element is an row.

if __name__ == '__main__': ## Test
    print('On main')