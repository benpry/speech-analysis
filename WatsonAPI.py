import json
from watson_developer_cloud import ToneAnalyzerV3, SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname

from empath import Empath


def empath_analytics(speech: str) -> list:
    if speech == '':
        return []
    categories_to_include = ['hate', 'cheerfulness', 'aggression', 'envy', 'anticipation', 'masculine', 'pride',
                             'dispute', 'nervousness', 'weakness', 'horror', 'swearing_terms', 'suffering', 'art',
                             'ridicule', 'optimism', 'divine', 'fear', 'religion', 'worship', 'confusion', 'death',
                             'violence', 'dominant_heirarchical', 'neglect', 'dominant_personality', 'love', 'order',
                             'sympathy', 'trust', 'deception', 'politeness', 'disgust', 'sadness', 'ugliness', 'lust',
                             'torment', 'politics', 'power', 'disappointment', 'pain', 'negative_emotion', 'competing',
                             'friends', 'achievement', 'feminine', 'positive_emotion']
    lexicon = Empath()
    results = lexicon.analyze(speech, categories=categories_to_include)
    return sorted(results, key=results.get, reverse=True)[0:5]


tone_analyzer = ToneAnalyzerV3(
    version='2018-09-14',
    username='141978e4-ec25-48b8-865e-bb39e677fd52',
    password='lR72wpphXU8k',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

speech_to_text = SpeechToTextV1(
    username='bd3ede36-d606-47ab-86d4-c86a639764f4',
    password='Menj5Df2LKKp')


class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.text = ""

    def on_data(self, data):
        for element in data["results"]:
            self.text += element["alternatives"][0]["transcript"]
            print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def get_text(self):
        return self.text


myRecognizeCallback = MyRecognizeCallback()

with open(join(dirname(__file__), './.', 'Recording1.mp3'),
          'rb') as audio_file:
    audio_source = AudioSource(audio_file)
    speech_to_text.recognize_using_websocket(
        audio=audio_source,
        content_type='audio/mp3',
        recognize_callback=myRecognizeCallback,
        model='en-US_BroadbandModel',
        keywords=['colorado', 'tornado', 'tornadoes'],
        keywords_threshold=0.5,
        max_alternatives=3)

text = myRecognizeCallback.get_text()
print(text)

tone_analysis = tone_analyzer.tone(
    {'text': text},
    'application/json').get_result()

for element in tone_analysis["document_tone"]["tones"]:
    print(element["tone_id"])

print(" \nTones in Sentence")

# for element in tone_analysis["sentences_tone"]:
#     for tone in element["tones"]:
#         if tone["score"] > 0.75:
#             print(tone["tone_id"])

if __name__ == '__main__':
    print(empath_analytics(text))
