import pandas as pd
import requests
from bs4 import BeautifulSoup
import html
import json

#Grab the list of dog breeds
with open('Data/Dogs/dog_link_list.csv','r') as d:
    for line in d:
        #split by comma
        dog_links = [x.strip() for x in line.split(',')]
        #remove all weirdness from the list
        dog_links = [x.strip('\'').strip('[\'').strip('\']') for x in dog_links]
d.close()

dog_df = pd.DataFrame()

for link in dog_links:
    #Get info for a specific breed 
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    html_data = soup.find('div', {'data-js-component': 'breedPage'})

    #includes '<div data-js-component="breedPage" data-js-props="' at the start and '>  </div>' at the end, which is not json.
    raw_div = html.unescape(str(html_data))

    # just remove html stuff! 
    clean_div = raw_div[50:-9]

    #save to a temporary json file
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(clean_div)
    
    # Opening JSON file
    f = open('data.json')
    
    # # returns JSON object as 
    # # a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    # Opening JSON file
    f = open('data.json')

    if len(data['settings']['breed_data']) > 1:
        current_breed = data['settings']['current_breed']
        row = { 'Breed': data['settings']['breed_data']['basics'][current_breed]['breed_name'], 
                'Description': data['settings']['breed_data']['description'][current_breed]['akc_org_blurb'], 
                'Group': data['settings']['current_breed_group']['name'], 
                'Origin':  data['settings']['breed_data']['basics'][current_breed]['origin'],
                'Life Expectancy': data['settings']['breed_data']['basics'][current_breed]['life_expectancy'], 
                'Related Breeds': data['settings']['breed_data']['basics'][current_breed]['related_breeds'], 
                'Temperament': data['settings']['breed_data']['traits'][current_breed]['temperament'], 
                'Adaptability Level': data['settings']['breed_data']['traits'][current_breed]['traits']['adaptability_level']['score'], 
                'Affectionate With Family': data['settings']['breed_data']['traits'][current_breed]['traits']['affectionate_with_family']['score'],
                'Barking Level': data['settings']['breed_data']['traits'][current_breed]['traits']['barking_level']['score'],
                'Coat Grooming Frequency': data['settings']['breed_data']['traits'][current_breed]['traits']['coat_grooming_frequency']['score'], 
                'Good with Young Children': data['settings']['breed_data']['traits'][current_breed]['traits']['good_with_young_children']['score'],
                'Coat Length': data['settings']['breed_data']['traits'][current_breed]['traits']['coat_length']['score'],
                'Coat Type': data['settings']['breed_data']['traits'][current_breed]['traits']['coat_type']['selected'],
                'Drooling Level': data['settings']['breed_data']['traits'][current_breed]['traits']['drooling_level']['score'],
                'Energy Level': data['settings']['breed_data']['traits'][current_breed]['traits']['energy_level']['score'],
                'Good With Other Dogs': data['settings']['breed_data']['traits'][current_breed]['traits']['good_with_other_dogs']['score'],
                'Mental Stimulation Needs': data['settings']['breed_data']['traits'][current_breed]['traits']['mental_stimulation_needs']['score'],
                'Openness to Strangers': data['settings']['breed_data']['traits'][current_breed]['traits']['openness_to_strangers']['score'],
                'Playfulness Level': data['settings']['breed_data']['traits'][current_breed]['traits']['playfulness_level']['score'],
                'Shedding Level': data['settings']['breed_data']['traits'][current_breed]['traits']['shedding_level']['score'],
                'Trainability Level': data['settings']['breed_data']['traits'][current_breed]['traits']['trainability_level']['score'],
        
        }

        if data['settings']['breed_data']['standards'][current_breed]['height_display']: 
            try:
                row['Min Height'] = data['settings']['breed_data']['standards'][current_breed]['height_min_f']
            except KeyError:
                row['Min Height'] = data['settings']['breed_data']['standards'][current_breed]['height_display']
            try:
                row['Max Height'] = data['settings']['breed_data']['standards'][current_breed]['height_max_m'] 
            except KeyError:
                row['Max Height'] = data['settings']['breed_data']['standards'][current_breed]['height_display']   
            
            
            try:
                row['Min Weight'] = data['settings']['breed_data']['standards'][current_breed]['weight_min_f']
            except KeyError:
                row['Min Weight'] = data['settings']['breed_data']['standards'][current_breed]['weight_display']
            try:
                row['Max Weight'] = data['settings']['breed_data']['standards'][current_breed]['weight_max_m']  
            except KeyError:
                row['Max Weight'] = data['settings']['breed_data']['standards'][current_breed]['weight_display']    


        print(row)
        dog_df = pd.concat([dog_df, pd.DataFrame([row])], ignore_index=True)

dog_df.to_csv('Breed_Info.csv')

# print(dogs)
