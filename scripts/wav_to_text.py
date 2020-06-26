import argparse
import csv
import glob
import io
import os
import sys

import pandas as pd
from tqdm import tqdm

from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums

def audition(wavs_path, input_filename, output_filename, language_code, sample_rate_hertz):
    stt("audition", wavs_path, input_filename, output_filename, language_code, sample_rate_hertz)

def audacity(wavs_path, input_filename, output_filename, language_code, sample_rate_hertz):
    stt("audacity", wavs_path, input_filename, output_filename, language_code, sample_rate_hertz)

def stt(file_type, wavs_path, input_filename, output_filename, language_code, sample_rate_hertz):    
    if file_type == 'audition':
        df = pd.read_csv(input_filename, sep='\t', encoding='utf-8')
        wav_data = zip(df['Name'].to_list(), df['Start'].to_list(), df['Duration'].to_list(), df['Time Format'].to_list(), df['Type'].to_list())
        metadata = [['Name', 'Start', 'Duration', 'Time Format', 'Type', 'Description']]
    elif file_type =='audacity':
        df = pd.read_csv(input_filename, sep='\t', encoding='utf-8', usecols=[0, 1, 2], names=['Start', 'End', 'Name'])
        # pad last two values to match audition column number
        wav_data = zip(df['Name'].to_list(), df['Start'].to_list(), df['End'].to_list(), df['End'].to_list(), df['End'].to_list())
        metadata = []

    client = speech_v1p1beta1.SpeechClient()
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        'language_code': language_code,
        'sample_rate_hertz': sample_rate_hertz,
        'encoding': encoding,
    }

    for wav_marker, start, duration, time_format, marker_type in wav_data:
        local_file_path = f'{wavs_path}/{wav_marker}.wav'
        with io.open(local_file_path, "rb") as f:
            content = f.read()
        audio = {"content": content}

        try: 
            response = client.recognize(config, audio)
            for result in response.results:
                # First alternative is the most probable result
                alternative = result.alternatives[0]
                print(u"Transcript: {}".format(alternative.transcript))
            if file_type == 'audition':
                metadata.append([wav_marker, start, duration, time_format, marker_type, alternative.transcript])
            elif file_type =='audacity':             
                metadata.append([start, duration, wav_marker, alternative.transcript])
        except Exception as err:
            metadata.append([local_file_path, "error: {0}".format(err)])

    # write out csv
    csv_out = csv.writer(open(output_filename, 'w'), delimiter='\t',
        quoting=csv.QUOTE_NONE)
    for result in metadata:
        if file_type == 'audition':
            csv_out.writerow([result[0], result[1], result[2], result[3], result[4], result[5]])
        elif file_type =='audacity': 
            csv_out.writerow([result[0], result[1], result[2], result[3]])

def execute_cmdline(argv):

    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Get transcripts from wav files',
        epilog      = 'Type "%s <command> -h" for more information.' % prog
    )

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'audition',         'Audition format', 'audition')
    p.add_argument(     '--wavs_path',  default="../test_data/wavs_export_audition")
    p.add_argument(     '--input_filename',  default="../test_data/Markers.csv")
    p.add_argument(     '--output_filename', default="../test_data/Markers_STT.csv")
    p.add_argument(     '--sample_rate_hertz', default=22050)
    p.add_argument(     '--language_code', default='en-US')

    p = add_command(    'audacity',         'Audacity format', 'audacity')
    p.add_argument(     '--wavs_path',  default="../test_data/wavs_export_audacity")
    p.add_argument(     '--input_filename',  default="../test_data/Label Track.txt")
    p.add_argument(     '--output_filename', default="../test_data/Label Track STT.txt")
    p.add_argument(     '--sample_rate_hertz', default=22050)
    p.add_argument(     '--language_code', default='en-US')

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

if __name__ == "__main__":
    execute_cmdline(sys.argv)
