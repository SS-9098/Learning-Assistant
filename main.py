from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, welcome to the Voice Assistant!"}

@app.post("/query/")
async def process_query(user_input: str):
    # Process the input and call your APIs here
    response = f"Processing your input: {user_input}"
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
