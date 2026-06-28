from pydantic import BaseModel


class Profile(BaseModel):

    name: str
    email: str
    phone: str