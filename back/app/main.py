from app.ingestion import ingest_file
from app.vector_store import get_vector_store
from app.rag import answer_question, stream_answer
from app.schemas import UserQuestion
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/chat/stream")
def chat_stream(query: UserQuestion):
    return StreamingResponse(
        stream_answer(query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

def main():
    try:
        response = stream_answer(UserQuestion(query="qui a tué nelson mandela ?"))
        for token in response:
            print(token, end="", flush=True)
        # print(f"Answer: {response}")
    except ValueError as e:
        print(f"Error: {e}")

main()
