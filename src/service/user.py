from datetime import timedelta, datetime
import os
from jose import jwt
import jwt
import bcrypt


from model.user import PublicUser, PrivateUser, SignInUser

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as data
else:
    from fake import user as data

# --- 새로운 인증 관련 코드
# SECRET 키는 반드시 바꾸고 배포해야한다.
SECRET_KEY = "keep-it-secret-keep-it-safe"
ALGORITHM = "HS256"


def verify_password(plain: str, hash: str) -> bool:
    """plain을 해시 값과 데이터베이스의 hash 값과 비교한다."""
    password_bytes = plain.encode('utf-8')
    hash_bytes = hash.encode('utf-8')
    is_valid = bcrypt.checkpw(password_bytes, hash_bytes)
    return is_valid

def get_hash(plain: str) -> str:
    """plain의 해시값을 반환한다."""
    password_bytes = plain.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def get_jwt_username(token: str) -> str | None:
    """JWT 접근 토큰으로부터 username을 반환한다."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None

    return username

def get_current_user(token: str) -> PublicUser | None:
    """OAuth 토큰을 풀어서 PublicUser를 반환한다."""
    if not (username := get_jwt_username(token)):
        return None
    if user := lookup_user(username):
        return user

    return None

def lookup_user(username: str, is_public=True) -> PublicUser | PrivateUser | None:
    """데이터베이스에서 username에 매칭되는 User를 반환한다.
    is_public이 True면 PublicUser를 반환하고 False면 PrivateUser를 반환한다.
    hash 속성은 PrivateUser만 가지고 있다. 비밀번호 인증을 위해 hash 속성이 필요하다.
    """
    if user := data.get_one(username, is_public=is_public):
        return user
    return None
