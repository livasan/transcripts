import pandas as pd
import datetime
import os
from yandex_transcribe import recognize
import assemblyai as aai
from aai_transcripotor import convert_to_dialogue, aai_trainscript, download_audio
from transcript_functions import generate_transcript, get_id, get_title, save_and_upload_file, upload_mp3_drive, \
    split_audio, save_locally

FILE_URL = "https://github.com/iskaiska911/wav_files/raw/4ac005e1a4e5cd13c10f78a9c2f98636d445c0d3/Case%20study%20clinical%20example%20CBT%20First%20session%20with%20a%20client%20with%20symptoms%20of%20depression%20(CBT%20model).mp3"
YOUR_API_TOKEN = "4cec269d03324f32b13c1abd33e61e5b"
GITHUB_TOKEN = "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"
aai.settings.api_key = f"f47232db71294e868b5cfaeae7d83346"


LinkList = [
    ('https://www.youtube.com/watch?v=dP-F8YoXyUA', 'ru'),  # RU
    ('https://www.youtube.com/watch?v=PZi1Vl2p8xw', 'en'),  # EN
    ('https://www.youtube.com/watch?v=eSzp2LxDUE8', 'ru')  # RU
]

texts = []
segment_duration = 15

for link, language in LinkList:
    id = get_id(link)
    transcript_link = None
    try:
        if language == 'ru':
            # transcript = recognize(link)
            with open('results/Открытая консультация психолога.txt', 'r', encoding='utf8') as file:
                file.readline()
                transcript = file.readline()
        else:
            transcript = generate_transcript(id)

        download_link = save_and_upload_file(get_title(id), transcript)
        file_name = download_audio(link)
        download_url = upload_mp3_drive(file_name)

        config = aai.TranscriptionConfig(speaker_labels=True, language_code='ru')
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(
            download_url,
            config=config
        )

        # transcript = aai_trainscript(api_token=YOUR_API_TOKEN, file_url=download_url)

        dialogue = convert_to_dialogue(transcript['words'])
        transcript_link = save_and_upload_file(file_name, dialogue)
        save_locally(file_name, dialogue)
        texts.append([get_title(id), link, download_link, download_url, transcript_link, 'speaker A - coach',
                      dialogue.count('Speaker B')])

    except TypeError:
        pass

df = pd.DataFrame(texts, columns=['title', 'video', 'text', 'download_url', 'transcript_link', 'flag', 'count_prompts'],
                  dtype=str)
df.to_csv(os.path.join(os.getcwd(), 'results_txt',
                       'transcrpit' + str(datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")) + '.csv'),
          encoding='utf-8', sep=',')
