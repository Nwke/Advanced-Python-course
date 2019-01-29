import json

countries_json = open('countries.json')
countries = json.load(countries_json)


class WikiCountries:
    def __init__(self, file_path, path_to_write):
        self.countries = json.load(open(file_path))
        self.ind = -1
        self.max_range = len(countries)

        self.out = open(path_to_write, 'a', encoding='utf8')

    def __iter__(self):
        return self

    def __next__(self):
        self.ind += 1
        if self.ind == self.max_range:
            self.out.close()
            raise StopIteration
        return self.countries[self.ind]['name']['official']

    def write_country_in_file(self, country):
        wiki_link = f'https://en.wikipedia.org/wiki/{country}'
        self.out.write(f'{country} - {wiki_link}\n')


our_country = WikiCountries('countries.json', 'new_countries.txt')

for country in our_country:
    our_country.write_country_in_file(country)
