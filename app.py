import os
from flask import Flask, render_template, request, redirect, flash, send_file, session, url_for
from io import BytesIO
import db

# envWS.py should exist only in Development
if os.path.exists("envWS.py"):
    import envWS

app = Flask(__name__)

# take app configuration from OS environment variables
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY")            # => Heroku Config Vars
app.config["FLASK_IP"] = os.environ.get("FLASK_IP",   "0.0.0.0")
# the source 'PORT' name is mandated by Heroku app deployment
app.config["FLASK_PORT"] = int(os.environ.get("PORT"))
app.config["FLASK_DEBUG"] = os.environ.get("FLASK_DEBUG", "False").lower() in {
    '1', 'true', 't', 'yes', 'y'}

# App routes
# ==============
@app.route("/")  # trigger point through webserver: "/"= root directory
def index():
    return render_template("index.html")


# Flask pattern from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_db_connection(exception):
    db.close_db_connection(exception)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))


# Run the App
# =================
if __name__ == "__main__":
    app.run(
        host=app.config["FLASK_IP"],
        port=app.config["FLASK_PORT"],
        debug=app.config["FLASK_DEBUG"],
        use_reloader=False
    )