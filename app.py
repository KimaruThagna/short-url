import random, string
from flask import current_app as app
from flask import request, redirect, jsonify
from .models import db, UrlRecord, UrlStats

@app.route('/url/<shortcode>', methods=['GET'])
def url_shortcode_redirect(shortcode):
    # retrieve url record using shortcode
    url_obj = UrlRecord.query.filter_by(shortcode=shortcode).first()
    # update count
    stats_obj = UrlStats.query.filter_by(Urlrecord=url_obj).first()
    stats_obj.update_access_count()
    #redirect using main url
    return redirect(url_obj.url)

@app.route('/', methods=['POST'])
def url_record():
    short_code = ''.join(random.choice(string.ascii_uppercase + 
                                       string.ascii_lowercase + 
                                       string.digits) for _ in range(6))
    #check for shortcode if not, create and save record
    pass

@app.route('/url/<shortcode>/stats', methods=['GET'])
def url_shortcode_stats(shortcode):
    #retrieve stats from stats and record table
    url_obj = UrlRecord.query.filter_by(shortcode=shortcode).first()
    stats_obj = UrlStats.query.filter_by(Urlrecord=url_obj).first()
    stats = {
        "registered_on": url_obj.created_on,
        "last_accessed_on": stats_obj.updated_on,
        "access_count": stats_obj.access_count
    }
    return jsonify(stats)
    