import speech_recognition as sr
from pydub import AudioSegment
import os

# List all video files available
# Note that I'm not including this directory into Git
files = os.listdir('Aulas - Economia Brasileira')

# Nested sorting

files = sorted(files, key=lambda e: int(e[0:12].replace('EB   Aula', '')))

# Defining a function that transcribes each file
def TranscribeLecture(file) :
    # Loading video file
    print('Transcribing lecture {}'.format(file.replace('.mp4', '')))
    video = AudioSegment.from_file('Aulas - Economia Brasileira/'+file, format = 'mp4')
    print('File {} loaded'.format(file))
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    #audio_path = 'Audio/'+file.replace('.mp4', '.wav')

    # Is that really necessary? We need to check
    #audio.export(audio_path, format = 'wav')
    #print('{} converted and exported as .wav'.format(file.replace('.mp4', '')))

    # We need to split audio into small pieces
    #sound = AudioSegment.from_wav(audio_path)

    delta = 312600 # I think is enough
    control = True # To control while loop
    split = [] # Empty list
    lim_inf = 0 # Initial lower bound
    while control :
        split.append(audio[lim_inf:(lim_inf+delta)]) # Creating each split
        lim_inf += delta
        if lim_inf > len(audio) - 1:
            control = False

    # Reconizing
    r = sr.Recognizer()

    text = [] # Empty list to store transcriptions
    counter = 0
    for x in split:
        counter += 1
        # Export each split
        print('Split {}/{}'.format(counter, len(split)))
        x.export('Audio/current_split.wav', format = 'wav')
        # Transcribe each split
        with sr.AudioFile('Audio/current_split.wav') as source:
            audio_text = r.record(source)
            text.append(r.recognize_google(audio_text, language='pt-BR'))

    # Append into single string

    text = ' '.join(text)

    # Save transcription
    print('Transcription concluded! Exporting as txt...')
    with open('Transcription/'+file.replace('.mp4', '.txt'), 'w') as txt_file:
        txt_file.write(text)

for lecture in files :
    TranscribeLecture(lecture)