from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
from app.rag import stream_answer
from app.schemas import UserQuestion
from app.ingestion import ingest_file

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


# def main():
# 	try:
# 		chunks = ingest_file("data/wars1.pdf")
# 		print(f"Number of chunks ingested: {len(chunks)}")
# 		# response = stream_answer(UserQuestion(query="qui a tué nelson mandela ?"))
# 		# for token in response:
# 		# 	print(token, end="", flush=True)
# 		# print(f"Answer: {response}")
# 	except ValueError as e:
# 		print(f"Error: {e}")


# main()
