import requests
from lxml import etree
from urllib.parse import urljoin
import random
from time import sleep
import pickle
import json
import csv


""" Parser for site: career.habr.com"""


def get_html(url, headers):
    request = requests.Session().get(url, headers=headers)
    if request.status_code in (200, 301, 302, 307):
        tree_dom = etree.HTML(requests.get(url).text)
        return tree_dom
    else:
        raise ValueError("unexpected HTTP code {}".format(request.status_code))


def wait(min_wait, max_wait):
    seconds_to_wait = round(
        random.uniform(min_wait, max_wait),
        2
    )
    sleep(seconds_to_wait)
    pass


def pagination(pagin_pages, base_url, headers):

    vacancy_list = list()

    for itm in pagin_pages:
        pag_dom = get_html(itm, headers)
        get_data_vacancy(pag_dom, base_url, vacancy_list)
        wait(0, 2)

    return vacancy_list


def get_data_vacancy(pag_dom, base_url, vacancy_list):
    vac_full_href = list()
    vac_name = pag_dom.xpath("//div[contains(@class,'job')]//div[contains(@class,'title')]//text()")
    vac_company = pag_dom.xpath("//div[contains(@class,'job')]//span[contains(@class,'company_name')]//text()")
    vac_hrefs = pag_dom.xpath("//div[contains(@class,'job')]//div[contains(@class,'title')]//a/@href")
    for itm in vac_hrefs:
        vac_full_href.append(urljoin(base_url, itm))
    vac_region = pag_dom.xpath("//div[contains(@class,'job')]//span[contains(@class,'location')]//text()")
    mrk = 0
    for name in vac_name:
        vacancy_list.append(
            {
                "Vacancy": name,
                "Company": vac_company[mrk],
                "Vacancy Href": vac_full_href[mrk],
                "Region": vac_region[mrk]
            }
        )
        mrk += 1
    return vacancy_list


def write_pickle(data):

    with open('data_habr_vacancy.pickle', 'wb') as f:
        pickle.dump(data, f)

    print("Writing habr vacancy's to pickle file complete.")


def write_json(data):
    with open('data_habr_vacancy.json', 'w', encoding='UTF16') as f:
        json.dump(data, f)

    print("Writing habr vacancy's to json file complete.")


def write_csv(data):

    with open("data_habr_vacancy.csv", "w",  encoding='UTF8', errors='replace', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            for k, v in row.items():
                writer.writerow((k, v))

    print("Writing habr vacancy's to csv file complete.")


def crawl():
    pagin_pages = list()
    base_url = "https://career.habr.com"
    headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/79.0.3945.88 Safari/537.36"}
    url_start = base_url + '/vacancies?q=python&currency=rur&location=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&city_id=678 '
    tree_dom = get_html(url_start, headers)
    pagin_href = tree_dom.xpath("//div[contains(@id,'paginator')]//a/@href")
    for itm in pagin_href[:-1]:
        pagin_pages.append(base_url+itm)
    data = pagination(pagin_pages, base_url, headers)
    write_pickle(data)
    write_json(data)
    write_csv(data)


if __name__ == '__main__':
    crawl()
