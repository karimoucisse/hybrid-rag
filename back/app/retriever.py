from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from app.ingestion import ingest_file

def bm25_retrieve_relevant_chunks(query: str) -> list[Document]:
	docs = ingest_file("data/wars1.pdf")
	retriever = BM25Retriever.from_documents(docs, k=4)
	res = retriever.invoke(query)
	print(res[0])

bm25_retrieve_relevant_chunks("Quand est ce que la première guerre mondiale a commencé ?")
