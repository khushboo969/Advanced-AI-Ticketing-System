from sqlalchemy import Column, Integer, String
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    category = Column(String)
    severity = Column(String)
    status = Column(String)
    department = Column(String)

# 🔥 NEW TABLE
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    skill = Column(String)
    availability = Column(String)  # Available / Busy
    ticket_load = Column(Integer)