import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path: str = "app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient("vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(
            name="candidate_portfolio"
        )

    def load_portfolio(self):
        """Load portfolio CSV into ChromaDB if not already loaded."""
        if self.collection.count() == 0:
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())],
                )

    def query_links(self, skills: list, n_results: int = 2) -> list:
        """Return portfolio links semantically relevant to given skills."""
        if not skills:
            return []
        return self.collection.query(
            query_texts=skills,
            n_results=min(n_results, self.collection.count()),
        ).get("metadatas", [])

    def reset_collection(self):
        """Clear the collection — useful for testing."""
        self.chroma_client.delete_collection("candidate_portfolio")
        self.collection = self.chroma_client.get_or_create_collection(
            name="candidate_portfolio"
        )