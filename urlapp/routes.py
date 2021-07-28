import random, string
from flask import current_app as app
from flask import request, redirect, jsonify, Response
from .models import db, UrlRecord


@app.route("/", methods=["GET"])
def home():
    return Response("Welcome", status=200, mimetype="application/json")
    #return jsonify(list(map(lambda x: x.to_dict(), UrlRecord.query.all())))

@app.route("/url/<shortcode>", methods=["GET"])
def url_shortcode_redirect(shortcode):
    # retrieve url record using shortcode
    url_obj = UrlRecord.query.filter_by(shortcode=shortcode).first()
    if url_obj:
        # update count
        url_obj.update_access_count()
        # redirect using main url
        return redirect(url_obj.url)
    else:
        return Response(f"URL does not exist", status=404, mimetype="application/json")


@app.route("/url/add", methods=["POST"])
def url_record():
    data = request.get_json(force=True)  # incase other content type was used
    short_code = ""
    if "shortcode" in data:  # user provided their shortcode
        short_code = data["shortcode"]
        if len(short_code) < 4:
            return Response(
                f"Error. Shortcode should contain at least 4 characters",
                status=400,
                mimetype="application/json",
            )
    else:

        short_code = "".join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(6)
        )
    new_urlrecord = UrlRecord(url=data["url"], shortcode=short_code,)

    try:
        db.session.add(new_urlrecord)
        db.session.commit()  # Commits all changes
        return Response(
            "Record successfully added", status=201, mimetype="application/json"
        )
    except Exception as e:
        return Response(f"Error \n {e}", status=400, mimetype="application/json")


@app.route("/url/<shortcode>/stats", methods=["GET"])
def url_shortcode_stats(shortcode):
    # retrieve stats from stats and record table
    url_obj = UrlRecord.query.filter_by(shortcode=shortcode).first()
    if url_obj:
        stats = {
            "registered_on": url_obj.created_on,
            "last_accessed_on": url_obj.updated_on,
            "access_count": url_obj.access_count,
        }
        return jsonify(stats)
    else:
        return Response(f"URL does not exist", status=404, mimetype="application/json")
