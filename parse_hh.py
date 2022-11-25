from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

"""
All data is used only for educational purposes. Not for commercial needs.
"""

end_line = '&hhtmFrom=vacancy_search_list'
hh_url = (
'https://hh.ru/search/vacancy'
'?text=rabbitmq&'
'salary='
'&clusters='
'true&area='
'1&page='
)

hh_tag = 'serp-item'
div_tag = 'div'
title = 'serp-item__title'

vk_url = (
'https://career.habr.com/'
'companies/vk/vacancies'
'?page='
)

vk_class = "vacancy-card__title"
vk_tag = 'div'
a_tag = "a"
vk_class_title = "vacancy-card__title-link"

headers = {"User-Agent": "Mozilla/5.0"}


def find_all_items(url: str, number_of_pages: int, elem: str, tag: str):
    results: list = []
    for page in range(number_of_pages + 1):
        response = requests.get(url + f"{page}" + end_line, headers=headers)
        soup = bs(response.content, 'html.parser')
        results += soup.find_all(f"{elem}", {'class': f"{tag}"})

    return results


def get_result_names(input_text: list, tag: str, class_title: str):
    titles = []
    for result in input_text:
        try:
            titles.append(result.find(f"{tag}", {'class': f"{class_title}"}).get_text())
        except Exception:
            raise Exception()

    output_result = pd.DataFrame(
        {
            'Titles': titles
        }
    )
    return output_result


def dump_to_excel(some_results, excel_title: str):
    some_results.to_excel(f'{excel_title}.xlsx', index=False)


if __name__ == '__main__':
    parsed_items = find_all_items(vk_url, 5, vk_tag, vk_class)
    print(parsed_items)
    output = get_result_names(parsed_items, a_tag, vk_class_title)
    print(output)
    dump_to_excel(output, "habr_career__vk_jobs")  # pandas data frame to excel
