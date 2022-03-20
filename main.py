from typing import Optional
from sqlalchemy.orm import Session

import crud
import models
from schemas import MusicRequest, MusicRequest
from database import SessionLocal, engine

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all music
@app.get("/musics/", response_model=list[MusicRequest])
def read_musics(db: Session = Depends(get_db)):
    musics = crud.get_musics(db)
    return musics

# Create music
@app.post("/musics/", response_model=MusicRequest)
def create_music(music: MusicRequest, db: Session = Depends(get_db)):
    return crud.create_music(db=db, music=music)

# Get music by id
@app.get("/musics/{music_id}/", response_model=MusicRequest)
def read_music(music_id: int, db: Session = Depends(get_db)):
    db_music = crud.get_music(db, music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=404, detail="music not found")
    return db_music

# Update music by id
@app.put("/musics/{music_id}/", response_model=MusicRequest)
def read_music(music_id: int, music: MusicRequest, db: Session = Depends(get_db)):
    db_music = crud.update_music(db, music=music, music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=404, detail="music not found")
    return db_music

# Get music by id
@app.delete("/musics/{music_id}/")
def read_music(music_id: int, db: Session = Depends(get_db)):
    db_music = crud.delete_music(db, music_id=music_id)
    if not db_music:
        raise HTTPException(status_code=404, detail="music not found")
    return JSONResponse(
        status_code=204,
        content= {
            "message": "Music deleted"
        }
    )

# Post image to music
@app.put("/musics/{music_id}/image/", response_model=MusicRequest)
def add_image(music_id: int, db: Session = Depends(get_db), img: UploadFile = File(...)):
    db_music = crud.get_music(db, music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=404, detail="music not found")
    
    if img.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
        raise HTTPException(status_code=404, detail="Not an image file")

    file_path = f"./upload/{img.filename}"
    with open(file_path, 'wb') as image:
        content = img.file.read()
        image.write(content)
        image.close()
    db_music = crud.update_music_with_image(db, music_id=music_id, path=file_path)
    if not db_music:
        raise HTTPException(status_code=500, detail="Failed to upload image")

    return db_music   
        