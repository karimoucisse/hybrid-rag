import os
import tempfile
from pathlib import Path
from collections.abc import Callable
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from langchain_community.document_loaders import PyPDFLoader, TextLoader

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
