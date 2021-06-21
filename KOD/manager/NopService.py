import json

with open('160221.json', 'r', encoding="utf-8") as f:
    data = json.load(f)


class NopService:

    @staticmethod
    def get_all_nop_data():
        return data
