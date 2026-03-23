from fastapi import FastAPI

app = FastAPI()

@app.post("/logout")
async def logout():
    return {"message": "Logout successful!"}