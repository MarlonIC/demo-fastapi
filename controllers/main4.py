from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Security - First Steps
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

