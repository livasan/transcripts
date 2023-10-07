import math
from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydub import AudioSegment
import datetime
import os



YOUR_API_TOKEN = "4cec269d03324f32b13c1abd33e61e5b"

youtube_key = 'AIzaSyBSeg4fvSt7OXUHPGLmHHqiNmQqBg6UMeI'
api_service_name = 'youtube'
api_version = 'v3'

gauth = GoogleAuth()
gauth.LocalWebserverAuth()


def generate_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)

    script = ""

    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            script += t + " "

    return script



def get_id(link):
    id = link[link.index('=') + 1:]
    return id


def get_title(id):
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=youtube_key)
    request = youtube.videos().list(part='snippet', id=id)
    response = request.execute()
    return response['items'][0]['snippet']['title']


def save_and_upload_file(file_name, file_content=None):
    folder_id = '1Hm0yx0bDp3sFD9tohAku4wvE7sT5FEkJ'
    file_name = file_name.replace('.mp3', '.txt')
    try:
        drive = GoogleDrive(gauth)
        my_file = drive.CreateFile({'title': f'{file_name}', 'parents': [{'id': folder_id}]})
        my_file.SetContentString(file_content)
        my_file.Upload()
        file_id = my_file['id']
        download_url = f"https://drive.google.com/uc?id={file_id}"

        return download_url

    except Exception:
        return 'Something went wrong'


def upload_mp3_drive(file_name):
    folder_id = '1Hm0yx0bDp3sFD9tohAku4wvE7sT5FEkJ'
    try:
        drive = GoogleDrive(gauth)
        my_file = drive.CreateFile({'title': f'{file_name}', 'parents': [{'id': folder_id}]})
        my_file.SetContentFile(file_name)
        my_file.Upload()
        file_id = my_file['id']
        download_url = f"https://drive.google.com/uc?id={file_id}"
        return download_url
    except Exception:
        return 'Something went wrong'


def split_audio(audio_filename, segment_duration=70 * 60 * 1000):
    audio = AudioSegment.from_file(audio_filename)
    segments = []
    segments_name = []
    num_segments = int(math.ceil(audio.duration_seconds * 1000) / segment_duration)
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, len(audio))
        segments.append(audio[start_time:end_time])

    for i, segment in enumerate(segments):
        segment.export(f"{audio_filename}_{i + 1}.mp3", format="mp3")
        segments_name.append(f"{audio_filename}_{i + 1}.mp3")

    return segments_name


def save_locally(file_name, content):
    txt_file = file_name + '.txt'
    with open(os.path.join(os.getcwd(), 'results', txt_file), "w", encoding='utf8') as file:
        # Write the content to the file
        file.write(content)
