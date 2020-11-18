from random import random
import random
from time import sleep
import requests
from package.storage import Storage
from package.descriptor import *


def wait(min_wait, max_wait):
    seconds_to_wait = round(
        random.uniform(min_wait, max_wait),
        2
    )
    print("In process: sleep to {} sec".format(seconds_to_wait))
    sleep(seconds_to_wait)
    pass


def save_data(data):
    storage_api = Storage()
    print("File was write. File: {}".format(storage_api.write(data)))


if __name__ == '__main__':
    print("Data acquisition process started.")
    vac_bse = dict()
    trial_sport = HabrDescriptor()
    pagination = trial_sport.get_pagination("python", 8)
    for page in pagination.pages:
        page_text = requests.get(page.url)
        wait(0, 1)
        if page_text.status_code in (200, 300, 302, 307):
            items = page.parse(page_text.text)
            for item in items:
                vac_bse[item.url] = {
                    "Vacancy": item.vacancy_name,
                    "Company": item.company_name,
                }

        else:
            raise ValueError("unexpected HTTP code {}".format(page_text.status_code))

    print("Data acquisition process is completed. Now write to file ...")
    save_data(vac_bse)

