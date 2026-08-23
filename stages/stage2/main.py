from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


# Serve the web page from the "static" folder.
# This line must always be LAST, after every endpoint above it.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
