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
    
    # Relación uno a muchos con Group
    groups = relationship("Group", back_populates="type_group")

# Model to groups
class Group(Base):
    __tablename__ = "group_"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey('type_group.id'))
    name = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Relación uno a uno con TypeGroup
    type_group = relationship("TypeGroup", back_populates="groups")
    # Relación uno a muchos con User
    users = relationship("User", back_populates="group")

# Model to users
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    user = Column(String(25))
    password = Column(String(255))
    rol = Column(Integer)
    group_id = Column(Integer, ForeignKey('group_.id'))
    routes = Column(Integer)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relación uno a uno con Group
    group = relationship("Group", back_populates="users")
    
    # Relación uno a muchos con Vehicle
    vehicles = relationship("Vehicle", back_populates="user")

#Model to type_vehicle
class TypeVehicle(Base):
    __tablename__ = "type_vehicle"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relación uno a muchos con Vehiculos
    vehicles = relationship("Vehicle", back_populates="type_vehicle")
    
class Vehicle(Base):
    __tablename__ = "vehicle"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    type_vehicle_id = Column(Integer, ForeignKey('type_vehicle.id'))
    brand = Column(String(255))
    model = Column(String(255))
    year = Column(String(4))
    registration = Column(String(10))
    image = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relación uno a uno con TypeVehicle
    type_vehicle = relationship("TypeVehicle", back_populates="vehicles")
    # Relación uno a muchos con User
    user = relationship("User", back_populates="vehicles")