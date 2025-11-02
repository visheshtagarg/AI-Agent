try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except ImportError:  # soft dependency
    SentenceTransformer = None  # type: ignore

try:
    import chromadb  # type: ignore
    from chromadb.config import Settings  # type: ignore
except ImportError:
    chromadb = None  # type: ignore
    Settings = None  # type: ignore
import os


class RAGRetrieverAgent:
    def __init__(self, persist_dir='chromadb_store'):
        self.dependency_missing = not (SentenceTransformer is not None and chromadb is not None and Settings is not None)
        self.available = False
        self.collection = None
        self.client = None
        self.embed_model = None
        self.collection_name = 'nutrition_facts'

        if self.dependency_missing:
            # Defer hard failure; allow the app to run without RAG.
            return

        try:
            os.makedirs(persist_dir, exist_ok=True)
            # Prefer PersistentClient when available
            if hasattr(chromadb, 'PersistentClient'):
                self.client = chromadb.PersistentClient(path=persist_dir)  # type: ignore
            else:
                self.client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir))

            if hasattr(self.client, 'get_or_create_collection'):
                self.collection = self.client.get_or_create_collection(self.collection_name)  # type: ignore
            else:
                try:
                    self.collection = self.client.get_collection(self.collection_name)
                except Exception:
                    self.collection = self.client.create_collection(self.collection_name)

            self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.available = True
        except Exception:
            # If initialization fails, keep unavailable but don't crash UI
            self.available = False
            self.client = None
            self.collection = None
            self.embed_model = None

    def add_documents(self, docs: list):
        if not self.available or self.collection is None or self.embed_model is None:
            # No-op when unavailable
            return
        ids = [d['id'] for d in docs]
        texts = [d['text'] for d in docs]
        embeddings = self.embed_model.encode(texts, convert_to_numpy=True).tolist()
        self.collection.add(documents=texts, metadatas=[d.get('metadata', {}) for d in docs], ids=ids, embeddings=embeddings)
        # Persist if supported
        if hasattr(self.client, 'persist'):
            try:
                self.client.persist()  # type: ignore
            except Exception:
                pass

    def query(self, text: str, n_results=3):
        if not self.available or self.collection is None:
            # Return empty-like result when unavailable
            return {"ids": [], "documents": [], "metadatas": []}
        res = self.collection.query(query_texts=[text], n_results=n_results)
        return res

