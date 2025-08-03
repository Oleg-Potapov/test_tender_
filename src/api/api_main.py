import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List
from src.api.schemas import TenderSchema
from src.repositories.tender_repository import TenderRepository


app = FastAPI()


@app.get("/tenders", response_model=List[TenderSchema])
def get_tenders():
    try:
        return TenderRepository().get_all_tenders()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
