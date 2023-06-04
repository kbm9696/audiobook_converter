import gunicorn
from gunicorn.app.base import Application, Config
from gunicorn import glogging
from gunicorn.workers import sync
from main import app
import logging
from logging.handlers import TimedRotatingFileHandler

CERTS_FILE = '/etc/certs/nginx-ca.crt'
KEY_FILE = '/etc/certs/nginx-ca.key'


class GUnicornFlaskApplication(Application):
    def __init__(self, app):
        self.usage, self.callable, self.prog, self.app = None, None, None, app

    def run(self, **options):
        self.cfg = Config()
        [self.cfg.set(key, value) for key, value in options.items()]
        return Application.run(self)

    def load(self): return self.app

if __name__ == "__main__":
    logging.basicConfig(filename='audiobook_converter.log',
                        format='%(asctime)s | %(levelname)s | %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=20)

    fh = TimedRotatingFileHandler('audiobook_converter.log', when='midnight', backupCount=5)
    fh.suffix = '%Y_%m_%d.log'
    gapp = GUnicornFlaskApplication(app)
    gapp.run(bind='{host}:{port}'.format(host='0.0.0.0', port=9075),
             workers=5, proxy_protocol= False, keyfile=KEY_FILE, certfile=CERTS_FILE)