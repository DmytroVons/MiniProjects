import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey

import auth
from ai_assistant import NiftyBridgeAIAssistant

app = FastAPI()


@app.post("/api/send")
def send_message(message: dict, api_key: APIKey = Depends(auth.get_api_key)):
    # Extract data from the request message
    query = message.get("message")

    assistant = NiftyBridgeAIAssistant()
    response = assistant.run(query=query)
    return {
        "message": response
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
dasd