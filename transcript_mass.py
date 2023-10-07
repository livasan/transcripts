import scrapetube
from transcript_functions import generate_transcript,get_id,get_title,save_and_upload_file
import numpy as np
import time
import pandas as pd
import ssl

videos = scrapetube.get_channel('UCYLR1ghzYNyvfjw78raCuxA')
video_id=[]

for video in videos:
    video_id.append(video['videoId'])

print(len(video_id))

texts=[]

for id in video_id[0:1000]:
    time.sleep(np.random.choice([x / 10 for x in range(7, 22)]))
    link='https://www.youtube.com/watch?v='+id
    try:
        download_link = save_and_upload_file(get_title(id),generate_transcript(id)[0])
        print(video_id.index(id))
        texts.append([get_title(id), link, download_link])
    except:
        pass


df = pd.DataFrame(texts, columns =['title', 'video', 'text'], dtype = str)
df.to_csv('DrPhil', encoding='utf-8')
