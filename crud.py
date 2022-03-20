from sqlalchemy.orm import Session

import models, schemas


def get_music(db: Session, music_id: int):
    return db.query(models.Music).filter(models.Music.id == music_id).first()

def get_musics(db: Session):
    return db.query(models.Music).all()

def create_music(db: Session, music: schemas.MusicRequest):
    db_music = models.Music(title= music.title, artist=music.artist, year=music.year)
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return db_music

def update_music(db: Session, music: schemas.MusicRequest, music_id: int):
    db_music = db.query(models.Music).get(music_id)
    if music:
        db_music.title = music.title
        db_music.artist = music.artist
        db_music.year = music.year
        if music.album_image:
            db_music.album_image = music.album_image
        db.commit()
        db.refresh(db_music)
        return db_music

def update_music_with_image(db: Session, music_id: int, path: str):
    db_music = db.query(models.Music).get(music_id)
    if db_music:
        db_music.album_image = path
        db.commit()
        db.refresh(db_music)
        return db_music
    return False

def delete_music(db: Session, music_id: int):
    db_music = db.query(models.Music).get(music_id)
    if db_music:
        db.delete(db_music)
        db.commit()
        return True
    return False

        
