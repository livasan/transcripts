import requests
import json

IAM_TOKEN = 't1.9euelZrJmJaNz5yLnonPzMeMzJfIjO3rnpWanpzMyZ6Ky5SVmseUzYuelpLl8_ccEHtW-e8qb14J_d3z91w-eFb57ypvXgn9zef1656VmpGdlIuOk47InJiRzJ6Um5nK7_zF656VmpGdlIuOk47InJiRzJ6Um5nK.BNq-8e3Z7igyyrmqN1PhndHSDndMqjC8oDmoA6jfi5zoWFhO8N3fZTuS7cAms9My06UCfdghCRljFj6OekHQDg'
folder_id = 'b1gjivcfmm980lodh5gs'
target_language = 'en'

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {0}".format(IAM_TOKEN)
}


def translate(text):
    body = {
        "targetLanguageCode": target_language,
        "texts": text,
        "folderId": folder_id,
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )

    text = json.loads(response.text)['translations'][0]['text']

    return text


def dialogue_translate(dialogue: str) -> str:
    '''
    :param dialogue: list of sentences
    :return: translated list of sentences
    '''
    dialogue = dialogue.split('\n')
    text = ''
    for line in dialogue:
        text += translate(line) + '\n'


    return text