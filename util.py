def getface(sentiment_score):
    posi,nega,neu,mix = getsentimentscore(sentiment_score)
    print(sentiment_score)
    if posi > 80:
        return "😁"
    if nega > 80:
        return "😢"
    if neu > 80:
        return "🙂"
    if mix > 80:
        return "😖"
    return "😶"

def getsentimentscore(sentiment_score):
    posi = sentiment_score['Positive'] * 100
    nega = sentiment_score['Negative'] * 100
    neu = sentiment_score['Neutral'] * 100
    mix = sentiment_score['Mixed'] * 100
    return posi,nega,neu,mix