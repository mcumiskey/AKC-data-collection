import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_top_dogs(soup):
    table = soup.find("table")

    breed_ranks_list = [
        row.text.strip()
        for row in table.findAll("td")
        if not row.text == ""
        if not "\n" in row.text
    ]

    df = pd.DataFrame(columns=["Rank", "Breed"])

    #2022 has a different table format without header
    if breed_ranks_list[0] == "1":
        df["Rank"] = breed_ranks_list[0::2]  # Every other item starting from index 0 
        df["Breed"] = breed_ranks_list[1::2]   # Every other item starting from index 1 
    else: 
        #check if the data is a rank or a breed, then build dataframe accordingly. 
        if not breed_ranks_list[3].isdigit():
            df["Rank"] = breed_ranks_list[2::2]  # Every other item starting from index 0 
            df["Breed"] = breed_ranks_list[3::2]   # Every other item starting from index 1 
        else: 
            df["Breed"] = breed_ranks_list[2::2]   # Every other item starting from index 1 
            df["Rank"] = breed_ranks_list[3::2]  # Every other item starting from index 0 

    df.set_index("Rank", inplace=True)   
    return df


year_links = [
    "https://www.akc.org/expert-advice/news/most-popular-dog-breeds-2023/",
    "https://www.akc.org/expert-advice/dog-breeds/most-popular-dog-breeds-2022/",
    "https://www.akc.org/expert-advice/dog-breeds/most-popular-dog-breeds-of-2021/",
    "https://www.akc.org/expert-advice/dog-breeds/the-most-popular-dog-breeds-of-2020/",
    "https://www.akc.org/most-popular-breeds/2019-full-list/",
    "https://www.akc.org/most-popular-breeds/2018-full-list/",
    "http://akc.org/most-popular-breeds/2017-full-list",
    "https://www.akc.org/most-popular-breeds/2016-full-list/",
    "https://www.akc.org/most-popular-breeds/2015-full-list/",
    "https://www.akc.org/most-popular-breeds/2014-full-list/",
    "https://www.akc.org/most-popular-breeds/2013-full-list/"
]

start_year = 2023

for year in year_links:
    page = requests.get(year)
    soup = BeautifulSoup(page.content, 'html.parser')
    top_200 = get_top_dogs(soup)
    file_name = "top_200_" + str(start_year)
    top_200.to_csv(file_name)
    start_year -= 1


