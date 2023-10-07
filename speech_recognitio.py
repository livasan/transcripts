#https://www.youtube.com/watch?v=2WLtLY6t-zw

import vosk
import wave
import youtube_dl

def download_audio(video_url, output_file):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': output_file,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

video_url = 'https://www.youtube.com/watch?v=your_video_id'
output_file = 'audio.wav'
download_audio(video_url, output_file)


def transcribe_audio(audio_file, model_path):
    model = vosk.Model(model_path)
    wf = wave.open(audio_file, 'rb')
    rec = vosk.KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            results.append(result)

    final_result = rec.FinalResult()
    if final_result:
        results.append(final_result)

    return results

audio_file = 'audio.wav'
model_path = 'path/to/model'
transcripts = transcribe_audio(audio_file, model_path)

for transcript in transcripts:
    print(transcript)


def convert_to_dialog(transcripts):
    dialog = []
    current_speaker = None
    for transcript in transcripts:
        text = transcript['text']
        speaker = 'A' if current_speaker == 'B' else 'B'
        dialog.append(f"\nSpeaker {speaker}: {text}")
        current_speaker = speaker
    return ' '.join(dialog)

# Assuming you have a list of transcript dictionaries
transcripts = [{'text': 'Hello'}, {'text': 'Hi'}, ...]
dialog = convert_to_dialog(transcripts)
print(dialog)




