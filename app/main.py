# coding=utf8
# !/usr/bin/python

import logging
from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from logging.handlers import TimedRotatingFileHandler
from api.user import UsersApi, UserApi
from api.audiobook import AudiobooksApi, ConvertApi, AudiobookApi

app = Flask(__name__)

bp = Blueprint('ipfs', __name__)
api = Api(bp)

api.add_resource(UsersApi,
                 '/user',
                 endpoint='user', methods=['get', 'post'])
api.add_resource(UserApi,
                 '/user/<uid>',
                 endpoint='user-instance', methods=['get', 'patch'])
api.add_resource(AudiobooksApi,
                 '/audiobook',
                 endpoint='audiobook', methods=['get','post'])
api.add_resource(AudiobookApi,
                 '/audiobook/<aid>',
                 endpoint='audiobook_instance', methods=['get','patch'])
api.add_resource(ConvertApi,
                 '/audiobook/convert',
                 endpoint='audiobook_convert', methods=['post'])


app.register_blueprint(bp, url_prefix='/api')


@app.errorhandler(504)
def gateway_time_out(error):
    message = {
        'status': 504,
        'error': 'Gateway Time-out',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(404)
def not_found(error):
    message = {
        'status': 404,
        'error': 'Not Found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(400)
def bad_request(error):
    message = {
        'status': 400,
        'error': 'Bad Request',
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp


@app.errorhandler(503)
def service_unavailable(e):
    resp = jsonify(e.description.json)
    resp.status_code = 503
    return resp


if __name__ == "__main__":
    # logging.basicConfig(filename='/var/log/ipfs_api.log',
    #                     format='%(asctime)s | %(levelname)s | %(message)s',
    #                     datefmt='%m/%d/%Y %I:%M:%S %p',
    #                     level=20)

    # fh = TimedRotatingFileHandler('ipfs_api.log', when='midnight', backupCount=5)
    # fh.suffix = '%Y_%m_%d.log'
    # logging.info("IPFS API Server")
    app.run(host='0.0.0.0',
            port=9075) #, ssl_context=('/etc/certs/nginx-ca.crt','/etc/certs/nginx-ca.key'))
