# Voice Dataset Creation

## Create Transcriptions for Existing Voice Recordings
* Create GCP Compute Engine Instance
* Under `Cloud API access scopes` select `Allow full access to all Cloud APIs`


### Installation
Create Conda Environment

```bash
conda create -n stt python=3.7
conda activate stt
pip install google-cloud-speech tqdm pandas
```

### Mark the Speech in Audition
* Open audio file in Adobe Audition
* Select `Diagnostics` -> `Mark Audio`
* Select the `Mark the Speech` preset
* Click `Scan`
* Click `Find Levels`
* Click `Mark All`

### Export Markers and WAVs from Audition
* Open `Markers` Tab
* Adjust markers, removing silence and noise to make clip length between 3 to 10 seconds long
* Select all markers in list
* Select `Export Selected Markers to CSV` and save as Markers.csv
* Select `Export Audio of Selected Range Markers` with the following options: 
    * Check `Use marker names in filenames`
    * Update Format to `WAV PCM`
    * Update Sample Type `22050 Hz Mono, 16-bit`
    * Use folder name `wavs_export`

### Create Initial Transcriptions with STT
Create Markers_STT.csv file:
```bash
python wav_to_text.py audition
```
### Fine-tune Transcriptions in Audition
* Delete all markers
* Import the Markers file with STT transcriptions: Markers_STT.csv
* Fine-tune the Description field in Markers to exactly match the words spoken

### Export Markers and WAVs from Audition
* Select all markers in list
* Select `Export Selected Markers to CSV` and save as Markers.csv
* Select `Export Audio of Selected Range Markers` with the following options: 
    * Check `Use marker names in filenames`
    * Update Format to `WAV PCM`
    * Update Sample Type `22050 Hz Mono, 16-bit`
    * Use folder name `wavs_export`

### Create metadata file in LJSpeech Format
Using the exported Markers.csv and WAVs in wavs_export, `markersfile_to_metadata.py` will create a metadata.csv and folder of WAVs to train your favorite TTS model:

```bash
python markersfile_to_metadata.py audition
```


*******
TODO Add SNR utility