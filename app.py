import random, string
from flask import current_app as app
from flask import request, redirect
from .models import db, UrlRecord, UrlStats

@app.route('/url/<shortcode>', methods=['GET'])
def url_shortcode_redirect(shortcode):
    # retrieve url record using shortcode
    # redirect using main url
    pass

@app.route('/', methods=['POST'])
def url_record():
    short_code = ''.join(random.choice(string.ascii_uppercase + 
                                       string.ascii_lowercase + 
                                       string.digits) for _ in range(6))
    #check for shortcode if not, create and save record
    pass

@app.route('/url/<shortcode>/stats', methods=['GET'])
def url_shortcode_stats(shortcode):
    #retrieve stats from stats table
    pass