# this file should not exist outside of the developer's machine
#================================================================
import os
# set temporary environment variables in the development system
# MongoDB in the cloud parameters
os.environ.setdefault("MONGO_DB_USER",    'root')              # => Heroku Config Vars
os.environ.setdefault("MONGO_DB_PASS",    'xxxxxxxxxxxxxxxx')  # => Heroku Config Vars
os.environ.setdefault("MONGO_CLUSTER",    'cluster0')          # => Heroku Config Vars
os.environ.setdefault("MONGO_DB_NAME",    'access4all')        # => Heroku Config Vars
os.environ.setdefault("MONGO_INIT",       "False")             # => Heroku Config Vars