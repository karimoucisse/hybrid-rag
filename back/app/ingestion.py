from collections.abc import Callable
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings

LOADERS: dict[str, Callable[[Path], BaseLoader]] = {
	".pdf": lambda p: PyPDFLoader(str(p)),
	".txt": lambda p: TextLoader(str(p), encoding="utf-8"),
}


def file_loader(file_path: Path) -> list[Document]:
	path = Path(file_path)
	suffix = path.suffix.lower()
	print(f"Loading file: {path}, suffix: {suffix}")
	f_loader = LOADERS.get(suffix)

	if f_loader is None:
		raise ValueError("Unsupported file type")
	try:
		docs = f_loader(path).load()
		if not docs:
			raise ValueError("No documents loaded")
	except Exception as e:
		raise ValueError(f"Error loading file: {e}")
	return docs


def chunk_docs(docs: list[Document]):
	if not docs:
		raise ValueError("No documents provided for chuncking.")
	settings = get_settings()
	text_spltter = RecursiveCharacterTextSplitter(
		chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
	)
	chunks = text_spltter.split_documents(docs)
	if not chunks:
		raise ValueError("No chunk created from the  provided documents.")
	return chunks


def ingest_file(file_path: Path):
	docs = file_loader(file_path)
	return chunk_docs(docs)
