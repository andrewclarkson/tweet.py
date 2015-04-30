import os
from flask import *
from datetime import datetime
from peewee import *

app = Flask('tweet')
db = PostgresqlDatabase(os.environ['DATABASE_URL'])

class Tweet(Model):
    """
    The data type for a tweet
    """
    created = DateTimeField
    content = TextField

    class Meta:
        database = db
        db_table = 'tweets'
        order_by = ('-created',)


@app.template_filter('strftime')
def strftime(date):
        return date.strftime('%b %d, %Y')

@app.route('/', methods=['GET'])
def index():
    query = Tweet.select(Tweet.id, Tweet.content)
    tweets = list(query)
    return render_template('index.html', tweets=tweets)

@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html')

@app.route('/', methods=['POST'])
def create():
    content = request.form.get('content', None)
    if content and len(content) <= 140:
        tweet = Tweet.create(
            content = content,
            created = datetime.now()
        )
        return redirect(url_for('index'))
    else:
        return redirect(url_for('new'))
    

if __name__ == '__main__':
    app.debug = True
    db.connect()
    db.create_tables([Tweet], safe=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
