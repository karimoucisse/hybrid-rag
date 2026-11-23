from app.ingestion import ingest_file
from app.vector_store import get_vector_store
from app.rag import answer_question, stream_answer
from app.schemas import UserQuestion
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def test():
#     return ("hello world !")

def main():
    try:
        response = stream_answer(UserQuestion(query="qui a causé la premiere guerre mondiale ?"))
        for token in response:
            print(token, end="", flush=True)
        # print(f"Answer: {response}")
    except ValueError as e:
        print(f"Error: {e}")

main()
