from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import os
import assemblyai as aai
import librosa
from pyAudioAnalysis import audioSegmentation

# print('Get current working directory : ', os.getcwd())


##Dr. Todd Grande
# https://www.youtube.com/watch?v=z9fF9F5w1cI

##Irvin Yalom
# https://www.youtube.com/watch?v=7R_-KBmU5g0

# Australian Institute of Professional Counsellors
# https://www.youtube.com/watch?v=AJ4Uyf5X6Sw

# Bob Cooke
# https://www.youtube.com/watch?v=w1K9wcSwYSw

# Australian Institute of Professional Counsellors
# https://www.youtube.com/watch?v=Ew8CAr1v48M

# Dr. Todd Grande
# https://www.youtube.com/watch?v=zyIN61kQ6VY

# UofL Depression Center
# https://www.youtube.com/watch?v=dJ1eDL15_Lw

# Sean Lee
# https://www.youtube.com/watch?v=ZU5BxhTrgz4

# Eleanor Shakiba
# https://www.youtube.com/watch?v=to73DYQkApQ

# Jennifer Starr
# https://www.youtube.com/watch?v=DCdyDtWSo_g


# Julie Matthiessen and Suzi Wear from Xenium HR
# https://www.youtube.com/watch?v=ZUS_WxKAXiE

# Kristine Landiorio from Hensel coaching  & consulting
# https://www.youtube.com/watch?v=UK4U1QySDlI

# Dr. Walters
# https://www.youtube.com/watch?v=h6Cfjf_0Hko

# 8aDFvvjC6XM
# https://www.youtube.com/watch?v=8aDFvvjC6XM

# Beck Institute for Cognitive Behavior Therapy
# https://www.youtube.com/watch?v=ac5Jct33oUU&t=42s

# Beck Institute for Cognitive Behavior Therapy
# https://www.youtube.com/watch?v=ikYCr-0GAfw

# Dr Fay Short
# https://www.youtube.com/watch?v=Sy6KfsR4H8U

# Dr. Todd Grande
# https://www.youtube.com/watch?v=2WLtLY6t-zw


# Dr. Michelle Cox
# https://www.youtube.com/watch?v=wKgPxVC1GlU

# Florida Atlantic University, School of Social Work
# https://www.youtube.com/watch?v=_gPcDRVALVo

def generate_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)
    script = ""

    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            script += t + " "

    return script, len(script.split())


id = '_gPcDRVALVo'
transcript, no_of_words = generate_transcript(id)

yt = YouTube('https://www.youtube.com/watch?v=7LD8iC4NqXM&t=115s')

video = yt.streams.filter(only_audio=True).first()

out_file = video.download(output_path=os.getcwd())

base, ext = os.path.splitext(out_file)
new_file = ' '.join(base.split()[:5]) + '.mp3'

os.rename(out_file, new_file)


sound = AudioSegment.from_mp3(new_file)
sound.export(base + '.wav', format='wav')



# segments = audioSegmentation.speaker_diarization(r'C:\Users\vasya\PycharmProjects\transcript\Case study clinical example CBT： First session with a client with symptoms of depression (CBT model) [7LD8iC4NqXM].wav', n_speakers=2)
#
# audio_path=r'C:\Users\almakarenkov\PycharmProjects\transcript\Case study clinical example CBT： First session with a client with symptoms of depression (CBT model) [7LD8iC4NqXM].wav'
#
# segments = audioSegmentation.speaker_diarization(audio_path, plot_res=True,n_speakers=2, mid_window=0.5, mid_step=0.1,
# short_window=0.15)
#
#
# print(segments)
