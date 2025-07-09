from pydantic import BaseModel

class EmailEvent(BaseModel):
    event_type: str
    user_id: int
    email: str
    template: str = "welcome"
