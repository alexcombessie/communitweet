"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

"""

import os
from flask import Flask, render_template, request, redirect, url_for
import module_mongolab as mlab
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


###
# Routing for your application.
###

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def hello_post():
    text = request.form['text']
    text = text.strip().lower()
    if mlab.notAlreadyInCollectionQuery(text):
        mlab.uploadToMongolab(text)
        return render_template('index1.html')
    else:
        if mlab.notAlreadyInCollectionCommunity(text):
            return render_template('index1.html')
        else:
            return redirect(url_for('results', query = text))

@app.route('/results/<query>')
def results(query):
    communityWords1 = mlab.communityWords(query,0)
    communityWords2 = mlab.communityWords(query,1)
    communityWords3 = mlab.communityWords(query,2)
    communityWords4 = mlab.communityWords(query,3)
    communitySize1 = mlab.communitySize(query,0)
    communitySize2 = mlab.communitySize(query,1)
    communitySize3 = mlab.communitySize(query,2)
    communitySize4 = mlab.communitySize(query,3)
    communityPercent1 = mlab.communitySizePercent(query,0)
    communityPercent2 = mlab.communitySizePercent(query,1)
    communityPercent3 = mlab.communitySizePercent(query,2)
    communityPercent4 = mlab.communitySizePercent(query,3)
    return render_template('results.html', communityWords1 = json.dumps(communityWords1), communityWords2 = json.dumps(communityWords2),
        communityWords3 = json.dumps(communityWords3), communityWords4 = json.dumps(communityWords4), communitySize1 = communitySize1,
        communitySize2 = communitySize2, communitySize3 = communitySize3, communitySize4 = communitySize4,
        communityPercent1 = communityPercent1, communityPercent2 = communityPercent2, communityPercent3 = communityPercent3,
        communityPercent4 = communityPercent4, query = query)

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('results.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


if __name__ == '__main__':
    app.run(debug=True)
