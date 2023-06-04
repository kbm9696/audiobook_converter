import PyPDF3
import pyttsx3
import os
from dba.audiobookdba import AudiobookDba, AudioBook
from utils.ipfs_apis import IPFS

ipfs_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' \
             '.eyJzdWIiOiJkaWQ6ZXRocjoweDE0RkY4NTU4MzVGMDYwZDBCRTk0ZWQyOTBjNTdiODE1YTE5MjQxNUQiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY1NzU2OTU4ODQxOSwibmFtZSI6Ik1BTklESUxMUyJ9.idaK-qJVyOb8WKP1cD0yddE8UJX4zRpBKtX-QqN49fU'


class ConvertAndUpload:
    def __init__(self):
        self.dba = AudiobookDba()

    def convert_pdf_to_audiobook(self, file_name, aid):
        try:
            engine = pyttsx3.init()
            book = open(file_name, 'rb')
            pdfRead = PyPDF3.PdfFileReader(book)
            # to start the reading from 1st page in the pdf
            num_of_page = pdfRead.numPages
            text = ''
            self.dba.update_status(aid, 'converting')
            print('converting')
            for page in pdfRead.pages:
                # page = pdfRead.getPage(i)
                # to extract text to read
                text += page.extractText()
            # takes in message to read or text
            # engine.say(text)
            tmp_file = os.path.join(os.getcwd(), 'temp')
            tmp_file = os.path.join(tmp_file, f'{file_name.split()[0]}.mp3')
            engine.save_to_file(text, tmp_file)
            engine.runAndWait()
            print('convert done')
            self.upload_audiobook(tmp_file, aid)
        except Exception as e:
            print(f'Got Exception while convert pdf to mp3 : {e}')

    def upload_audiobook(self, file, aid):
        try:
            self.dba.update_status(aid, 'uploading')
            print('uploading')
            ipfs_api = IPFS()
            res = ipfs_api.upload_nft_storage(apikey=ipfs_token, file=file)
            ipfs_hash = res.get('value').get('cid')
            e = AudioBook()
            e.status = 'uploaded',
            e.audiobook_link = ipfs_hash
            data = {
                'status': 'uploaded',
                'audiobook_link': ipfs_hash
            }
            self.dba.update_data(aid, data)
            print('uploaded')
        except Exception as e:
            print('error while upload converted audiobook')

    def upload_pdf(self, file, aid):
        try:
            self.dba.update_status(aid, 'uploading')
            print('uploading')
            ipfs_api = IPFS()
            res = ipfs_api.upload_nft_storage(apikey=ipfs_token, file=file)
            ipfs_hash = res.get('value').get('cid')
            e = AudioBook()
            e.status = 'uploaded',
            e.pdf_link = ipfs_hash
            data = {
                'status': 'uploaded',
                'pdf_link': ipfs_hash
            }
            self.dba.update_data(aid, data)
            print('uploaded')
        except Exception as e:
            print('error while upload converted audiobook')

    def upload_all(self, files, aid):
        try:
            self.dba.update_status(aid, 'uploading')
            data = {}
            print('uploading')
            for file in files:
                ipfs_api = IPFS()
                res = ipfs_api.upload_nft_storage(apikey=ipfs_token, file=file)
                ipfs_hash = res.get('value').get('cid')
                if 'mp3' in file:
                    data['audiobook_link'] = ipfs_hash
                if 'pdf' in file:
                    data['pdf_link'] = ipfs_hash
            data['status'] = 'uploaded'
            self.dba.update_data(aid, data)
            print('uploaded')
        except Exception as e:
            print('error while upload converted audiobook')
