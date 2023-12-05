from fastapi import APIRouter, Depends, HTTPException
from routes.schemas import InNow, OutNow


router = APIRouter()


@router.get("/now/", status_code=200, response_model=OutNow)
def get_now(body: InNow):
    pass
