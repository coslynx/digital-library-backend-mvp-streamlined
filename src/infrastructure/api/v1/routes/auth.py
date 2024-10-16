from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.domain.users.services.user_service import UserService
from src.infrastructure.api.dependencies.database import get_db
from src.utils.exceptions import UserNotFoundError, InvalidCredentialsError
from src.utils.jwt_utils import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    user_service: UserService = Depends(),
):
    user = user_service.login_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
async def register_user(user: User, db: Session = Depends(get_db), user_service: UserService = Depends()):
    try:
        new_user = user_service.register_user(db, user)
        return new_user
    except HTTPException as e:
        raise e