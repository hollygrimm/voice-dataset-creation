# TODO: CODE IN PROCESS

# https://cloud.google.com/text-to-speech
voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
# they have 180 voices
# can vary pitch
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/texttospeech/cloud-client/quickstart.py
