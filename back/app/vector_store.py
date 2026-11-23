from app.config import get_settings

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def get_vector_store() -> Chroma:
	settings = get_settings()
	embeddings = OllamaEmbeddings(model=settings.embedding_model)
	vector_store = Chroma(
		collection_name=settings.vector_store_name,
		embedding_function=embeddings,
		persist_directory=settings.vector_store_path,
	)
	return vector_store
