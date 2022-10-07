from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

# for rabbitmq search Moscow
#hh_url = 'https://hh.ru/search/vacancy?text=rabbitmq&from=suggest_post&area='
hh_url = 'https://hh.ru/search/vacancy?text=rabbitmq&salary=&clusters=true&area=1&page='
end_line = '&hhtmFrom=vacancy_search_list'
headers = {"User-Agent": "Mozilla/5.0"}


def find_all_items(url: str, number_of_pages: int):
    results: list = []
    for page in range(number_of_pages + 1):
        response = requests.get(url + f"{page}" + end_line, headers=headers)
        soup = bs(response.content, 'html.parser')
        results += soup.find_all('div', {'class': 'serp-item'})

    return results


def get_result_names(input_text: list):
    names = []
    for result in input_text:
        try:
            names.append(result.find('a', {'class': 'serp-item__title'}).get_text())
        except Exception:
            raise Exception()

    output_result = pd.DataFrame(
        {
            'Name': names
        }
    )
    return output_result


def dump_to_excel(some_results):
    some_results.to_excel('hh_rabbitmq_moscow_positions.xlsx', index=False)


if __name__ == '__main__':
    parsed_items = find_all_items(hh_url, 15)
    output = get_result_names(parsed_items)
    dump_to_excel(output)  # pandas data frame to excel
