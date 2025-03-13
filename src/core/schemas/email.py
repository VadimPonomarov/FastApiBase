from pydantic import BaseModel


class MyTemplateData(BaseModel):
    title: str
    message: str
