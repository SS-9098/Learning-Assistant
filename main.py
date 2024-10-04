from fastapi import FastAPI
from Voice import recognize_speech_from_mic

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voice Assistant"}

@app.post("/speech-to-text/")
async def process_speech():
    # Recognize speech from the microphone
    recognized_text = recognize_speech_from_mic()
    return {"recognized_text": recognized_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
