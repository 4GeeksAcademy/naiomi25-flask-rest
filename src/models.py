from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Boolean ,Table,Column
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

conexion = Table (
    
    'conexion',
    db.metadata,
    Column('post_id',ForeignKey('post.id'),primary_key=True),
    Column("tag_id",ForeignKey("tag.id"),primary_key=True)
    
    )

class User(db.Model):
    
    __tablename__ = 'usuario'
    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]= mapped_column(nullable=False,unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    posts : Mapped [List['Post']] = relationship (back_populates = 'author')
    
    comments: Mapped [List ['Comment']] = relationship( back_populates= 'user_comment')
    


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name" : self.name
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    
    __tablename__ = 'post'
    
    id:Mapped[int]=mapped_column(primary_key = True)
    caption: Mapped[str] = mapped_column(String(150),nullable= False )
    image : Mapped[str] = mapped_column(nullable= False)
    
    user_id :Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    author :Mapped['User'] = relationship(back_populates= 'posts')
    postComment :Mapped [List ['Comment']] = relationship(back_populates= 'comment')
    tags : Mapped[List['Tag']]= (relationship(secondary='conexion',back_populates='posts'))
    
    
    def serialize(self):
        return {
            "id": self.id,
            'caption': self.caption,
            'image' : self.image
        }
    
class Comment(db.Model):
    
    __tablename__ = 'comment'
    
    id : Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(100) ,nullable= True)
    post_id :Mapped[int] = mapped_column(ForeignKey('post.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey ('usuario.id'))
    
    user_comment : Mapped['User'] = relationship(back_populates= 'comments')
    comment :Mapped['Post'] = relationship(back_populates= 'postcomment')
    
    
    
    def serialize (self):
        return{
            "id": self.id,
            'content' : self.content
         }
        
class Tag(db.Model):
    __tablename__ = 'tag'
    
    id : Mapped[int]= mapped_column(primary_key=True)
    name : Mapped[str]= mapped_column(nullable=False,unique=True)
    
    posts : Mapped[List['Post']] = relationship(secondary='conexion',back_populates='tags')
   
    
    def serialize(self):
        return {
        "id": self.id,
        'name':self.name
        }
    
    
