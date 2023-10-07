import requests
from bs4 import BeautifulSoup
import re
from text_functions import merge_elements

from fake_headers import Headers

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import os
import datetime
import numpy as np
import time

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
gdrive = GoogleDrive(gauth)


def prompts_from_abby(url, drive=gdrive):
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )

    saved_files_info = []

    response = requests.get(url, verify=False)

    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    container_elements = soup.find_all("div", class_="Container_container__2GT6K")

    text = [i.get_text() for i in container_elements]

    pattern = r'\| Letter \d{1,2} of \d{1,2}$'

    filtered_variables = [var for var in text if not re.search(pattern, var) and var not in (
    'Load More Articles', 'SubscribeReceive Dear Abby Free Every DayEmail address:Subscribe Now')]

    result = merge_elements(filtered_variables)

    result = [i for i in result if i.startswith('DEAR ABBY:')]

    for element in result:
        # Получаем первые 30 символов элемента и используем их как название файла
        file_name = element[:30]

        # Создаем файл на Google Drive
        folder_id = '1Hm0yx0bDp3sFD9tohAku4wvE7sT5FEkJ'

        gfile = drive.CreateFile({'title': f'{file_name}', 'parents': [{'id': folder_id}]})
        gfile.SetContentString(element)
        gfile.Upload()  # Загружаем файл на Google Drive

        # Сохраняем информацию о файле в массив
        saved_files_info.append({'name': file_name, 'link': gfile['alternateLink']})

    return saved_files_info


final_info = []
for k in ['2012', '2013', '2014']:
    for i in range(1, 13):
        for j in range(1, 31):
            time.sleep(np.random.choice([x / 10 for x in range(4, 10)]))
            print([k, i, j])
            try:
                final_info.append((prompts_from_abby(f'https://www.uexpress.com/life/dearabby/{k}/{i}/{j}')))
            except:
                pass

flattened_list = [item for sublist in final_info for item in sublist]

df = pd.DataFrame(flattened_list)

df.to_csv(os.path.join(os.getcwd(), 'results_txt',
                       'DearAbbyFinal' + str(datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")) + '.csv'),
          encoding='utf-8', sep=',')
