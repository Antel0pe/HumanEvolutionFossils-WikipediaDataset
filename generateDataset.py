import pandas as pd

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
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_human_evolution_fossils#Late_Miocene_(7.2%E2%80%935.5_million_years_old)', match=f'^{fossil['firstFossilName']}$')
    
    if len(table) > 1:
        print(f'Matching multiple tables for: {fossil}. There should only be 1... Taking first match.')
        table = table[0]
    elif len(table) == 0:
        print(f'No matching table found for {fossil}...')
    elif len(table) == 1:
        table = table[0]

    
    listOfTables.append(table)

concatTables = pd.concat(listOfTables)

def combineYearDiscoveredColumns(row):
    if not pd.isna(row['Year discovered']):
        return row['Year discovered']
    elif not pd.isna(row['Date discovered']):
        return row['Date discovered']
    else:
        return ''

concatTables['Date of Discovery'] = concatTables.apply(combineYearDiscoveredColumns, axis=1)
mergedDateTable = concatTables.drop(columns=['Year discovered', 'Date discovered'])
print(mergedDateTable.columns.values)
