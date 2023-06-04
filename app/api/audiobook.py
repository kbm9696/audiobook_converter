import base64
import os

from flask import jsonify, request
from flask_restful import Resource
from dba.audiobookdba import AudioBook, AudiobookDba
from utils.ipfs_apis import IPFS
import schemas
import dba.utils
from threading import Thread
from utils.bankend import ConvertAndUpload
from utils.validation import validate_user_credentials

ipfs_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' \
             '.eyJzdWIiOiJkaWQ6ZXRocjoweDE0RkY4NTU4MzVGMDYwZDBCRTk0ZWQyOTBjNTdiODE1YTE5MjQxNUQiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY1NzU2OTU4ODQxOSwibmFtZSI6Ik1BTklESUxMUyJ9.idaK-qJVyOb8WKP1cD0yddE8UJX4zRpBKtX-QqN49fU'

headers = {
    'content-type': 'application/json',
    'Accept': 'application/json'
}


def get_current_user():
    auth = request.headers.get('Authorization')
    # Decode the base64-encoded credentials
    encoded_credentials = auth.split(' ')[-1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    # Split the credentials into username and password
    username, password = decoded_credentials.split(':')
    return username


def validate_user_access(aid):
    dba = AudiobookDba()
    data = dba.get_by_audiobooks(aid)
    if data['username'] == get_current_user():
        return True
    else:
        return False


class AudiobooksApi(Resource):
    def __init__(self):
        pass

    @validate_user_credentials
    def get(self):
        try:
            resp = {}
            audiobook_dba = AudiobookDba()
            audiobook_collections = audiobook_dba.get_all_audiobooks()
            resp = {
                'description': 'audiobook collections',
                'collections': audiobook_collections,
                'count': len(audiobook_collections)
            }
            resp = jsonify(resp)
            resp.status_code = 200
            return resp
        except Exception as e:
            print('Error while get audiobook collections')

    @validate_user_credentials
    def post(self):
        resp = {}
        try:
            audiobooks = AudioBook()
            audiobook_dba = AudiobookDba()
            req_files = request.files
            print(request.form)
            req_data = dict(request.form)
            print('ssss', req_data)
            validation_status = dba.utils.schema_validation(req_data, schemas.AUDIOBOOK_POST)
            if validation_status is not None:
                print('Validation failed for the given data', validation_status.message)
                response = {'error': 'Validation failed', 'message': str(validation_status.message)}
                resp = jsonify(response)
                resp.status_code = 400
                return resp
            req_data['premium'] = True if req_data['premium'].lower() == 'true' else False
            audiobooks.title = req_data['title']
            audiobooks.premium = req_data['premium']
            audiobooks.type_of_storage = req_data['type_of_storage']
            audiobooks.uploaded_by = get_current_user()
            # ipfs_api = IPFS()
            files = []
            for k in req_files:
                tmp_file = os.path.join(os.getcwd(), 'temp')
                tmp_file = os.path.join(tmp_file, req_files[k].filename)
                files.append(tmp_file)
                print(tmp_file)
                with open(tmp_file, 'wb+') as f:
                    req_files[k].save(f)
                print(os.getcwd())
            #     res = ipfs_api.upload_nft_storage(apikey=ipfs_token, file=tmp_file)
            #     ipfs_hash = res.get('value').get('cid')
            #     print("luhiu", ipfs_hash)
            #     if 'mp3' in tmp_file:
            #         audiobooks.audiobook_link = ipfs_hash
            #     if 'pdf' in tmp_file:
            #         audiobooks.pdf_link = ipfs_hash
            # audiobooks.status = 'uploaded'
            audiobooks.audiobook_link = ''
            audiobooks.pdf_link = ''
            audiobooks.status = 'started'
            r = audiobook_dba.add(audiobooks)
            print("id", r)
            upld = ConvertAndUpload()
            t = Thread(target=upld.upload_all, args=([files,r]))
            t.start()
            resp = jsonify(resp)
            resp.status_code = 201
            return resp
        except Exception as e:
            print(f'Got Exception while upload audiobook:{e}')
            response = {'error': f'Got Exception while upload audiobook:{e}'}
            resp = jsonify(response)
            resp.status_code = 400
            return resp


class AudiobookApi(Resource):
    def __init__(self):
        pass

    @validate_user_credentials
    def get(self, aid):
        try:
            resp = {}
            audiobook_dba = AudiobookDba()
            audiobook_data = audiobook_dba.get_by_audiobooks(aid)
            # print('audiobook_data', audiobook_data)
            if not bool(audiobook_data):
                resp = {
                    "message": "resource not found"
                }
                resp = jsonify(resp)
                resp.status_code = 404
                return resp
            resp = audiobook_data
            resp = jsonify(resp)
            resp.status_code = 200
            return resp

        except Exception as e:
            print(f'Got Exception in Get method of Audiobook:{e}')
            resp = {
                'error': f'Got Exception in Get method of Audiobook:{e}'
            }
            resp = jsonify(resp)
            resp.status_code = 400
            return resp

    @validate_user_credentials
    def patch(self, aid):
        resp = {}
        try:
            data = request.get_json()
            validation_status = dba.utils.schema_validation(data, schemas.AUDIOBOOK_PATCH)
            if validation_status is not None:
                print('Validation failed for the given data', validation_status.message)
                response = {'error': 'Validation failed', 'message': str(validation_status.message)}
                resp = jsonify(response)
                resp.status_code = 400
                return resp
            audiobook_dba = AudiobookDba()
            ret = audiobook_dba.update_data(aid, data)
            if len(ret):
                resp['error'] = ret
            resp = jsonify(resp)
            resp.status_code = 201
            return resp
        except Exception as e:
            print(f'Got Exception in patch handler:{e}')
            resp['error'] = f'Got Exception in patch handler:{e}'
            resp = jsonify(resp)
            resp.status_code = 400
            return resp


class ConvertApi(Resource):
    def __init__(self):
        pass

    @validate_user_credentials
    def post(self):
        resp = {}
        try:
            audiobooks = AudioBook()
            audiobook_dba = AudiobookDba()
            req_files = request.files['pdf']
            # print(req_files[0])
            req_data = dict(request.form)
            print('ssss', req_data)
            validation_status = dba.utils.schema_validation(req_data, schemas.AUDIOBOOK_POST)
            if validation_status is not None:
                print('Validation failed for the given data', validation_status.message)
                response = {'error': 'Validation failed', 'message': str(validation_status.message)}
                resp = jsonify(response)
                resp.status_code = 400
                return resp
            req_data['premium'] = True if req_data['premium'].lower() == 'true' else False
            audiobooks.title = req_data['title']
            audiobooks.premium = req_data['premium']
            audiobooks.type_of_storage = req_data['type_of_storage']
            audiobooks.uploaded_by = get_current_user()
            ipfs_api = IPFS()
            tmp_file = os.path.join(os.getcwd(), 'temp')
            tmp_file = os.path.join(tmp_file, req_files.filename)
            print(tmp_file)
            with open(tmp_file, 'wb+') as f:
                req_files.save(f)
            # res = ipfs_api.upload_nft_storage(apikey=ipfs_token, file=tmp_file)
            # ipfs_hash = res.get('value').get('cid')
            # if 'pdf' in tmp_file:
            #     audiobooks.pdf_link = ipfs_hash
            audiobooks.status = 'started'
            audiobooks.audiobook_link = ''
            audiobooks.pdf_link = ''
            r = audiobook_dba.add(audiobooks)
            cvrt = ConvertAndUpload()
            t = Thread(target=cvrt.convert_pdf_to_audiobook, args=(tmp_file, r))
            t.start()
            t1 = Thread(target=cvrt.upload_pdf, args=(tmp_file,r))
            t1.start()
            print("id", r)
            resp = jsonify(resp)
            resp.status_code = 201
            return resp
        except Exception as e:
            print(f'Got Exception while upload audiobook:{e}')
            response = {'error': f'Got Exception while upload audiobook:{e}'}
            resp = jsonify(response)
            resp.status_code = 400
            return resp
