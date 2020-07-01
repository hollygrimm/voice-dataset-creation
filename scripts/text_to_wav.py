import argparse
import sys

import pandas as pd

from google.cloud import texttospeech

def tts_generate(input_filename, wavs_output_path):
    df = pd.read_csv(input_filename, sep='|', encoding='utf-8', usecols=[0, 1], names=['filename', 'text_sentence'])

    for filename, text_sentence in zip(df['filename'].to_list(), df['text_sentence'].to_list()):
        print(f'filename:{filename} text_sentence:{text_sentence}')

        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text_sentence)
        voice = texttospeech.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        with open(f'{wavs_output_path}{filename}.wav', 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file {filename}.wav')

def execute_cmdline(argv):

    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Convert markers file into metadata format',
        epilog      = 'Type "%s <command> -h" for more information.' % prog
    )

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'tts_generate',         'Generate synthetic dataset from CSV', 'tts_generate')
    p.add_argument(     '--input_filename',  default="../test_data/tts_metadata.csv")
    p.add_argument(     '--wavs_output_path',  default="../test_data/tts_wavs/")

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

if __name__ == "__main__":
    execute_cmdline(sys.argv)
