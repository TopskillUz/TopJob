from typing import Annotated

from fastapi import APIRouter, Depends

from utils.deps import require_user

router = APIRouter()


@router.get("/")
def get_resume(current_user: Annotated[dict, Depends(require_user("read_user"))]):
    print(12, current_user)
