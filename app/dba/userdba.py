from sqlalchemy import Column, Integer, DateTime, create_engine, VARCHAR, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool
import dba.utils

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(VARCHAR(200), nullable=False)
    user_name = Column(VARCHAR(200), nullable=False)
    password = Column(VARCHAR(200), nullable=False)
    premium_user = Column(Boolean, nullable=False)
    created_time = Column(DateTime(timezone=True), default=func.now())
    uploaded_on = Column(DateTime(timezone=True), default=func.now())


class UserDba():
    def __init__(self):
        engine = create_engine(dba.utils.build_db_string(), poolclass=NullPool)
        self.session = sessionmaker()
        self.session.configure(bind=engine)
        Base.metadata.create_all(engine)

    def get_all_users(self):
        s = self.session()
        result = []
        try:
            q = s.query(Users).all()
            for r in q:
                temp = r.__dict__
                temp.pop('_sa_instance_state')
                result.append(r.__dict__)
        except Exception as e:
            print(f'error while get all users from dba{e}')
        finally:
            s.close()
            return result

    def get_by_userid(self, uid):
        s = self.session()
        result = {}
        try:
            q = s.query(Users).filter_by(user_id=uid).first()
            if q:
                result = q.__dict__
                result.pop('_sa_instance_state')
        except Exception as e:
            print(f'error while get the user id:{uid} from db {e}')
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
            user = s.query(Users).filter_by(user_id=uid).first()
            if not user:
                return f'User-id:{uid} not found'
            if "username" in data:
                user.user_name = data["username"]
            if "password" in data:
                user.password = data["password"]
            s.commit()

        except Exception as err:
            s.rollback()
            print(f'Exception while update user details for{uid} : {err}')
            return f'Exception while update user details for{uid} : {err}'
        except SQLAlchemyError as err:
            s.rollback()
            print(f'SQL Error while update user details for{uid} : {err}')
            return f'SQL Error while update user details for{uid} : {err}'
        finally:
            s.close()
            return ''
