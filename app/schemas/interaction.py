from pydantic import BaseModel

class InteractionBase(BaseModel):
    user_id: int
    product_id: int
    interaction_type: str

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int

    class Config:
        from_attributes = True