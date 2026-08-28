from pydantic import BaseModel

class Login(BaseModel):
    isUserConfirmed:bool
