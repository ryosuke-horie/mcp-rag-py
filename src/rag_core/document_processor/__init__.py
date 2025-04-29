# rag_core/document_processor/__init__.py

"""
ドキュメントの読み込みと分割を行うモジュール。
"""

from .loader import load_documents
from .splitter import split_documents

__all__ = [
    "load_documents",
    "split_documents",
]
