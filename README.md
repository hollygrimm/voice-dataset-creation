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

### Mark the Speech
In **Audition**, open audio file:
* Select `Diagnostics` -> `Mark Audio`
* Select the `Mark the Speech` preset
* Click `Scan`
* Click `Find Levels`
* Click `Scan` again
* Click `Mark All`

Or, in **Audacity**, open audio file:
* Select `Analyze`->`Sound Finder`

### Export Markers/Labels and WAVs
In **Audition**:
* Open `Markers` Tab
* Adjust markers, removing silence and noise to make clip length between 3 to 10 seconds long
* Select all markers in list
* Select `Export Selected Markers to CSV` and save as Markers.csv
* Select `Preferences` -> `Media & Disk Cache` and Untick `Save Peak Files`
* Select `Export Audio of Selected Range Markers` with the following options: 
    * Check `Use marker names in filenames`
    * Update Format to `WAV PCM`
    * Update Sample Type `22050 Hz Mono, 16-bit`
    * Use folder name `wavs_export`

Or, in **Audacity**:
* Select `Export multiple...`
    * Format: WAV
    * Options: Signed 16-bit PCM
    * Split files based on Labels
    * Name files using Label/Track Name
    * Use folder name `wavs_export`
* Select `Export labels` to `Label Track.txt`

### Create Initial Transcriptions with STT
For **Audition**, use `Markers.csv` and wavs folder to run:
```bash
python wav_to_text.py audition
```
For **Audacity**, use `Label Track.txt` and wavs folder to run:
```bash
python wav_to_text.py audacity
```

### Fine-tune Transcriptions
For **Audition**:
* Delete all markers
* Select `Import Markers from File` and select file with STT transcriptions: Markers_STT.csv
* Fine-tune the Description field in Markers to exactly match the words spoken

For **Audacity**:
* Open `Label Track STT.txt` in a text editor.
* Fine-tune the Labels to exactly match the words spoken

### Export Markers and WAVs from Audition
For **Audition**:
* Select all markers in list
* Select `Export Selected Markers to CSV` and save as Markers.csv
* Select `Export Audio of Selected Range Markers` with the following options: 
    * Check `Use marker names in filenames`
    * Update Format to `WAV PCM`
    * Update Sample Type `22050 Hz Mono, 16-bit`
    * Use folder name `wavs_export`

For **Audacity**:
* Select `Export multiple...`
    * Format: WAV
    * Options: Signed 16-bit PCM
    * Split files based on Labels
    * Name files using Label/Track Name
    * Use folder anem `wavs_export`

### Create metadata file in LJSpeech Format
Using the exported `Markers.csv`/`Label Track STT.txt` and WAVs in wavs_export, `markersfile_to_metadata.py` will create a metadata.csv and folder of WAVs to train your favorite TTS model:

For **Audition**:
```bash
python markersfile_to_metadata.py audition
```

For **Audacity**:
```bash
python markersfile_to_metadata.py audacity
```

***
TODO Add SNR colab

***
TODO Steps to create dataset synthetically
