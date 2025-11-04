import uvicorn
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Home Page"}

@app.get("/get_user")
async def get_user():
    return {"message": "Hello World"}

@app.get("/get_user/{user_id}")
async def read_item(user_id: int):
    if user_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID cannot be negative"
        )
    if user_id == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID cannot be zero"
        )
    return {"user_id": user_id}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)