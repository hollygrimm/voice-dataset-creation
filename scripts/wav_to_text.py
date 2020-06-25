from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import glob
from tqdm import tqdm
import csv
import io
import os
import pandas as pd

def stt():
    client = speech_v1p1beta1.SpeechClient()
    language_code = 'en-US'
    sample_rate_hertz = 48000
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        'language_code': language_code,
        'sample_rate_hertz': sample_rate_hertz,
        'encoding': encoding,
    }

    metadata = [['Name', 'Start', 'Duration', 'Time Format', 'Type', 'Description']]

    df = pd.read_csv('Markers.csv', sep='\t', encoding='utf-8')
    for wav_marker, start, duration, time_format, marker_type in zip(df['Name'].to_list(), df['Start'].to_list(), df['Duration'].to_list(), df['Time Format'].to_list(), df['Type'].to_list()):
        local_file_path = f'wavs/{wav_marker}.wav'
        with io.open(local_file_path, "rb") as f:
            content = f.read()
        audio = {"content": content}

        try: 
            response = client.recognize(config, audio)
            for result in response.results:
                # First alternative is the most probable result
                alternative = result.alternatives[0]
                print(u"Transcript: {}".format(alternative.transcript))
                metadata.append([wav_marker, start, duration, time_format, marker_type, alternative.transcript])
        except Exception as err:
            metadata.append([filename, "error: {0}".format(err)])

    # write out csv
    csv_out = csv.writer(open('metadata.csv', 'w'), delimiter='\t',
        quoting=csv.QUOTE_NONE)
    for result in metadata:
        csv_out.writerow([result[0], result[1], result[2], result[3], result[4], result[5]])

if __name__ == "__main__":
    stt()
