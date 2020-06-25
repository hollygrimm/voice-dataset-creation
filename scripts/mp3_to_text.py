from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import glob
from tqdm import tqdm
import csv
import io
import os

def sample_recognize():
    client = speech_v1p1beta1.SpeechClient()
    language_code = "en-US"
    sample_rate_hertz = 48000
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }

    wavfiles = [f for f in glob.glob("/home/grimmh/datasets/speech/Final_Exports/*/*.wav")]

    metadata = []

    for local_file_path in tqdm(wavfiles):
        with io.open(local_file_path, "rb") as f:
            content = f.read()
        audio = {"content": content}

        #TODO: Split local_file_path and remove the wav path
        filename = os.path.splitext(os.path.split(local_file_path)[-1])[0]

        try: 
            response = client.recognize(config, audio)
            for result in response.results:
                # First alternative is the most probable result
                alternative = result.alternatives[0]
                print(u"Transcript: {}".format(alternative.transcript))
                metadata.append([filename, alternative.transcript])
        except Exception as err:
            metadata.append([filename, "error: {0}".format(err)])

    # write out csv
    csv_out = csv.writer(open('metadata.csv', 'w'), delimiter='|',
        quoting=csv.QUOTE_NONE)
    for result in metadata:
        csv_out.writerow([result[0], result[1]])

if __name__ == "__main__":
    sample_recognize()
