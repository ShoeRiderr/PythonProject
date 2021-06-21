from collections import Counter
from manager.NopService import NopService
import matplotlib.pyplot as plt


class Model:
    available_symptoms = {
        "Zaczerwienienie i bolesność": ["zaczerwienienie i krótkotrwała bolesność",
                                        "zaczerwienieniei krótkotrwała bolesność"],
        # I figured out that there is a typo in json file
        "Gorączka": ["temp", "temperatura", "gorączka"],
        "Drgawki": ["drgawki"],
        "Wymioty": ["wymioty"],
        "Omdlenie": ["omdlenie", "utrata przytomności"]
    }

    available_genders = {
        "male": "M",
        "female": "K"
    }

    def __init__(self):
        self.nop_list = []
        self.nops = NopService.get_all_nop_data()

        for nop in self.nops:
            list_of_symptoms_keys = [key
                                     for key, list_of_symptoms_values in Model.available_symptoms.items()
                                     for symptom in list_of_symptoms_values
                                     if symptom in nop["DESCRIPTION"].lower()]

            result = {
                "date": nop["DATE"],
                "voivodeship": nop["VOIVODESHIP"],
                "region": nop["REGION"],
                "gender": nop["GENDER"],
                "symptoms": list(dict.fromkeys(list_of_symptoms_keys))  # remove duplicated symptoms
            }
            self.nop_list.append(result)

    def count_loaded_nops(self):
        return len(self._get_all_nops())

    def count_womens_loaded_in_nops(self):
        return len(list(filter(lambda x: x["gender"] == "K", self._get_all_nops())))

    def count_mens_loaded_in_nops(self):
        return self.count_loaded_nops() - self.count_womens_loaded_in_nops()

    def count_people_with_fever_in_pomeranian_voivodeship(self):
        records = self._get_records_from_specific_voivodeship('pomorskie')
        all_symptoms = dict()
        i = 0
        for value in records:
            for symptom in value["symptoms"]:
                if symptom.lower() == 'gorączka':
                    all_symptoms[i] = symptom
                    i += 1

        return dict(Counter(all_symptoms.values()))

    def statement_showing_amount_of_nops_in_voivodeships(self):
        voivodeships = dict()
        i = 0
        for value in self._get_all_nops():
            voivodeships[i] = value['voivodeship']
            i += 1

        return dict(Counter(voivodeships.values()))

    def quantitative_statistics_of_nop_symptoms_in_pomerania(self):
        result = self._calculate_number_of_symptoms("pomorskie")

        return dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

    def create_pie_chart_of_occurrence_of_nops_depending_on_gender(self):
        gender_division = dict()
        i = 0
        for value in self._get_all_nops():
            if value['gender'] in Model.available_genders.values():
                gender_division[i] = value['gender']
                i += 1

        counted_gender_division = dict(Counter(gender_division.values()))
        all_records = counted_gender_division["K"] + counted_gender_division["M"]

        pie_labels = ["Female", "Male"]
        counted_gender_division_in_perc = list(map(lambda x: (x * 100) / all_records, counted_gender_division.values()))

        fig1, ax1 = plt.subplots()
        ax1.pie(counted_gender_division_in_perc, labels=pie_labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        plt.title("Occurrence of NOP's depending on gender")
        plt.show()
        plt.savefig('wykres_zadanie_6.png')

    def create_bar_graph_of_amount_of_each_symptoms(self):
        counted_symptoms = self._calculate_number_of_symptoms()
        symptoms = list(counted_symptoms.keys())
        symptoms_amount = list(counted_symptoms.values())

        plt.bar(symptoms, symptoms_amount, width=0.4)

        plt.xlabel("Symptoms")
        plt.ylabel("Quantity")
        plt.title("Quantitative statistics of all nops in Poland")
        plt.show()
        plt.savefig('wykres_zadanie_7.png')

    def create_line_chart_showing_number_of_nops_in_time(self):
        dates = self._get_list_of_days_from_nops_dates()
        men = self._filter_num_of_nops_by_date('M')
        women = self._filter_num_of_nops_by_date('K')
        plt.plot(dates, men)
        plt.plot(dates, women)
        plt.legend(["Men", "Women"], loc="upper left")
        plt.title('Line chart showing number of NOPs in time.')
        plt.xlabel('Dates')
        plt.ylabel('Amount of NOP')
        plt.show()
        plt.savefig('wykres_zadanie_8.png')

    def _get_all_nops(self):
        return self.nop_list

    def _calculate_number_of_symptoms(self, voivodeship=''):
        if len(voivodeship) > 0:
            records = self._get_records_from_specific_voivodeship(voivodeship)
        else:
            records = list(self._get_all_nops())

        all_symptoms = dict()
        i = 0
        for value in records:
            for symptom in value["symptoms"]:
                all_symptoms[i] = symptom
                i += 1

        return dict(Counter(all_symptoms.values()))

    def _get_list_of_dates(self):
        records = list(self._get_all_nops())
        all_dates = dict()
        i = 0
        for value in records:
            all_dates[i] = value["date"]
            i += 1

        return list(dict.fromkeys(list(all_dates.values())))

    def _filter_num_of_nops_by_date(self, gender):
        if gender.upper() not in Model.available_genders.values():
            raise TypeError("Gender parameter must be equal M or K.")

        result = dict()
        i = 0
        for date in self._get_list_of_dates():
            result[i] = len(
                list(filter(lambda x: x['gender'] == gender.upper() and x['date'] == date, self._get_all_nops())))
            i += 1

        return list(result.values())

    def _get_list_of_days_from_nops_dates(self):
        result = dict()
        i = 0

        for date in self._get_list_of_dates():
            result[i] = date[:5]
            i += 1

        return list(result.values())

    def _get_records_from_specific_voivodeship(self, voivodeship):
        return list(filter(lambda x: x["voivodeship"] == voivodeship, self._get_all_nops()))