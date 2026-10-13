from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def main():
    return {"message": "Hello World"}

@app.get("/rdoc")
def rdoc():
    return {"rdoc": "RDOC"}
