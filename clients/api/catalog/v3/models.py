from pydantic import BaseModel



class CatalogLoginResponse(BaseModel):
    uid: str
    cnsOnline: bool
    buyerId: int
    child:bool