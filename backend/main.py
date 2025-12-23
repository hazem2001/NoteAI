from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_notesDB, insert_noteDB, update_noteDB, delete_noteDB, get_noteDB, search_wordDB
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from llm import query_notes


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],         # List of allowed origins
    allow_credentials=True,        # Allow cookies/auth headers to be sent cross-origin
    allow_methods=["*"],           # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # Allow all headers
)


class CreateNote(BaseModel):
    title: str
    content: str

class UpdateNote(BaseModel):
    title: str | None = None
    content: str | None = None


def change_embedding_to_list(note):
    note.embedding = note.embedding.tolist()
    return note

@app.get("/notes")
def get_notes(last_id: int, limit: int):
    try:
        if(limit < -1):
            raise HTTPException(status_code=400, detail="Limit can't be negative. -1 return all notes.")
        notes = get_notesDB(last_id, limit)
        notes = [ change_embedding_to_list(note) for note in notes ]
        return notes
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database Error")

@app.get("/notes/{id}")
def get_note_id(id: int):
    try:
        note = change_embedding_to_list(get_noteDB(id))
        return note
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database Error")

@app.post("/notes")
def create_note(note: CreateNote):
    try:
        new_note = insert_noteDB(note.title, note.content)
        if(new_note.id != None):
            return new_note
        else:
            raise HTTPException(status_code=500, detail="Note wasn't created")
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database Error")

@app.put("/notes/{id}")
def update_note(id: int, note: UpdateNote):
    try:
        update_noteDB(id, note.title, note.content)
        return note
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database Error")

@app.delete("/notes/{id}")
def delete_note(id: int):
    try:
        deleted = delete_noteDB(id)
        if(not deleted):
            raise HTTPException(status_code=400, detail="Note Id not found")

        return True
    except SQLAlchemyError as e:
        print(e)

@app.get("/search")
def search_word(search: str, offset: int, limit: int):
    try:
        notes = search_wordDB(search, offset, limit)
        notes = [ change_embedding_to_list(note) for note in notes ]
        return notes
    except SQLAlchemyError as e:
        print(e)

@app.get("/ask-ai")
def ask_ai(query: str):
    try:
        notes = get_notesDB(0, -1)
        text = query_notes(notes, query)
        return text
    except SQLAlchemyError as e:
        print(e)


