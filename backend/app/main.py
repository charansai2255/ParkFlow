from fastapi import FastAPI

app = FastAPI(
    title="ParkFlow API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to ParkFlow API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }