from fastapi import FastAPI

app = FastAPI(
    title="Market AI",
    version="1.0.0",
 )


@app.get("/")
def root():
          return {
                  "status": "Online",
                  "message": "Market AI Backend"
                  }

