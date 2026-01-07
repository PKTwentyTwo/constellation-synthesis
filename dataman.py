'''A data manager that uses JSON to store syntheses.'''
#(I have barely any idea how JSON works.)
import json
import os
cwd = os.getcwd()
datadir = cwd + '/data/'
if not os.path.exists(datadir):
    os.mkdir(datadir)

class DataManager:
    '''The class used for the actual data management.'''
    def __init__(self, rule):
        '''Setup the data manager with a dictionary of lists of dictionaries.'''
        self.rule = rule
        self.loaded = {}
    def load_data(self, apgcode, rule=None):
        '''Attempt to load data from a json file.'''
        if rule is None:
            rule = self.rule
        data = []
        file = datadir + rule + '/' + apgcode + '.json'
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            data = json.loads(content)
        self.loaded[apgcode] = data
    def save_json(self, file, data):
        '''Saves a list of dictionaries as a json file.'''
        full_json = '['
        for x in data:
            section = '{'
            for y in x:
                item = x[y]
                section = section + '\"' + y + '\":'
                if type(item) == type(10):
                    section += str(item)
                elif type(item) == type('Yes'):
                    section += '\"' + item + '\"'
                else:
                    section += '\"' + str(item) + '\"'
                section = section + ','
            section = section[:-1]
            section += '}'
            full_json += section + ','
        full_json = full_json[:-1]
        full_json = full_json + ']'
        full_json = full_json.replace('\'', '\"')
        print(file)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(full_json)
    def commit(self, apgcode, dictionary):
        '''Adds a dictionary to the big data structure.'''
        if apgcode not in self.loaded:
            self.loaded[apgcode] = [dictionary]
        else:
            self.loaded[apgcode].append(dictionary)
    def getfield(self, apgcode, field):
        if apgcode not in self.loaded:
            return []
        dictionaries = self.loaded[apgcode]
        if len(dictionaries) == 0:
            return []
        if field not in dictionaries[0]:
            return []
        data = []
        for x in dictionaries:
            data.append(x[field])
        return data
