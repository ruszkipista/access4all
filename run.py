import os
from flask import Flask, render_template, request, redirect, flash, url_for
import db

# envWS.py should exist only in Development
if os.path.exists("envWS.py"):
    import envWS

app = Flask(__name__)

# take app configuration from OS environment variables
app.secret_key = os.environ.get("FLASK_SECRET_KEY")  # => Heroku Config Vars
app.config["FLASK_IP"] = os.environ.get("FLASK_IP",   "0.0.0.0")
# the source 'PORT' name is mandated by Heroku app deployment
app.config["FLASK_PORT"] = int(os.environ.get("PORT"))
app.config["FLASK_DEBUG"] = os.environ.get("FLASK_DEBUG", "False").lower() \
                            in {'1', 'true', 't', 'yes', 'y'}

# App routes
# ==============
@app.route("/")  # trigger point through webserver: "/"= root directory
def index():
    return render_template("index.html")


@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html")


@app.route("/interviews")
def interviews():
    records = db.get_interviews_all()
    if not records:
        flash("There are no records. Create one below!", 'info')
    return render_template(
        "interviews.html", 
        collection_name    = db.INTERVIEWS,
        viewfields         = db.get_viewfields(db.INTERVIEWS),
        records            = records,
        question_set_names = db.get_question_set_names()
    )


@app.route("/interviews/<record_id>", methods=['GET', 'POST'])
def update_interview(record_id):
    record_id = int(record_id)
    collection_name = db.INTERVIEWS
    record = db.get_record_by_id(collection_name, record_id)
    if not record:
        entity_name = db.get_entity_name(collection_name)
        flash(f"{entity_name} {record_id} does not exist", "danger")
        return redirect(url_for('interviews'))

    if request.method == 'POST':
        result = db.save_record_from_form_to_db(request, collection_name, record)
        for m in result.messages:
            flash(*m)
        # if record is empty, then the update was successful
        if not result.record:
            return redirect(url_for('interviews'))

    question_set_id = record.get("question_set_id", None)
    question_set = db.get_record_by_id(db.QUESTION_SETS, question_set_id)

    return render_template(
        "questions.html",
        collection_name = collection_name,
        interview       = record,
        question_set    = question_set
    )


@app.route("/delete/<collection_name>/<record_id>", methods=['POST'])
def delete_record(collection_name, record_id):
    record = db.get_record_by_id(collection_name, int(record_id))
    if not record:
        flash(f"Record {record_id} does not exist", "danger")
    else:
        # delete record
        db.delete_record(collection_name, record)
        entity_name = db.get_entity_name(collection_name)
        flash(f"Deleted one {entity_name} record", "info")
    return redirect(url_for('interviews'))


@app.route("/create/<collection_name>", methods=['POST'])
def create_record(collection_name):
    result = db.save_record_from_form_to_db(request, collection_name, {})
    for m in result.messages:
        flash(*m)
    return redirect(url_for('interviews'))


@app.route("/results")
def results():
    interviews = db.get_interviews_all()
    return render_template(
        "results.html", 
        collection_name    = db.INTERVIEWS,
        records            = interviews,
    )


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))


@app.context_processor
def context_variables():
    return dict(
        fieldcatalog = db.fieldcatalog,
        buffer = {coll: db.get_lookup_int_to_ext(coll) for coll in db.get_buffered_collections()}
    )


@app.template_filter('get_foreign_value')
def _jinja2_filter_get_foreign_value(entity_id, collection_name):
    return db.get_foreign_value(entity_id, collection_name)


# inspired by https://stackoverflow.com/questions/4830535/how-do-i-format-a-date-in-jinja2
@app.template_filter('datetime_to_str')
def _jinja2_filter_datetime_to_str(dt, format):
    if dt:
        return dt.strftime(format)
    else:
        return str()


# Run the App
# =================
if __name__ == "__main__":
    app.run(
        host=app.config["FLASK_IP"],
        port=app.config["FLASK_PORT"],
        debug=app.config["FLASK_DEBUG"],
        use_reloader=False
    )