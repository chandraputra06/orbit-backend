from pydantic import BaseModel

class CustomerRFMResponse(BaseModel):
    customer_id: str
    recency: int
    frequency: int
    monetary: float
