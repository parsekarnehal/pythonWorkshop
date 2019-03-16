from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


def scoreAnalyser(sentence):
    score = analyser.polarity_scores(sentence)
    print(score['compound'])


scoreAnalyser("The movie was very good")
