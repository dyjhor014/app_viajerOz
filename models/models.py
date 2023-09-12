from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Model to type of groups
class TypeGroup(Base):
    __tablename__ = "type_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relación uno a uno con Group
    group = relationship("Group", uselist=False, back_populates="type_group")

# Model to groups
class Group(Base):
    __tablename__ = "group_"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey('type_group.id'), unique=True)  # Establece unique=True para una relación uno a uno
    name = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Relación uno a uno con TypeGroup
    type_group = relationship("TypeGroup", uselist=False, back_populates="group")
    user = relationship("User", uselist=False, back_populates="group")

# Model to users
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    user = Column(String(25))
    password = Column(String(255))
    rol = Column(Integer)
    group_id = Column(Integer, ForeignKey('group_.id'), unique=True)
    routes = Column(Integer)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relación uno a uno con TypeGroup
    group = relationship("Group", uselist=False, back_populates="user")