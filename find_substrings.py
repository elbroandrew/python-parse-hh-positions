import openpyxl as o
import pandas as pd

wb = o.load_workbook('hh_rabbitmq_moscow_positions.xlsx')
work_sheet = wb['Sheet1']

result_entries = []

# for row in work_sheet.iter_rows(min_row=2, max_row=work_sheet.max_row):
#     for cell in row:
#         result_entries.append(cell.value)

for cell in work_sheet['A']:
    result_entries.append(cell.value.lower())  # to lower case

result_entries = result_entries[1:]  # remove 'name' field

list_of_key_words = ['php', 'devops', 'go', 'mysql', 'python', 'ruby', 'c#', 'kotlin', 'java', 'node', 'full', 'js']

positions = ['senior', 'lead', 'junior', 'middle', 'техлид', 'начинающий', 'главный', 'старший']


def count_positions(entries: list, input_list: list) -> pd.DataFrame:
    d = dict.fromkeys(entries, 0)

    for clause in input_list:
        for key_word in entries:
            if key_word in clause:
                d[key_word] += 1

    sorted_d = dict(sorted(d.items(), key=lambda var: var[1], reverse=True))

    output = pd.DataFrame(
        {
            "Key words": sorted_d.keys(),
            "Count": sorted_d.values()
        }
    )

    return output


def dump_to_excel(some_results):
    some_results.to_excel('hh_rabbitmq_moscow_positions_cleaned_data.xlsx', index=False)


if __name__ == '__main__':
    result_key_words = count_positions(list_of_key_words, result_entries)
    dump_to_excel(result_key_words)
