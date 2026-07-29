from fastapi import FastAPI

app = FastAPI(
    title = "ParkFlow API",
    version = "0.0.1",
)

@app.get("/")
def root():
    return {
        "message" : "Welcome to ParkFlow API"
    }