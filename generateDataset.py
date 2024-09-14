import pandas as pd
import json

# For each table of data, this is the name of the first fossil. Pandas will only scrape tables that have one of these fossil names. 
firstFossilFromEachTable = [
    {
        'table': 'Late Miocene',
        'firstFossilName': 'El Graeco'
    },
    {
        'table': 'Pliocene',
        'firstFossilName': 'Ardi'
    }, 
    {
        'table': 'Lower Paleolithic',
        'firstFossilName': 'KNM-WT 17000'
    }, 
    {
        'table': 'Middle Paleolithic',
        'firstFossilName': 'Dragon Man'
    }, 
    {
        'table': 'Upper Paleolithic',
        'firstFossilName': 'Homo luzonensis'
    },
    {
        'table': 'Holocene',
        'firstFossilName': 'Luzia'
    }
]

listOfTables = []

for fossil in firstFossilFromEachTable:
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_human_evolution_fossils#Late_Miocene_(7.2%E2%80%935.5_million_years_old)',
                         match=f'^{fossil["firstFossilName"]}$',
                         attrs={'class': 'wikitable'})

    if len(table) >= 1:
        if len(table) > 1:
            print(f'Matching multiple tables for: {fossil}. There should only be 1... Taking first match.')

        table = table[0]
        listOfTables.append(table)
    else:
        print(f'No matching table found for {fossil}...')

    
    

concatTables = pd.concat(listOfTables)

print(concatTables)

def combineYearDiscoveredColumns(row):
    if not pd.isna(row['Year discovered']):
        return row['Year discovered']
    elif not pd.isna(row['Date discovered']):
        return row['Date discovered']
    else:
        return ''

concatTables['Date of Discovery'] = concatTables.apply(combineYearDiscoveredColumns, axis=1)
mergedDateTable = concatTables.drop(columns=['Year discovered', 'Date discovered', "Unnamed: 0"])
removeCitations = mergedDateTable.replace(r'\[\d+\]', '', regex=True)
removeCitations.to_json('fossil_data.json', orient='records', lines=False, force_ascii=False)

