"""
Task graph builder.
Creates relationships between tasks, projects, and decisions.
"""
from typing import List, Dict


def build_task_graph(tasks: List[Dict]) -> Dict:
    """
    Build a graph of task relationships.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        Graph structure with nodes and edges
    """
    # Minimal v1 graph:
    # - Each task becomes a node
    # - Create edges between tasks that share at least one keyword (very simple)
    nodes = []
    edges = []

    def keywords(title: str) -> set[str]:
        return {w.lower() for w in title.split() if len(w) >= 4}

    task_keywords: Dict[str, set[str]] = {}
    for t in tasks:
        tid = str(t.get("id"))
        title = str(t.get("title", ""))
        nodes.append({"id": tid, "label": title, "status": t.get("status")})
        task_keywords[tid] = keywords(title)

    ids = list(task_keywords.keys())
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if task_keywords[a] and task_keywords[b] and (task_keywords[a] & task_keywords[b]):
                edges.append({"from": a, "to": b, "type": "related"})

    return {"nodes": nodes, "edges": edges}

