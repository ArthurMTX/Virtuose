from pydantic import BaseModel

class DomainCreationForm(BaseModel):
    name: str
    template: str