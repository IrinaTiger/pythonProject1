from pydantic import BaseModel


class Channel(BaseModel):
    type:str
    value:str

class AuthRequestResponse(BaseModel):

    action: str
    repeatTime: int
    expireTime: int
    channel:Channel


