from sqlalchemy import create_engine, desc, Column, String, Text, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from embeddings import create_embedding


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    embedding = Column(Vector(768))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), 
                        nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), 
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)

Base.metadata.create_all(engine)

def get_notesDB(last_id, limit):
    try: 
        sess = Session()

        # When I send -1, it will be all notes.
        if(limit == -1):
            notes = ( sess.query(Note).where(Note.id > last_id)
            .order_by(Note.id).all() )
        else: 
            notes = ( sess.query(Note).where(Note.id > last_id)
            .order_by(Note.id).limit(limit).all() )

        return notes
    finally:
        sess.close()

def get_noteDB(id):
    try: 
        sess = Session()
        note = sess.get(Note, id)
        return note
    finally:
        sess.close()
    

def insert_noteDB(title, content):
    try:
        sess = Session()

        embedding = create_embedding(f"{title} {content}")
        new_note = Note(title=title, embedding=embedding, content=content)

        sess.add(new_note)
        sess.commit()
        sess.refresh(new_note)

        return new_note
    finally:
        sess.close()

def update_noteDB(id, title, content):
    try:
        sess = Session()
        note = sess.get(Note, id)
        if(title is not None):
            note.title = title
        if(content is not None):
            note.content = content
        
        embedding = create_embedding(f"{note.title} {note.content}")
        note.embedding = embedding
        
        sess.commit()
    finally:
        sess.close()

def delete_noteDB(id):
    try:
        sess = Session()
        note = sess.get(Note, id)
        if(note == None):
            return False
        sess.delete(note)
        sess.commit()

        return True
    finally:
        sess.close()
    

def search_wordDB(search, offset, limit):
    try:
        sess = Session()
        search_embedding = create_embedding(search)

        notes = ( sess.query(Note)
        .order_by(Note.embedding.cosine_distance(search_embedding))
        .order_by(desc(Note.updated_at))
        .offset(offset)
        .limit(limit).all() )
        
        return notes

    finally:
        sess.close()

    
    