from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List, Dict
import os

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = None

    def process_documents(self, documents: List[Dict]):
        all_splits = []
        all_metadatas = []

        for doc in documents:
            splits = self.text_splitter.split_text(doc['content'])
            metadatas = [{'uuid': doc['uuid']} for _ in splits]
            
            all_splits.extend(splits)
            all_metadatas.extend(metadatas)

        self.vector_store = Chroma.from_texts(
            texts=all_splits,
            metadatas=all_metadatas,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
        return self.vector_store

    async def query_similar_documents(self, query: str, k: int = 1):
        if not self.vector_store:
            self.vector_store = Chroma(
                persist_directory="./chroma_db",
                embedding_function=self.embeddings
            )
        
        results = self.vector_store.similarity_search_with_relevance_scores(
            query,
            k=k
        )
        return results 