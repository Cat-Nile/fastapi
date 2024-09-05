import os
from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from model.user import PrivateUser, PublicUser, SignInUser

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as service
else:
    from service import user as service

from error import Missing, Duplicate

ACCESS_TOKEN_EXPIRE_MINUTES = 30