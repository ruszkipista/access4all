# this file should not exist outside of the developer's machine
#================================================================
import os
# set temporary environment variables in the development system
# Flask Web Server parameters
os.environ.setdefault("FLASK_SECRET_KEY","juyfu fytflg ufy  jfufujuvcjuhvc")  # => Heroku Config Vars
os.environ.setdefault("FLASK_IP",         "127.0.0.1")
os.environ.setdefault("PORT",             "5500")
os.environ.setdefault("FLASK_DEBUG",      "True")