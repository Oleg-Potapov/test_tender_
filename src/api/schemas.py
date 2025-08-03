from pydantic import BaseModel


class TenderSchema(BaseModel):
    number: str
    link: str
    goods_description: str
    organizer: str
    publish_date: str
    end_date: str
