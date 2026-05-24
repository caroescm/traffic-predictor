from fastapi import FastAPI

app = FastAPI(title="Traffic Predictor")

@app.get("/")
def root():
    return {"message": "Traffic Predictor API is running"}