import argparse
import pythoncom
import os
from MoralisSDK import ipfs
import PyPDF3
import pyttsx3
from sqlalchemy import create_engine, Column, Integer, VARCHAR, Boolean, Text, DateTime, func, NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import threading

DB_CONF = {
    "pgsql": {
        "host": "192.168.1.9",
        "port": 5432,
        "user": "postgres",
        "password": "9696",
        "protocol": "postgresql+psycopg2"
    }
}

# Database configuration
DATABASE_URI = '{proto}://{user}:{pwd}@{server}:{port}/{db}'.format(
    proto=DB_CONF['pgsql']['protocol'],
    user=DB_CONF['pgsql']['user'],
    pwd=DB_CONF['pgsql']['password'],
    server=DB_CONF['pgsql']['host'],
    port=DB_CONF['pgsql']['port'],
    db="audiobook_db"
)

api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' \
          '.eyJzdWIiOiJkaWQ6ZXRocjoweDE0RkY4NTU4MzVGMDYwZDBCRTk0ZWQyOTBjNTdiODE1YTE5MjQxNUQiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY1NzU2OTU4ODQxOSwibmFtZSI6Ik1BTklESUxMUyJ9.idaK-qJVyOb8WKP1cD0yddE8UJX4zRpBKtX-QqN49fU'

# Database model
Base = declarative_base()


def create_db_session():
    # Create database engine and session
    engine = create_engine(DATABASE_URI, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(VARCHAR(200), nullable=False)
    user_name = Column(VARCHAR(200), nullable=False)
    password = Column(VARCHAR(200), nullable=False)
    premium_user = Column(Boolean, nullable=False)
    created_time = Column(DateTime(timezone=True), default=func.now())
    uploaded_on = Column(DateTime(timezone=True), default=func.now())


class AudioBook(Base):
    __tablename__ = 'audiobook'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(200), nullable=False)
    pdf_link = Column(VARCHAR(200), nullable=False)
    audiobook_link = Column(VARCHAR(200), nullable=False)
    premium = Column(Boolean, nullable=False)
    type_of_storage = Column(VARCHAR(200), nullable=False)
    api_key_for_storage = Column(Text, nullable=False)
    status = Column(VARCHAR(200), nullable=False)
    uploaded_by = Column(VARCHAR(200), nullable=False)
    uploaded_on = Column(DateTime(timezone=True), default=func.now())


def update_status(status, aid):
    session = create_db_session()
    audiobook = session.query(AudioBook).filter(AudioBook.id == aid).first()
    audiobook.status = status
    session.commit()
    session.close()


def update_links(data, aid):
    session = create_db_session()
    audiobook = session.query(AudioBook).filter(AudioBook.id == aid).first()
    audiobook.pdf_link = data['pdf_link']
    audiobook.audiobook_link = data['audiobook_link']
    audiobook.status = data['status']
    session.commit()
    session.close()


# Function to upload PDF files and save NFT links in the database


def convert_pdf_to_audiobook(file_name, aid, api_key, storage_type='nft'):
    try:
        pythoncom.CoInitialize()
        engine = pyttsx3.init()
        book = open(file_name, 'rb')
        pdfRead = PyPDF3.PdfFileReader(book)
        # to start the reading from 1st page in the pdf
        num_of_page = pdfRead.numPages
        text = ''
        update_status('converting', aid)
        # print('converting')
        for page in pdfRead.pages:
            # to extract text to read
            text += page.extractText()
        # takes in message to read or text
        tmp_file = os.path.join(os.getcwd(), 'temp')
        tmp_file = os.path.join(tmp_file, f'{file_name.split()[0]}.mp3')

        engine.save_to_file(text, tmp_file)
        engine.runAndWait()
        print("converted", tmp_file)
        pythoncom.CoUninitialize()
        upload_all([file_name, tmp_file], aid, storage_type, api_key)
    except Exception as e:
        print(f'Got Exception while convert pdf to mp3 : {e}')


def upload_all(files, aid, storage_type, api_key):
    try:
        update_status('uploading', aid)
        data = {}
        for file in files:
            ipfs_api = ipfs.IPFS()
            ipfs_hash = ''
            print('uploading', file)
            if storage_type == 'nft':
                res = ipfs_api.upload_nft_storage(apikey=api_key, file=file)
                if type(res) == str:
                    print("error in nft ", res)
                ipfs_hash = ipfs_api.nft_storage_download_link(res.get('value').get('cid'))
            elif storage_type == 'web3':
                res = ipfs_api.upload_web3_storage(apikey=api_key, file=file)
                ipfs_hash = ipfs_api.web3_storage_download_link(res.get('cid'))
            if 'mp3' in file:
                data['audiobook_link'] = ipfs_hash
            if 'pdf' in file:
                data['pdf_link'] = ipfs_hash
            print('uploaded', file)
        data['status'] = 'uploaded'
        update_links(data, aid)
    except Exception as e:
        print('error while upload all', e)


# Function to add the admin user as a default user
def add_default_user():
    admin_user = Users(
        user_id='Admin',
        user_name='Admin',
        password='admin123',
        premium_user=True,
    )
    session = create_db_session()
    session.add(admin_user)
    session.commit()
    print("Admin user added successfully")
    session.close()


def upload_pdf(path):
    # Create a list to hold the threads
    threads = []
    eid = 0
    # Save data to the database
    for file_name in os.listdir(path):
        if file_name.endswith('.pdf'):
            audiobook = AudioBook(
                title=file_name.split('.')[0],
                pdf_link='',  # Leave empty for now, will be updated after upload
                audiobook_link='',  # Leave empty for now, will be updated after upload
                premium=False,
                type_of_storage='nft',
                api_key_for_storage= api_key,
                status='started',
                uploaded_by='Admin',
            )
            print("iohuy")
            # Base.metadata.create_all(engine)
            session = create_db_session()
            session.add(audiobook)
            session.commit()
            eid = audiobook.id

            print(f"Saved {file_name} to database")
            session.close()
        # Upload files to NFT in separate threads
        if file_name.endswith('.pdf'):
            thread = threading.Thread(target=convert_pdf_to_audiobook, args=(os.path.join(folder_path, file_name), eid,
                                                                             api_key))
            threads.append(thread)
            thread.start()

    # Wait for all threads to complete
    print('wait for while to complete the upload')
    for thread in threads:
        thread.join()

    print("PDF upload completed")


# Main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to add default user and upload PDFs')
    parser.add_argument('--add_default_user', action='store_true', help='Add default user')
    parser.add_argument('--upload_pdfs', action='store_true', help='Upload PDFs')

    args = parser.parse_args()

    if args.add_default_user:
        add_default_user()

    if args.upload_pdfs:
        folder_path = input("Enter the folder path: ")
        upload_pdf(folder_path)
    # pythoncom.CoUninitialize()
