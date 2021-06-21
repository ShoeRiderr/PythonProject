import NopModel

nops = NopModel.Model()

# zad 2
file = open("odpowiedzi.txt", "w")

file.write(f"All NOP's: {nops.count_loaded_nops()}\n")

file.write(f"Results concerning women's NOP's: {nops.count_womens_loaded_in_nops()}\n")

file.write(f"Results concerning men's NOP's: {nops.count_mens_loaded_in_nops()}\n")

# zad 3
file.write(f"Number of people with fever in pomerania: {nops.count_people_with_fever_in_pomeranian_voivodeship()}\n")

file.close()


# zad 4
file = open('zestawienie.txt', 'w')

for k, v in nops.statement_showing_amount_of_nops_in_voivodeships().items():
    file.write(f"{k}: {v}\n")

file.close()


# zad 5
file = open('pomorskie.txt', 'w')
file.write("Quantitative statistic of nops in pomerania region:\n\n")
for k, v in nops.quantitative_statistics_of_nop_symptoms_in_pomerania().items():
    file.write(f"{k}: {v}\n")

file.close()

# zad 6
nops.create_pie_chart_of_occurrence_of_nops_depending_on_gender()

# zad 7
nops.create_bar_graph_of_amount_of_each_symptoms()

# zad 8
nops.create_line_chart_showing_number_of_nops_in_time()