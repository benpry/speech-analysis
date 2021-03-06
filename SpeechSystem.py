from flask import Flask, request, jsonify, make_response
from empath import Empath
from watson_developer_cloud import ToneAnalyzerV3, SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname

app = Flask(__name__)


def empath_analytics(speech: str) -> list:
    categories_to_include = ['hate', 'cheerfulness', 'aggression', 'envy', 'anticipation', 'masculine', 'pride',
                             'dispute', 'nervousness', 'weakness', 'horror', 'swearing_terms', 'suffering', 'art',
                             'ridicule', 'optimism', 'divine', 'fear', 'religion', 'worship', 'confusion', 'death',
                             'violence', 'dominant_heirarchical', 'neglect', 'dominant_personality', 'love', 'order',
                             'sympathy', 'trust', 'deception', 'politeness', 'disgust', 'sadness', 'ugliness', 'lust',
                             'torment', 'politics', 'power', 'disappointment', 'pain', 'negative_emotion', 'competing',
                             'friends', 'achievement', 'feminine', 'positive_emotion']
    lexicon = Empath()
    results = lexicon.analyze(speech, categories=categories_to_include)
    output = {}
    for (key, value) in results.items():
        if value != 0:
            output[key] = value
    return sorted(output, key=output.get, reverse=True)[0:5]


tone_analyzer = ToneAnalyzerV3(
    version='2018-09-14',
    username='141978e4-ec25-48b8-865e-bb39e677fd52',
    password='lR72wpphXU8k',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)


@app.route('/get_speech_impression', methods=['POST'])
def get_speech_impression():
    """This method handles the http requests for the Dialogflow webhook

    """
    req = request.get_json(silent=True, force=True)
    res = impression(req['queryResult']['queryText'])

    return make_response(jsonify({'fulfillmentText': res}))


def impression(text):
    print(text)
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        'application/json').get_result()
    reply = "Some of the tones that could be perceived from that are: "
    feels = []
    print(reply)
    print(tone_analysis)
    for element in tone_analysis["document_tone"]["tones"]:
        feel = element["tone_id"].lower()
        if feel not in feels and tone_analysis["document_tone"]["tones"].index(element) != len(tone_analysis["document_tone"]["tones"]) - 1:
            feels.append(feel)
            reply += feel + ', '
        elif feel not in feels:
            reply += feel

    reply2 = ". While someone listening may be made to feel or consider: "
    second_line = False
    lst_sentiments = empath_analytics(text)
    for element in lst_sentiments:
        feel2 = element.lower()
        if feel2 not in feels and lst_sentiments.index(element) != len(lst_sentiments)-1:
            second_line = True
            feels.append(feel2)
            reply2 += element + ', '
        elif feel2 not in feels:
            second_line = True
            feels.append(feel2)
            reply2 += element

    if second_line is True:
        reply += reply2
    reply += "."
    return reply


if __name__ == '__main__':
    app.run()
