from sqlalchemy import Column, Integer, ForeignKey, DateTime
from server.data.database import Base
from datetime import datetime

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    record_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True, default=None)