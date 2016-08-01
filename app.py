"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

"""

import os
from flask import Flask, render_template, request, redirect, url_for
import json
import ast

import sys
#sys.path.append('C:/CommuniTweet/CommuniTweet')
#import mongolab as mlab

sys.path.append('./CommuniTweet/')
import CommuniTweet.mongolab as mlab


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

sys.path.append('C:/CommuniTweet/templates')

###
# Routing for your application.
###

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def hello_post():
    query = request.form['query']
    text = mlab.Encoding(query)
    lang = request.form['lang']
    lang = lang.strip().lower()
    if mlab.AlreadyInCollectionQuery(text,lang) == "Yes":
        if mlab.AlreadyInCollectionCommunity(text,lang):
            d = mlab.FindTheMostRecentResult(text,lang)
            return redirect(url_for('results', query = text, lang = lang, date = d)) 
        else:
            Queries=mlab.chooseQueryRandomly(lang)
            return redirect(url_for('waiting_room', query1=Queries[0][0], date1=Queries[1][0], 
                query2=Queries[0][1], date2=Queries[1][1], 
                query3=Queries[0][2], date3=Queries[1][2],
                query4=Queries[0][3], date4=Queries[1][3],
                query5=Queries[0][4], date5=Queries[1][4],
                lang=lang,TooFew="False"))
    elif mlab.AlreadyInCollectionQuery(text,lang) == "Too few users":
        TooFew="True"
        Queries=mlab.chooseQueryRandomly(lang)
        return redirect(url_for('waiting_room', query1=Queries[0][0], date1=Queries[1][0], 
                query2=Queries[0][1], date2=Queries[1][1], 
                query3=Queries[0][2], date3=Queries[1][2],
                query4=Queries[0][3], date4=Queries[1][3],
                query5=Queries[0][4], date5=Queries[1][4],
                lang=lang,TooFew=TooFew))
        
    else:
        mlab.uploadToMongolab(text,lang,1)
        Queries=mlab.chooseQueryRandomly(lang)
        return redirect(url_for('waiting_room', query1=Queries[0][0], date1=Queries[1][0], 
                query2=Queries[0][1], date2=Queries[1][1], 
                query3=Queries[0][2], date3=Queries[1][2],
                query4=Queries[0][3], date4=Queries[1][3],
                query5=Queries[0][4], date5=Queries[1][4],
                lang=lang,TooFew="False"))
                
@app.route('/waiting_room/<lang>/<path:query1>_<date1>_<path:query2>_<date2>_<path:query3>_<date3>_<path:query4>_<date4>_<path:query5>_<date5>_<TooFew>')
def waiting_room(query1,date1,query2,date2,query3,date3,query4,date4,query5,date5,lang,TooFew):
    return render_template('waiting_room.html',query1=query1, date1=date1, 
                query2=query2, date2=date2, 
                query3=query3, date3=date3,
                query4=query4, date4=date4,
                query5=query5, date5=date5,
                lang=lang, TooFew=TooFew)



@app.route('/results/<path:query>_<lang>_<date>', methods=['GET','POST'])
def results(query,lang,date):
    if request.method == 'POST':
        form=ast.literal_eval(request.form['old_queries'])
        return redirect(url_for('results', query = query, lang = form["language"], date = form["date"]))
    else:
        results=mlab.downloadOtherResultsForTheQuery(query)
        communityWords=[]
        communityAccounts=[]
        communitySize=[]
        communityPercent=[]
        for i in range(0,4):
            communityWords.append(json.dumps(mlab.communityWords(query,lang,date,i)))
            communityAccounts.append(mlab.communityAccounts(query,lang,date,i))
            communitySize.append(mlab.communitySize(query,lang,date,i))
            communityPercent.append(mlab.communitySizePercent(query,lang,date,i))
        LangBeautifulString=mlab.changeLanguageCharacterString(lang)
        Languages=["Dutch","English","French","German","Italian","Spanish"]
        return render_template('results.html', results=results, communityWords = communityWords, communityAccounts=communityAccounts,
                communitySize = communitySize, communityPercent = communityPercent, 
                query = query, lang=lang, date=date, LangBeautifulString=LangBeautifulString, Languages=Languages)
        

@app.route('/about_us/')
def about_us():
    """Render the website's about page."""
    return render_template('about_us.html')

@app.route('/results/twitter_redirection1')
def twitter_redirection1():
    Community1Account=request.args.get('community1')
    return redirect("https://twitter.com/"+Community1Account,code=302)
    
@app.route('/results/twitter_redirection2')
def twitter_redirection2():
    Community2Account=request.args.get('community2')
    return redirect("https://twitter.com/"+Community2Account,code=302)
    
@app.route('/results/twitter_redirection3')
def twitter_redirection3():
    Community3Account=request.args.get('community3')
    return redirect("https://twitter.com/"+Community3Account,code=302)
    
@app.route('/results/twitter_redirection4')
def twitter_redirection4():
    Community4Account=request.args.get('community4')
    return redirect("https://twitter.com/"+Community4Account,code=302)


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


