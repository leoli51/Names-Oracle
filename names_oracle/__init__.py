import os
from os import path
import importlib.resources

data_handle = importlib.resources.files(__package__).joinpath("data")
with data_handle as p:
    data_path = p

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
    with data_handle as data_path:
        return os.listdir(data_path)

def load(country):
    global names
    global last_names

    if country not in get_available_countries():
        raise ValueError(f'Country: {country} is not supported or is not a valid country. Hint: use list_available_countries()')
    
    names[country] = dict()
    max_occurrences[country] = {'name' : 0, 'last_name' : 0}
    max_name_occ = 0
    with open(path.join(data_path, country, 'names.csv'), 'r', encoding='utf-8') as namesfile:
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
            max_name_occ = max(max_name_occ, sum(names[country][name].values()))
    
    max_occurrences[country]['name'] = max_name_occ
    
    last_names[country] = dict()
    max_last_name_occ = 0
    with open(path.join(data_path, country, 'last_names.csv'), 'r', encoding='utf-8') as lastnamesfile:
        for i, line in enumerate(lastnamesfile.readlines()):
            if i == 0:
                continue
            line = line.strip().split(',')
            lastname = line[0]
            count = int(line[1])
            last_names[country][lastname] = count
            max_last_name_occ = max(max_last_name_occ, count)
    
    max_occurrences[country]['last_name'] = max_last_name_occ

# query name data:  
def get_name_info(name, country):
    global names
    global last_names

    if country not in last_names:
        load(country)

    first_name_counts = None
    if name in names[country]:
        first_name_counts = names[country][name]

    last_name_count = 0
    if name in last_names[country]:
        last_name_count = last_names[country][name]
    
    # returns none if there is no available data for this entry
    if not (first_name_counts or last_name_count):
        return None
    
    name_count = first_name_counts if first_name_counts else {'M' : 0, 'F': 0}
    total_name_count = sum(name_count.values())
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


def split_name_in_first_and_last(name, country):
    name_parts = name.title().strip().split()
    best_score = 0
    best_names = []    
    for i in range(len(name_parts) + 1): # +1 to include the case in which it is only a name
        first_name_guess = " ".join(name_parts[:i])
        last_name_guess = " ".join(name_parts[i:])

        first_name_data = get_name_info(first_name_guess, country)
        last_name_data = get_name_info(last_name_guess, country)

        if not (first_name_data or last_name_data):
            continue

        fn_fn_score = first_name_data[FIRST_NAME_PROBABILITY_TAG] if first_name_data else 0
        fn_ln_score = first_name_data[LAST_NAME_PROBABILITY_TAG] if first_name_data else 0

        ln_fn_score = last_name_data[FIRST_NAME_PROBABILITY_TAG] if last_name_data else 0
        ln_ln_score = last_name_data[LAST_NAME_PROBABILITY_TAG] if last_name_data else 0

        if fn_fn_score + ln_ln_score > ln_fn_score + fn_ln_score:
            score = fn_fn_score + ln_ln_score
            if score > best_score:
                best_score = score
                best_names = [first_name_guess, last_name_guess]
        else:
            score = ln_fn_score + fn_ln_score
            if score > best_score:
                best_score = score
                best_names = [last_name_guess, first_name_guess]
    
    return best_names
