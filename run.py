import os
from flask import Flask, render_template, request, redirect, flash, send_file, session, url_for
from io import BytesIO
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

@app.route("/interviews")
def interviews():
    interviews         = db.get_interviews_all()
    question_set_names = db.get_question_set_names()
    return render_template(
        "interviews.html", 
        collection_name    = db.INTERVIEWS,
        records            = interviews,
        fieldcatalog       = db.fieldcatalog,
        question_set_names = question_set_names)


@app.route("/update/<collection_name>/<record_id>", methods=['GET', 'POST'])
def update_record(collection_name, record_id):
    record = db.get_db_record_by_id(collection_name, record_id)
    if not record:
        entity_name = db.get_db_entity_name(collection_name)
        flash(f"{entity_name} {record_id} does not exist", "danger")
        return redirect(url_for('maintain', collection_name=collection_name))

    if request.method == 'POST':
        result = db.save_record_to_db(request, collection_name, record)
        print(*result.messages[0])
        for m in result.messages:
            flash(*m)
        # if record is empty, then the update was successful
        if not result.record:
            return redirect(url_for('maintain', collection_name=collection_name))

    return render_template(
        "maintain.html",
        collection_name=collection_name,
        records=[],
        last_record=record
    )


@app.route("/delete/<collection_name>/<record_id>", methods=['POST'])
def delete_record(collection_name, record_id):
    record = db.get_db_record_by_id(collection_name, record_id)
    if not record:
        flash(f"Record {record_id} does not exist", "danger")
    else:
        # delete record
        db.delete_db_record(collection_name, record)
        entity_name = db.get_db_entity_name(collection_name)
        flash(f"Deleted one {entity_name} record", "info")
    return redirect(url_for('maintain', collection_name=collection_name))


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))

@app.template_filter('create_data_attributes')
def _jinja2_filter_create_data_attributes(coll_fieldcat: dict, record: dict, filter_postfix: str):
    return db.create_form_data_attributes(coll_fieldcat, record, filter_postfix)


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