from fastapi import FastAPI

app = FastAPI(title="Parking Among")


@app.get("/health")
def health():
    return {"status": "ok"}