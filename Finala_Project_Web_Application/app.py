from flask import Flask, request, render_template
import tweepy
import re
import pickle
from nltk.stem.snowball import SnowballStemmer
import warnings

warnings.filterwarnings('ignore')
s_stemmer = SnowballStemmer(language='english')

consumer_key = "aGgWXgGEVuTtXODmmTn5pN9BN"
consumer_secret = "7I2MgjyGcrgyXVziqFtlm3777HMH5IQA6A8A5XwMjrqdyVFOS2"
access_token = "1578553498161004544-U04dW5oNZB73iETRcaAazL8nf3Kh9n"
access_token_secret = "TW3uuJArfGnE6f02upRUBf7LeFWvGXdDC26Q2zf8bKafH"

stopwords_path = './model/stopwords.txt'
stopwords = []
with open(stopwords_path, 'r') as f:
    for line in f:
        stopwords.append(line.strip('\n'))

model_path = './model/lm.sav'
predict_model = pickle.load(open(model_path, 'rb'))
transformer_path = './model/vec_tfidf.pkl'
vec_transformer = pickle.load(open(transformer_path, 'rb'))

app = Flask(__name__)


def get_user_tweets(username):
    client = tweepy.Client(consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           access_token=access_token, access_token_secret=access_token_secret)
    user_id = client.get_user(username=username, user_auth=True).data.id
    tweets = client.get_users_tweets(id=user_id, max_results=100, user_auth=True)
    texts = []
    for tweet in tweets.data:
        texts.append(tweet.text)
    return texts


def data_process(tweets):
    total = []
    for line in tweets:
        line = line.strip().lower().split(" ")
        new_line = list(filter(lambda word: re.match('^[a-zA-Z]+$', word) != None and
                                            word not in stopwords, line))
        new_line = list(map(lambda word: s_stemmer.stem(word), new_line))
        total = total + new_line
    total = total + total
    while len(total) < 500:
        total = total + total
    text_to_predict = " ".join(total[:500])
    return text_to_predict


def predict(data_to_predict):
    return list(predict_model.predict(vec_transformer.transform([data_to_predict])))[0]


@app.route('/index')
@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/username', methods=['GET', 'POST'])
def get_username():
    username = request.form.get('username')
    print(username)
    # calculating
    try:
        tweets = get_user_tweets(username)
    except:
        return render_template("index.html")
    data_to_predict = data_process(tweets)
    result = predict(data_to_predict)
    print(result)
    if result == 'INTJ':
        return render_template("intj.html")
    elif result == 'INTP':
        return render_template("intp.html")
    elif result == 'ENTJ':
        return render_template("entj.html")
    elif result == 'ENTP':
        return render_template("entp.html")
    elif result == 'INFJ':
        return render_template("infj.html")
    elif result == 'INFP':
        return render_template("infp.html")
    elif result == 'ISFP':
        return render_template("isfp.html")
    elif result == 'ESFP':
        return render_template("esfp.html")
    elif result == 'ESFJ':
        return render_template("esfj.html")
    elif result == 'ISFJ':
        return render_template("isfj.html")
    elif result == 'ESTP':
        return render_template("estp.html")
    elif result == 'ESTJ':
        return render_template("estj.html")
    elif result == 'ISTP':
        return render_template("istp.html")
    elif result == 'ISTJ':
        return render_template("istj.html")
    elif result == 'ENFP':
        return render_template("enfp.html")
    elif result == 'ENFJ':
        return render_template("enfj.html")
    else:
        return render_template("index.html")

@app.route('/model', methods=['GET', 'POST'])
def model():
    return render_template('model.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/intj', methods=['GET', 'POST'])
def intj():
    return render_template('intj.html')


@app.route('/intp', methods=['GET', 'POST'])
def intp():
    return render_template('intp.html')


@app.route('/entj', methods=['GET', 'POST'])
def entj():
    return render_template('entj.html')


@app.route('/entp', methods=['GET', 'POST'])
def entp():
    return render_template('entp.html')


@app.route('/infj', methods=['GET', 'POST'])
def infj():
    return render_template('infj.html')


@app.route('/infp', methods=['GET', 'POST'])
def infp():
    return render_template('infp.html')

@app.route('/esfp', methods=['GET', 'POST'])
def esfp():
    return render_template('esfp.html')


@app.route('/esfj', methods=['GET', 'POST'])
def esfj():
    return render_template('esfj.html')

@app.route('/isfp', methods=['GET', 'POST'])
def isfp():
    return render_template('isfp.html')

@app.route('/isfj', methods=['GET', 'POST'])
def isfj():
    return render_template('isfj.html')

@app.route('/estp', methods=['GET', 'POST'])
def estp():
    return render_template('estp.html')

@app.route('/estj', methods=['GET', 'POST'])
def estj():
    return render_template('estj.html')

@app.route('/istp', methods=['GET', 'POST'])
def istp():
    return render_template('istp.html')

@app.route('/istj', methods=['GET', 'POST'])
def istj():
    return render_template('istj.html')

@app.route('/enfp', methods=['GET', 'POST'])
def enfp():
    return render_template('enfp.html')

@app.route('/enfj', methods=['GET', 'POST'])
def enfj():
    return render_template('enfj.html')

if __name__ == '__main__':
    app.run(debug=True)
