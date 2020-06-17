import datetime
from sqlalchemy import Column, Numeric, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
engine=create_engine("sqlite:///temp.db",echo=True)

def _get_date():
    return datetime.datetime.now()

class Login_details(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    username=Column(String)
    password=Column(String)

class cust_data(Base):
    __tablename__='cust_data'
    cust_id=Column(Integer,primary_key=True)
    ssn_id=Column(Integer,unique=True,nullable=False)
    cust_name=Column(String,nullable=False)
    cust_age=Column(Integer,nullable=False)
    cust_add=Column(String,nullable=False)
    cust_state=Column(String,nullable=False)
    cust_city=Column(String,nullable=False)
    dep_amt=Column(Numeric,default=0)
    acc_type=Column(String)
    lst_up=Column(DateTime,default=_get_date())

    def __init__(self,ssn_id,cust_name,cust_age,cust_add,cust_state,cust_city):
        self.ssn_id=ssn_id
        self.cust_name=cust_name
        self.cust_age=cust_age
        self.cust_add=cust_add
        self.cust_state=cust_state
        self.cust_city=cust_city

Base.metadata.create_all(engine)