def getface(sentiment_score):
    if sentiment_score is None:
        return "";
    posi,nega,neu,mix = getsentimentscore(sentiment_score)
    # 感情を読み取ってアイコンを変更する
    printout("You:",posi,nega,neu,mix)
    # if posi > 90:
    #     return ""
    return ""


def getaiface(sentiment_score):
    if sentiment_score is None:
        return None;
    posi,nega,neu,mix = getsentimentscore(sentiment_score)
    # 感情を読み取ってアイコンを変更する
    printout("AI:",posi,nega,neu,mix)
    # if posi > 80:
    #     return ""
    return ""

def getsentimentscore(sentiment_score):
    posi = sentiment_score['Positive'] * 100
    nega = sentiment_score['Negative'] * 100
    neu = sentiment_score['Neutral'] * 100
    mix = sentiment_score['Mixed'] * 100
    return posi,nega,neu,mix

def printout(w,posi,nega,neu,mix):
    print(w)
    print("  Positive = ", posi)
    print("  Negative = ", nega)
    print("  Neutral = ", neu)
    print("  Mixed = ", mix)

# Simple exception class
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv