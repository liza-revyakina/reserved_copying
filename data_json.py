import json


class Data:
    def __init__(self, data, name='info.json'):
        self.name = name
        self.data = data

    def data_info(self):
        with open(self.name, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        with open(self.name, encoding='utf-8') as f:
            json_data = json.load(f)
        return json_data
