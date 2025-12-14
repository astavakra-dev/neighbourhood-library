from sqlalchemy import Column, Integer, String
from server.data.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_no = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)