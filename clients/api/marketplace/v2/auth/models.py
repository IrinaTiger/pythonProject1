from pydantic import BaseModel


class LoginResponse(BaseModel):
    isUserConfirmed: bool
