from pydantic import BaseModel


class MusicRequest(BaseModel):
    title: str
    artist: str
    year: int
    album_image: str | None = None

    class Config:
       orm_mode = True
   