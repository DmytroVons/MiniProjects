# NiftyBridge AI Assistant

## Overview

The NiftyBridge AI Assistant is an application that utilizes an LLM (Large Language Model) powered by LangChain and
FastAPI to provide a chatbot interface. The assistant can answer questions and provide information based on the analysis
of PDF files.

## Requirements

To run the application, ensure you have the following components installed:

- Python 3.10 or higher
- `pip` (Python package manager)

## Dependencies

Before running the application, install the necessary dependencies by executing the following command:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a .env file in the root directory and specify the required environment variables:

- OPENAI_API_KEY=YOUR_OPENAI_API_KEY
- API_KEY=YOUR_API_KEY

Replace YOUR_OPENAI_API_KEY with your OpenAI API key and YOUR_API_KEY with the API key you'll use for authentication.

## Running the Application

Follow these steps to run the application:

1. Install the required dependencies as mentioned above.

2. Start the FastAPI application using the following command:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

The application will be accessible at http://127.0.0.1:8000

## Interacting with the API

To interact with the application's API, you can use the following curl command to send a message:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/send' \
  -H 'accept: application/json' \
  -H 'access_token: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Hello"}'
```

Replace YOUR_API_KEY with the actual API key you provided in the environment variables.

## How to use the Swagger UI interface to send a message to your FastAPI application:

1. Open your web browser and navigate to the Swagger UI documentation for your FastAPI application. The URL is
   usually http://127.0.0.1:8000/docs
2. Click the "Authorize" button and pass YOUR_API_KEY from .env file.

3. In the Swagger UI interface, locate the send_message endpoint and expand it by clicking on it.

4. Click the "Try it out" button to open the input fields for the endpoint.

5. In the "Request body" section, you'll see a text area where you can input the JSON data for the message. Enter your
   message data in the required JSON format. For example:

```json
{
  "message": "Hello"
}
```

5. The response will be displayed below, showing the message sent by your FastAPI application.
