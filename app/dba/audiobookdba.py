from sqlalchemy import Column, Integer, DateTime, create_engine, VARCHAR, asc, text, Text, and_, or_, Boolean, cast
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool
import dba.utils

Base = declarative_base()


class AudioBook(Base):
    __tablename__ = 'audiobook'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(200), nullable=False)
    pdf_link = Column(VARCHAR(200), nullable=False)
    audiobook_link = Column(VARCHAR(200), nullable=False)
    premium = Column(Boolean, nullable=False)
    type_of_storage = Column(VARCHAR(200), nullable=False)
    status = Column(VARCHAR(200), nullable=False)
    uploaded_by = Column(VARCHAR(200), nullable=False)
    uploaded_on = Column(DateTime(timezone=True), default=func.now())


class AudiobookDba:
    def __init__(self):
        engine = create_engine(dba.utils.build_db_string(), poolclass=NullPool)
        self.session = sessionmaker()
        self.session.configure(bind=engine)
        Base.metadata.create_all(engine)

    def get_all_audiobooks(self):
        s = self.session()
        result = []
        try:
            q = s.query(AudioBook).all()
            for r in q:
                temp = r.__dict__
                temp.pop('_sa_instance_state')
                result.append(r.__dict__)
        except Exception as e:
            print(f'error while get all audiobook from dba{e}')
        finally:
            s.close()
            return result

    def get_by_audiobooks(self, uid):
        s = self.session()
        result = {}
        try:
            q = s.query(AudioBook).filter_by(id=uid).first()
            if q:
                result = q.__dict__
                result.pop('_sa_instance_state')
        except Exception as e:
            print(f'error while get the audiobook id:{uid} from db {e}')
        finally:
            s.close()
            return result

    def add(self, e):
        s = self.session()
        eid = 0
        try:
            print(e)
            s.add(e)
            # s.flush()
            s.commit()
            eid = e.id
        except Exception as err:
            s.rollback()
            print('error while insert entity', e)
        except SQLAlchemyError as err:
            s.rollback()
            print('sql error while insert entity', e)
        finally:
            s.close()
            return eid

    def update_data(self,uid,data):
        s = self.session()
        try:
            user = s.query(AudioBook).filter_by(id=uid).first()
            if not user:
                return f'audiobook-id:{uid} not found'
            if "title" in data:
                user.title = data["title"]
            if "pdf_link" in data:
                user.pdf_link = data["pdf_link"]
            if "audiobook_link" in data:
                user.audiobook_link = data["audiobook_link"]
            if "premium" in data:
                user.premium = data["premium"]
            if "status" in data:
                user.status = data["status"]
            s.commit()

        except Exception as err:
            s.rollback()
            print(f'Exception while update audiobook details for{uid} : {err}')
            return f'Exception while update audiobook details for{uid} : {err}'
        except SQLAlchemyError as err:
            s.rollback()
            print(f'SQL Error while update audiobook details for{uid} : {err}')
            return f'SQL Error while update audiobook details for{uid} : {err}'
        finally:
            s.close()
            return ''

    def update_status(self,uid,status):
        s = self.session()
        try:
            user = s.query(AudioBook).filter_by(id=uid).first()
            if not user:
                return f'audiobook-id:{uid} not found'
            user.status = status
            s.commit()

        except Exception as err:
            s.rollback()
            print(f'Exception while update audiobook details for{uid} : {err}')
            return f'Exception while update audiobook details for{uid} : {err}'
        except SQLAlchemyError as err:
            s.rollback()
            print(f'SQL Error while update audiobook details for{uid} : {err}')
            return f'SQL Error while update audiobook details for{uid} : {err}'
        finally:
            s.close()
            return ''