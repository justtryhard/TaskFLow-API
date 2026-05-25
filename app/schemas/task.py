from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)