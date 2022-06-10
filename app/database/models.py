import os
import pickle
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from decouple import config


user = config('DB_USER')
password = config('DB_PASSWORD')
host = config('DB_HOST')
port = config('DB_PORT')
database = config('DB_DATABASE')
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL, echo=True)
session = Session(engine)


metadata_pickle_filename = "mydb_metadata"
cache_path = os.path.join(os.getcwd(), ".sqlalchemy_cache")
cached_metadata = None
if os.path.exists(cache_path):
    try:
        with open(os.path.join(cache_path, metadata_pickle_filename), 'rb') as cache_file:
            cached_metadata = pickle.load(file=cache_file)
    except IOError:
        print('cache file not found - no problem, reflect as usual')
        # if you want to update the metadata and schema, you need to delete the cache file

if cached_metadata:
    Base = automap_base(declarative_base(bind=engine, metadata=cached_metadata))
else:
    Base = automap_base()
    # save the metadata for future runs
    try:
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        # make sure to open in binary mode - we're writing bytes, not str
        with open(os.path.join(cache_path, metadata_pickle_filename), 'wb') as cache_file:
            pickle.dump(Base.metadata, cache_file)
    except Exception as e:
        print('problem saving metadata to cache: ', str(e))


class Product(Base):
    __tablename__ = 'product'
    
class CoinsBalance(Base):
    __tablename__ = 'coin_balance'
    
class TransferFact(Base):
    __tablename__ = 'transfer_fact'
    
class User(Base):
    __tablename__ = 'user_account'
    
class ExchangeRequest(Base):
    __tablename__ = 'exchange_req'
    
class ProductRequest(Base):
    __tablename__ = 'product_req'
    
class Department(Base):
    __tablename__ = 'dept'
    
class ExchangeType(Base):
    __tablename__ = 'exchange_type'
    
class ProductDescription(Base):
    __tablename__ = 'product_description'
    
class Role(Base):
    __tablename__ = 'role'

class TransferFact(Base):
    __tablename__ = 'transfer_fact'
    
class RequestStatus(Base):
    __tablename__ = 'req_status'
    
Base.prepare(engine, reflect=True)