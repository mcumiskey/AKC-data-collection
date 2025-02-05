import json
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import html

page = requests.get("https://www.akc.org/dog-breeds/")
soup = BeautifulSoup(page.content, 'html.parser')


# find the select element and then all the option elements inside it
select = soup.find('select', {'id': 'mobile-breed-search'})
#"option" is all the things that appear in the mobile links
options = select.find_all('option')

# breed names!
breeds = [option.text.strip() for option in options]

#links!
links = []
for o in options: 
    result = re.search(r"\"([^]]+)\"", str(o))

    if result:
        links.append(result.group().strip("\""))

links = [re.search(r"\"([^]]+)\"", str(o)).group().strip("\"") 
         for o in options 
         if re.search(r"\"([^]]+)\"", str(o))]

print(links)

