import time
from typing import List, Dict

class RAGEvaluator:
    def __init__(self):
        self.responses: List[Dict] = []

    def evaluate_response(self, query: str, response: str, context: List[Dict]) -> Dict:
        """Evaluates response relevance, length, and citations."""
        start_time = time.time()
        metrics = {
            "response_length": len(response),
            "source_citations": sum(1 for doc in context if doc["content"] in response),
            "evaluation_time": time.time() - start_time,
            "context_relevance": self._calculate_relevance(query, context)
        }
        self.responses.append({"query": query, "response": response, "metrics": metrics})
        return metrics

    def _calculate_relevance(self, query: str, context: List[Dict]) -> float:
        """Simple relevance score based on query match in documents."""
        return sum(1 for c in context if query.lower() in c["content"].lower()) / len(context)
