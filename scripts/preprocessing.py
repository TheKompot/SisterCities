import pickle


file = open('data/sister_cities.pkl', 'rb')
data = pickle.load(file)
file.close()


country_to_continent = {}

for val in data.values():
    if val['continent'] == 'the_United_Kingdom':
        val['continent'] = 'Europe'
    if val['continent'] == 'South_America':
        val['continent'] = 'South America'
    if val['continent'] == 'North_America':
        val['continent'] = 'North America'
    if val['country'] not in country_to_continent:
        country_to_continent[val['country']] = val['continent']
    
file = open('data/sister_cities.pkl', 'wb')

plus_countries = ['Cape Verde', 'North Macedonia', 'Poland', 'São Tomé and Príncipe', 'Island', 'New Zealand',
                 'Germany', 'Japan', 'Japa', 'England', 'Antigua and Barbuda', 'France', 'Philippines', 'Kosovo',
                 'Seychelles', 'The Gambia', 'Czech Republic', 'Kazakhstah', 'South Africa', 'Hungary', 'Czech Republic ',
                   'San Marino', 'Bosnia and Hercegovina', 'Moldavia', 'China', 'Gibraltar', 'Germany ', 'Italy',
                     'Bosnia and Herzegovina', 'Taiwan', 'NaN', 'Andorra', 'South Korea', 'United Kingdom', 'United States',
                       'Isle of Man', 'West Bank', 'Netherlands', 'Ireland', 'Faroe Islands', 'Vietnam', 'Cyprus']
plus_continent = ['Africa','Europe','Europe','Africa','Europe','Oceania',
                  'Europe','Asia','Asia','Europe','North America','Europe','Asia','Europe',
                  'Africa','Africa','Europe','Asia','Africa','Europe','Europe',
                  'Europe','Europe','Europe','Asia','Europe','Europe','Europe',
                  'Europe','Asia','Europe','Europe','Asia','Europe','North America',
                  'Europe','Asia','Europe','Europe','Europe','Asia','Europe']
for country, cont in zip(plus_countries,plus_continent):
    country_to_continent[country] = cont
    


not_found= set()

for val in data.values():
    val['continent_of_sc'] = []
    for country in val['country_of_sc']:
        if country in country_to_continent:
            val['continent_of_sc'].append(country_to_continent[country])
        else:
            print(country)
print(set(country_to_continent.values()))    

# dump information to that file
pickle.dump(data, file)

# close the file
file.close()