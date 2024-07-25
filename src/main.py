from fastapi import FastAPI
from web import explorer, creature
import uvicorn
import icecream as ic

app = FastAPI()


@app.get("/")
def top():
    return "Hello World!"


@app.get("/echo/{thing}")
def echo(thing):
    return f"echoing {thing}"


app.include_router(explorer.router)
app.include_router(creature.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
