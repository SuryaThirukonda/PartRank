import fastapi as fastAPI


app = fastAPI.FastAPI()


@app.get("/")
def read_root():
    return {"Status": "OK"}


@app.get("/health")
def health_check():
    return {"yo bhai" : "code kharro"}