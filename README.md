# chatbot_fastapi_langgraph
Chatbot using fastapi and langgraph

## Setup

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Set up environment variables
```bash
cp example.env .env
```
paste your api keys in the .env file

2. Run the application
```bash
uvicorn main:app --reload
```
3. Access the application
```bash
http://localhost:8000
```
4. Chat with the chatbot
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "messages": ["Hello, how are you?"],
           "thread_id": "example_thread"
         }'
```
## Project structure

```bash
.
├── .env
├── main.py
├── requirements.txt
├── template.py
├── graph.py
├── Context_manager.py
├── llm.py
```