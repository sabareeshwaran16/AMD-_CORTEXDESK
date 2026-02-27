from .base_agent import BaseAgent
from typing import Dict, Any, List

class ResearchAgent(BaseAgent):
    def __init__(self, event_bus, working_memory, vector_db, embedding_model):
        super().__init__(
            agent_id="research_agent",
            capabilities=["semantic_search", "generate_citations", "answer_query"],
            event_bus=event_bus,
            working_memory=working_memory
        )
        self.vector_db = vector_db
        self.embedding_model = embedding_model
    
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        query = task.get("query", "")
        
        if task.get("capability") == "semantic_search":
            results = self._semantic_search(query)
        elif task.get("capability") == "answer_query":
            results = self._answer_query(query)
        else:
            results = []
        
        result = {
            "query": query,
            "results": results,
            "confidence": 0.8
        }
        
        self.publish_event("research_completed", result)
        return result
    
    def _semantic_search(self, query: str) -> List[Dict[str, Any]]:
        query_vector = self.embedding_model.encode(query)
        results = self.vector_db.search(query_vector, top_k=5)
        return results
    
    def _answer_query(self, query: str) -> str:
        search_results = self._semantic_search(query)
        
        if not search_results:
            return "No relevant information found."
        
        context = "\n".join([
            r["metadata"].get("text", "")[:200]
            for r in search_results[:3]
        ])
        
        return f"Based on available documents:\n{context}"
    
    def index_document(self, text: str, metadata: Dict[str, Any]):
        vector = self.embedding_model.encode(text)
        metadata["text"] = text
        self.vector_db.add(vector, metadata)
        self.vector_db.save()
