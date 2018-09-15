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


if __name__ == "__main__":
    spch = """Do I really look like a guy with a plan, Harvey?

    I don’t have a plan …

    The mob has plans. The cops have plans.

    You know what I am, Harvey? I am a dog chasing cars… I wouldn’t know what to do with one if I caught it.

    I just do things. I am just the wrench in the gears. I hate plans.

    Yours, theirs, everyone’s. Maroni has plans. Gordon has plans.

    Schemers trying to control their worlds.

    I am not a schemer. I show the schemer how pathetic their attempts to control things really are.

    So when I say that you and your girlfriend was nothing personal, you know I am telling the truth.

    I just did what I do best. I took your plan and turned it on itself.

    Look what I have done to this city with a few drums of gas and a couple of bullets.

    Nobody panics when the expected people gets killed. Nobody panics when things go according to plan, even if the plan is horrifying.

    If I tell the press that tomorrow a gangbanger will get shot or a truckload of soldiers will be blown up, nobody panics. – because it’s all part of the plan.

    But when I say that one little old mayor will die, everybody lose their minds.

    Introduce a little anarchy, you upset the established order and everything becomes chaos.

    I am agent of chaos.

    And you know the thing about chaos Harvey?

    “IT is FAIR.”
    """
    print(empath_analytics(spch))
