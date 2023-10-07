import requests
import time
from github import Github
import yt_dlp as youtube_dl

# replace with your API token
YOUR_API_TOKEN = "4cec269d03324f32b13c1abd33e61e5b"

# URL of the file to transcribe
FILE_URL = "https://github.com/iskaiska911/wav_files/raw/4ac005e1a4e5cd13c10f78a9c2f98636d445c0d3/Case%20study%20clinical%20example%20CBT%20First%20session%20with%20a%20client%20with%20symptoms%20of%20depression%20(CBT%20model).mp3"
github_token = "YOUR_GITHUB_ACCESS_TOKEN"
repo_name = "REPOSITORY_NAME"


# AssemblyAI transcript endpoint (where we submit the file)

def aai_trainscript(file_url, api_token):
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

    # request parameters where Speaker Diarization has been enabled
    data = {
        "audio_url": file_url,
        "speaker_labels": True,
        "speakers_expected": 2
    }

    # HTTP request headers
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }

    # submit for transcription via HTTP request
    response = requests.post(transcript_endpoint, json=data, headers=headers)

    # polling for transcription completion
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{response.json()['id']}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            # print the results
            # print(json.dumps(transcription_result, indent=2))
            break
        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
        else:
            time.sleep(0.2)

    return transcription_result


def convert_to_dialogue(dicts):
    dialogue = ""
    current_speaker = ""

    for d in dicts:
        speaker = d['speaker']
        text = d['text']

        if speaker != current_speaker:
            # If the speaker changes, add a new line
            dialogue += f"\nSpeaker {speaker}: {text}"
            current_speaker = speaker
        else:
            # If the speaker remains the same, concatenate the text
            dialogue += " " + text

    # Remove leading newline character
    dialogue = dialogue.lstrip('\n')

    return dialogue


# Example input dictionaries


def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            file_path = ydl.prepare_filename(info)
            file_name = file_path.replace('.webm', '.mp3')
            ydl.download([link])
            return file_name
    except:
        pass


def upload_mp3_drive(audio_file_wav, github_token=github_token):
    g = Github(github_token)
    repository = g.get_user().get_repo('audio')
    file_path = "./" + audio_file_wav
    with open(file_path, "rb") as file:
        content = file.read()

    repository.create_file(file_path, f"Initial commit{audio_file_wav}", content)

    download_url = repository.get_contents(file_path).download_url

    return download_url
