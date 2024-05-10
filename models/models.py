import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, text, func, Text, Enum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import MetaData

metadata = MetaData()

Base = declarative_base()

# Model to type of groups
class TypeGroup(Base):
    __tablename__ = "type_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relación uno a muchos con Group
    groups = relationship("Group", back_populates="type_group", cascade="all, delete")

# Model to groups
class Group(Base):
    __tablename__ = "group_"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey('type_group.id'))
    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Relación uno a uno con TypeGroup
    type_group = relationship("TypeGroup", back_populates="groups", cascade="all, delete")
    # Relación uno a muchos con User
    users = relationship("User", back_populates="group", cascade="all, delete")

# Model to users
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    dni = Column(String(8), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    user = Column(String(25), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('user', 'admin', 'moderator', name='user_role'), default='user') # Campo para el rol del usuario, por default USER
    group_id = Column(Integer, ForeignKey('group_.id'))
    routes = Column(Integer, default=0)
    is_active = Column(Boolean, default=False)
    activation_token = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    def verify_password(self, plain_password: str) -> bool:
        # Verifica la contraseña proporcionada con la contraseña almacenada en el modelo
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password.encode('utf-8'))
    
    # Relación uno a uno con Group
    group = relationship("Group", back_populates="users", cascade="all, delete")
    
    # Relación uno a muchos con Vehicle
    vehicles = relationship("Vehicle", back_populates="user", cascade="all, delete")
    
    # Definir relacion con image
    images = relationship("Image", back_populates="user", lazy="dynamic", cascade="all, delete")
    
    # Definir relacion con LikeDislikePost
    like_dislike_post = relationship("LikeDislikePost", back_populates="user", lazy="dynamic", cascade="all, delete")
    
    # Definir relacion con LikedislikeComment
    like_dislike_comment = relationship("LikeDislikeComment", back_populates="user", cascade="all, delete")
    
    # Definir relacion con comment
    comment = relationship("Comment", back_populates="user", cascade="all, delete")
    
    # Definir relacion con Recomendation
    recomendation = relationship("Recomendation", back_populates="user", cascade="all, delete")
    
    # Definir relacion con LikeDislikeRecomendation
    like_dislike_recomendation = relationship("LikeDislikeRecomendation", back_populates="user", cascade="all, delete")
    
    # Relación uno a muchos con Post
    posts = relationship("Post", back_populates="user", cascade="all, delete")

#Model to type_vehicle
class TypeVehicle(Base):
    __tablename__ = "type_vehicle"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relación uno a muchos con Vehiculos
    vehicles = relationship("Vehicle", back_populates="type_vehicle", cascade="all, delete")
    
class Vehicle(Base):
    __tablename__ = "vehicle"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    type_vehicle_id = Column(Integer, ForeignKey('type_vehicle.id'), nullable=False)
    brand = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    year = Column(String(4), nullable=False)
    registration = Column(String(10), nullable=False)
    image = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relación uno a uno con TypeVehicle
    type_vehicle = relationship("TypeVehicle", back_populates="vehicles", cascade="all, delete")
    
    # Relación uno a muchos con User
    user = relationship("User", back_populates="vehicles", cascade="all, delete")
    
    # Relación uno a uno con Post
    posts = relationship("Post", uselist=False, back_populates="vehicle", cascade="all, delete")
    
class Category(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relación de muchos a uno con Post
    posts = relationship("Post", back_populates="category", cascade="all, delete")

class Department(Base):
    __tablename__ = "department"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relacion de muchos a uno con City
    cities = relationship("City", back_populates="department", cascade="all, delete")
    
class City(Base):
    __tablename__ = "city"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Definir relacion con Department
    department = relationship("Department", back_populates="cities", cascade="all, delete")
    
    # Definir la relación para acceder a los Posts relacionados como ciudad de origen
    origin_posts = relationship("Post", foreign_keys="[Post.city_origin]", back_populates="origin_city", cascade="all, delete")
    
    # Definir la relación para acceder a los Posts relacionados como ciudad de destino
    destination_posts = relationship("Post", foreign_keys="[Post.city_destination]", back_populates="destination_city", cascade="all, delete")
    
    # Definir relacion con Recomendation
    recomendation = relationship("Recomendation", back_populates="city", cascade="all, delete")
    
class Post(Base):
    __tablename__ = "post"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    title = Column(String(255), nullable=False)
    date = Column(String(16), nullable=False)
    brief = Column(String(255), nullable=False) 
    content = Column(Text, nullable=False) 
    city_origin = Column(Integer, ForeignKey('city.id'), nullable=False)
    city_destination = Column(Integer, ForeignKey('city.id'), nullable=False)
    like = Column(Integer, default=0) # Contador de likes
    dislike = Column(Integer, default=0) # Contador de dislikes
    comments = Column(Integer, default=0) # Contador de comentarios
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Definir la relación con la tabla Category
    category = relationship("Category", back_populates="posts", cascade="all, delete")
    
    # Definir la relación con la tabla City como ciudad de origen
    origin_city = relationship("City", foreign_keys=[city_origin], back_populates="origin_posts", lazy="joined", cascade="all, delete")
    
    # Definir la relación con la tabla City como ciudad de destino
    destination_city = relationship("City", foreign_keys=[city_destination], back_populates="destination_posts", lazy="joined", cascade="all, delete")

    # Definir relacion con Image
    images = relationship("Image", back_populates="post", lazy="dynamic", cascade="all, delete")
    
    # Definir relacion con LikeDislikePost
    like_dislike_post = relationship("LikeDislikePost", back_populates="post", lazy="dynamic", cascade="all, delete")
    
    # Definir relacion con Comment
    comment = relationship("Comment", back_populates="post", lazy="dynamic", cascade="all, delete")
    
    # Definir relacion con Recomendation
    recomendation = relationship("Recomendation", back_populates="post", lazy="dynamic", cascade="all, delete")
    
    # Relación muchos a uno con User
    user = relationship("User", back_populates="posts", cascade="all, delete")
    
    # Relación muchos a uno con Vehicle
    vehicle = relationship("Vehicle", back_populates="posts", cascade="all, delete")
    
class Image(Base):
    __tablename__ = "image"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Definir relacion con Post
    post = relationship("Post", back_populates="images", cascade="all, delete")
    
    # Definir relacion con User
    user = relationship("User", back_populates="images", cascade="all, delete")

class LikeDislikePost(Base):
    __tablename__ = "like_dislike_post"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    action = Column(Enum('like', 'dislike'))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Definir relacion con Post
    post = relationship("Post", back_populates="like_dislike_post", cascade="all, delete")
    
    # Definir relacion con User
    user = relationship("User", back_populates="like_dislike_post", cascade="all, delete")
    
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='unique_like_post_user'),
    )

class Comment(Base):
    __tablename__ = "comment"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(Text, nullable=False)
    like = Column(Integer, default=0)
    dislike = Column(Integer, default=0)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Definir relacion con Post
    post = relationship("Post", back_populates="comment", cascade="all, delete")
    
    # Definir relacion con User
    user = relationship("User", back_populates="comment", cascade="all, delete")
    
    # Definir relacion con LikeDislikeComment
    like_dislike_comment = relationship("LikeDislikeComment", back_populates="comment", cascade="all, delete")
    
class LikeDislikeComment(Base):
    __tablename__ = "like_dislike_comment"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(Integer, ForeignKey('comment.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    action = Column(Enum('like', 'dislike'))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Definir relacion con Comment
    comment = relationship("Comment", back_populates="like_dislike_comment", cascade="all, delete")
    
    # Definir relacion con User
    user = relationship("User", back_populates="like_dislike_comment", cascade="all, delete")
    
    __table_args__ = (
        UniqueConstraint('comment_id', 'user_id', name='unique_like_comment_user'),
    )

class CategoryRecomendation(Base):
    __tablename__ = "category_recomendation"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Definir relacion con Recomendation
    recomendation = relationship("Recomendation", back_populates="category_recomendation", cascade="all, delete")
    
class Recomendation(Base):
    __tablename__ = "recomendation"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_recomendation_id = Column(Integer, ForeignKey('category_recomendation.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    name = Column(Text, nullable=False)
    detail = Column(Text, nullable=False)
    location = Column(String(255), unique=True, nullable=False)
    phone_contact = Column(String(255), unique=True, nullable=False)
    name_contact = Column(String(255), unique=True, nullable=False)
    image = Column(Text, nullable=False)
    like = Column(Integer, default=0)
    dislike = Column(Integer, default=0)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Definir relacion con CategoryRecomendation
    category_recomendation = relationship("CategoryRecomendation", back_populates="recomendation", cascade="all, delete")
    
    # Definir relacion con Post
    post = relationship("Post", back_populates="recomendation", cascade="all, delete")
    
    # Definir relacion con User
    user = relationship("User", back_populates="recomendation", cascade="all, delete")
    
    # Definir relacion con City
    city = relationship("City", back_populates="recomendation", cascade="all, delete")
    
    # Definir relacion con LikeDislikeRecomendation
    like_dislike_recomendation = relationship("LikeDislikeRecomendation", back_populates="recomendation", cascade="all, delete")
    
class LikeDislikeRecomendation(Base):
    __tablename__ = "like_dislike_recomendation"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    recomendation_id = Column(Integer, ForeignKey('recomendation.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    action = Column(Enum('like', 'dislike'))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Definir relacion con Recomendation
    recomendation = relationship("Recomendation", back_populates="like_dislike_recomendation", cascade="all, delete")
    
    # Definir relacion con User
    user = relationship("User", back_populates="like_dislike_recomendation", cascade="all, delete")
    
    __table_args__ = (
        UniqueConstraint('recomendation_id', 'user_id', name='unique_like_recomendation_user'),
    )