from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def _health_check():
    return "Running"
