import os
from os import path

# common tags
NAME_TAG = 'name'

# name tags
NAME_COUNT_TAG = 'first_name_frequency'
NAME_NORM_COUNT_TAG =  'first_name_norm_frequency'
MALE_COUNT_TAG = 'male_frequency'
FEMALE_COUNT_TAG = 'female_frequency'
MALE_PROBABILITY_TAG = 'male_probability'
FEMALE_PROBABILITY_TAG = 'female_probability'
FIRST_NAME_PROBABILITY_TAG = 'first_name_probability'

# last name tags
LAST_NAME_COUNT_TAG = 'last_name_frequency'
LAST_NAME_NORM_COUNT_TAG =  'last_name_norm_frequency'
LAST_NAME_PROBABILITY_TAG = 'last_name_probability'

# country -> name -> sex -> count
names = dict()
# country -> surname -> count
last_names = dict()

max_occurrences = dict()

def get_available_countries():
    return os.listdir('data')

available_countries = get_available_countries()

def load(country):
    global names
    global last_names

    if country not in available_countries:
        raise ValueError(f'Country: {country} is not supported or is not a valid country. Hint: use list_available_countries()')
    
    names[country] = dict()
    max_occurrences[country] = {'name' : 0, 'last_name' : 0}
    max_name_occ = 0
    with open(path.join('data', country, 'names.csv'), 'r', encoding='utf-8') as namesfile:
        for i, line in enumerate(namesfile.readlines()):
            if i == 0:
                continue
            line = line.strip().split(',')
            name = line[0]
            sex = line[1]
            count = int(line[2])
            if name not in names[country]:
                names[country][name] = {'M' : 0, 'F' : 0}
            
            names[country][name][sex] = count
            max_name_occ = max(max_name_occ, count)
    
    max_occurrences[country]['name'] = max_name_occ
    
    last_names[country] = dict()
    max_last_name_occ = 0
    with open(path.join('data', country, 'last_names.csv'), 'r', encoding='utf-8') as lastnamesfile:
        for i, line in enumerate(lastnamesfile.readlines()):
            if i == 0:
                continue
            line = line.strip().split(',')
            lastname = line[0]
            count = int(line[1])
            last_names[country][lastname] = count
            max_last_name_occ = max(max_last_name_occ, count)
    
    max_occurrences[country]['last_name'] = max_last_name_occ

def load_all():
    for country in available_countries:
        load(country)

# query name data:  
def get_name_info(name, country):
    global names
    global last_names

    if country not in last_names:
        load(country)

    first_name_data = None
    if name in names[country]:
        first_name_data = names[country][name]

    last_name_data = None
    if name in last_names[country]:
        last_name_data = last_names[country][name]
    
    # returns none if there is no available data for this entry
    if not (first_name_data or last_name_data):
        return None
    
    name_count = first_name_data if first_name_data else {'M' : 0, 'F': 0}
    total_name_count = sum(name_count.values())
    last_name_count = last_name_data if last_name_data else 0
    total_count = total_name_count + last_name_count 

    info = {
        NAME_TAG : name,

        NAME_COUNT_TAG : total_name_count, 
        NAME_NORM_COUNT_TAG : total_name_count / max_occurrences[country]['name'],
        MALE_COUNT_TAG : name_count['M'],
        FEMALE_COUNT_TAG : name_count['F'],
        MALE_PROBABILITY_TAG : name_count['M'] / (total_name_count if total_name_count else 1),
        FEMALE_PROBABILITY_TAG : name_count['F'] / (total_name_count if total_name_count else 1),
        FIRST_NAME_PROBABILITY_TAG : total_name_count / total_count,

        LAST_NAME_COUNT_TAG : last_name_count,
        LAST_NAME_NORM_COUNT_TAG : last_name_count / max_occurrences[country]['last_name'],
        LAST_NAME_PROBABILITY_TAG : last_name_count / total_count
    }

    return info

if __name__ == '__main__':
    from pprint import pprint
    pprint(get_available_countries())
    pprint(get_name_info('Leonardo', 'IT'))
    pprint(get_name_info('Maria Felicita', 'IT'))
    pprint(get_name_info('Banana', 'IT'))
    pprint(get_name_info('Mawlkenv lka', 'IT'))
