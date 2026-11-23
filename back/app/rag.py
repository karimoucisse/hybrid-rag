import json
from app.schemas import UserQuestion, ChatResponse
from app.vector_store import get_vector_store
from langchain_core.documents import Document
from app.config import get_settings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from functools import lru_cache
from typing import Iterator

PROMPT = ChatPromptTemplate.from_template(
		"""You are a helpful assistant. Use the following pieces of context to answer the question at the end.
		Respond in the same language as the question.
		the context is below, delimited by triple backticks.

		context: ```{context}```

		Question: {question}

		If you don't know the answer, just say that you don't know, don't try to make up an answer, just say "I don't know".

		Answer:

		"""
	)

def retrieve_relevant_chunks(query: UserQuestion) -> list[Document]:
	vector_store = get_vector_store()
	chunks = vector_store.similarity_search(query, k=3)
	return chunks

def format_docs(chunks: list[Document]) -> str:
	normalized_chunks = "\n\n".join([chunk.page_content for chunk in chunks])
	return normalized_chunks

@lru_cache
def get_chat_model() -> ChatOllama:
	settings = get_settings()
	chat_model = ChatOllama(
		model=settings.chat_model,
		temperature=settings.temperature,
        reasoning=False
	)
	return chat_model

@lru_cache
def get_chain() -> Runnable:
	llm = get_chat_model()
	chain = PROMPT | llm | StrOutputParser()
	return chain

def sse(data: dict) -> str:
    """Formate un événement SSE."""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def stream_answer(query: UserQuestion) -> Iterator[str]:
    try:
        print(f"Answering question: {query.query}")
        context = format_docs(retrieve_relevant_chunks(query.query))
        chain = get_chain()

        for chunk in chain.stream({"context": context, "question": query.query}):
            yield sse({"token": chunk})
        yield sse({"done": True})
    except Exception as e:
        yield sse({"error": str(e)})

def answer_question(query: UserQuestion) -> ChatResponse:
	print(f"Answering question: {query.query}")
	context = format_docs(retrieve_relevant_chunks(query.query))
	response = get_chain().invoke({"context": context, "question": query.query})
	return ChatResponse(answer=response, sources=[])
