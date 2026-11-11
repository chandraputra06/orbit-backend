from pydantic import BaseModel

class FuzzyStatus(BaseModel):
    status: str = "not_configured"
    message: str
