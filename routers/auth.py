from fastapi import APIRouter

router = APIRouter()


@router.get("/auth")
def get_user():
    return {"message": "This is the auth endpoint"}
