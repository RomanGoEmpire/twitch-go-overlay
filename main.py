from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def health():
    return "API is running"
