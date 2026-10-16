from pydantic import BaseModel


class Authorization_catalog(BaseModel):
    uid: str
    cnsOnline: bool
    buyerId: int
    child:bool