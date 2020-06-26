import argparse
import os
import sys
from shutil import copyfile, rmtree

import pandas as pd


def audition(wavs_export_path, wavs_final_path, input_filename, output_filename):
  create_metadata_and_wavs("audition", wavs_export_path, wavs_final_path, input_filename, output_filename)

def audacity(wavs_export_path, wavs_final_path, input_filename, output_filename):
  create_metadata_and_wavs("audacity", wavs_export_path, wavs_final_path, input_filename, output_filename)

def create_metadata_and_wavs(file_type, wavs_export_path, wavs_final_path, input_filename, output_filename):
  # delete and recreate wavs_final_path when rerunning
  if os.path.exists(wavs_final_path):
    rmtree(wavs_final_path)
  os.mkdir(wavs_final_path)

  fp = open(output_filename, 'w')

  if file_type == 'audition':
    df = pd.read_csv(input_filename, sep='\t', encoding='utf-8')
  elif file_type =='audacity':
    df = pd.read_csv(input_filename, sep='\t', encoding='utf-8', usecols=[2, 3], names=['Name', 'Description'])
  
  for wav_marker_name, sentence in zip(df['Name'].to_list(), df['Description'].to_list()):
    if not pd.isnull(sentence):
      print(sentence)
      wav_path_orig = str(wav_marker_name) + ".wav"
      wav_path = wav_path_orig.replace(" ", "_").replace("M", "m")
      wav_filename = wav_path.replace(".wav", "")
      copyfile(wavs_export_path + wav_path_orig, wavs_final_path + wav_path)

      fp.write(f"{wav_filename}|{sentence}|{sentence}\n")
  fp.close()

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

    p = add_command(    'audition',         'Audition format', 'audition')
    p.add_argument(     '--wavs_export_path',  default="../test_data/wavs_export_audition/")
    p.add_argument(     '--wavs_final_path',  default="../test_data/wavs/")
    p.add_argument(     '--input_filename',  default="../test_data/Markers.csv")
    p.add_argument(     '--output_filename',  default="../test_data/metadata.csv")

    p = add_command(    'audacity',         'Audacity format', 'audacity')
    p.add_argument(     '--wavs_export_path',  default="../test_data/wavs_export_audacity/")
    p.add_argument(     '--wavs_final_path',  default="../test_data/wavs/")
    p.add_argument(     '--input_filename',  default="../test_data/Label Track STT.txt")
    p.add_argument(     '--output_filename',  default="../test_data/metadata.csv")

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

if __name__ == "__main__":
    execute_cmdline(sys.argv)
