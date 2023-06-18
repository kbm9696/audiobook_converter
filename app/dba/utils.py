from sqlalchemy.types import TypeDecorator, VARCHAR
import json
import logging
import os
import jsonschema
from jsonschema import validate

DB_CONF = {
    "pgsql": {
        "host": "dpg-ci5jielgkuvh0tmd81tg-a.oregon-postgres.render.com",
        "port": 5432,
        "user": "fastapi",
        "password": "xjOAmoeYgDderm2Af5DZgS3PCW9R7uwH",
        "protocol": "postgresql"
    }
}
DB_CONF_FILE = '/etc/db_conf.json'


def load_database_configuration():
    try:
        global DB_CONF
        if os.path.exists(DB_CONF_FILE):
            with open(DB_CONF_FILE) as f:
                DB_CONF = json.load(f)
        # if DB_CONF.get('pgsql') and DB_CONF.get('pgsql').get('password'):
        #     DB_CONF['pgsql']['password'] = DB_CONF['pgsql']['password']

        # DB_CONF['pgsql']['database'] = 'core'
    except ValueError as e:
        logging.error('DBA Utils : Initialization Error! Unable to load database configuration')


def build_db_string(database='testdba'):
    # load_database_configuration()
    host = ''
    if DB_CONF.get('pgsql') and DB_CONF.get('pgsql').get('host'):
        host = DB_CONF.get('pgsql').get('host')
    else:
        host = DB_CONF.get('pgsql').get('{}_db_host'.format(database))

    dburi = '{proto}://{user}:{pwd}@{server}:{port}/{db}'.format(
        proto=DB_CONF['pgsql']['protocol'],
        user=DB_CONF['pgsql']['user'],
        pwd=DB_CONF['pgsql']['password'],
        server=host,
        port=DB_CONF['pgsql']['port'],
        db=database
    )
    print('dbauri',dburi)
    #dburi = 'postgres://fastapi:xjOAmoeYgDderm2Af5DZgS3PCW9R7uwH@dpg-ci5jielgkuvh0tmd81tg-a.oregon-postgres.render.com:5432/testdba'
    #dburi = 'postgres://fastapi:xjOAmoeYgDderm2Af5DZgS3PCW9R7uwH@dpg-ci5jielgkuvh0tmd81tg-a:5432/testdba'
    return dburi


def schema_validation(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        print("Validation successful. The JSON data is valid.")
        return None
    except jsonschema.exceptions.ValidationError as ve:
        print("Validation error:")
        print(ve)
        return ve
