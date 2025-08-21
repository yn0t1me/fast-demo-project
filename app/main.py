from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/health")
def read_health():
    return {"status": "ok"}
