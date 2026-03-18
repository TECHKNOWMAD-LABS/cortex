"""GraphRAG knowledge store — entity-relationship graph with JSON persistence.

Provides a triple-based knowledge graph for enriching retrieval with
relationship traversal. Integrates with the existing KnowledgeRetriever
via retrieve_with_graph().

Security:
- Graph stored as JSON (json.dump) — NEVER pickle.
- Triple extraction uses string operations and regex — never eval() or exec().
- Graph file created with standard permissions.

Usage:
    from knowledge.graph_store import GraphStore

    gs = GraphStore()
    gs.add_triple("AKI", "caused_by", "nephrotoxic drugs")
    gs.add_triple("AKI", "diagnosed_with", "serum creatinine")
    results = gs.query(subject="AKI")
    neighbors = gs.get_neighbors("AKI", depth=2)
    gs.save("knowledge/graph.json")
"""

from __future__ import annotations

import json
import re
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, NamedTuple

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


class Triple(NamedTuple):
    """A knowledge graph triple with optional metadata."""

    subject: str
    predicate: str
    object: str
    metadata: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Graph Store
# ---------------------------------------------------------------------------


class GraphStore:
    """Manages a knowledge graph stored as triples.

    Supports add, query, neighbor traversal, regex-based triple extraction,
    JSON persistence, and optional NetworkX export.
    """

    def __init__(self) -> None:
        self._triples: list[Triple] = []
        # Indexes for fast lookup
        self._by_subject: dict[str, list[int]] = defaultdict(list)
        self._by_predicate: dict[str, list[int]] = defaultdict(list)
        self._by_object: dict[str, list[int]] = defaultdict(list)

    # ---- Core operations ---------------------------------------------------

    def add_triple(
        self,
        subject: str,
        predicate: str,
        object: str,
        metadata: dict[str, Any] | None = None,
    ) -> Triple:
        """Add a triple to the graph.

        Args:
            subject: The subject entity.
            predicate: The relationship.
            object: The object entity.
            metadata: Optional metadata dict.

        Returns:
            The created Triple.
        """
        subject = subject.strip()
        predicate = predicate.strip()
        object = object.strip()

        if not subject or not predicate or not object:
            raise ValueError("Subject, predicate, and object must be non-empty strings.")

        triple = Triple(
            subject=subject,
            predicate=predicate,
            object=object,
            metadata=metadata or {},
        )
        idx = len(self._triples)
        self._triples.append(triple)
        self._by_subject[subject.lower()].append(idx)
        self._by_predicate[predicate.lower()].append(idx)
        self._by_object[object.lower()].append(idx)
        return triple

    def query(
        self,
        subject: str | None = None,
        predicate: str | None = None,
        object: str | None = None,
    ) -> list[Triple]:
        """Query triples by any combination of subject, predicate, object.

        All provided fields must match (AND logic). If no fields are
        provided, returns all triples.

        Args:
            subject: Filter by subject (case-insensitive).
            predicate: Filter by predicate (case-insensitive).
            object: Filter by object (case-insensitive).

        Returns:
            List of matching Triple objects.
        """
        candidate_sets: list[set[int]] = []

        if subject is not None:
            candidate_sets.append(set(self._by_subject.get(subject.lower(), [])))
        if predicate is not None:
            candidate_sets.append(set(self._by_predicate.get(predicate.lower(), [])))
        if object is not None:
            candidate_sets.append(set(self._by_object.get(object.lower(), [])))

        if not candidate_sets:
            return list(self._triples)

        result_indices = candidate_sets[0]
        for s in candidate_sets[1:]:
            result_indices = result_indices & s

        return [self._triples[i] for i in sorted(result_indices)]

    def get_neighbors(self, entity: str, depth: int = 1) -> dict[str, list[dict[str, str]]]:
        """Get connected entities via BFS traversal.

        Args:
            entity: The starting entity.
            depth: Maximum traversal depth (default 1).

        Returns:
            Dict mapping entity names to lists of connection info dicts.
            Each connection dict has keys: predicate, direction, connected_to.
        """
        depth = max(1, min(10, depth))
        entity_lower = entity.lower()

        visited: set[str] = set()
        neighbors: dict[str, list[dict[str, str]]] = defaultdict(list)
        queue: deque[tuple[str, int]] = deque([(entity_lower, 0)])
        visited.add(entity_lower)

        while queue:
            current, current_depth = queue.popleft()
            if current_depth >= depth:
                continue

            # Outgoing edges (current is subject)
            for idx in self._by_subject.get(current, []):
                triple = self._triples[idx]
                obj_lower = triple.object.lower()
                neighbors[triple.object].append(
                    {
                        "predicate": triple.predicate,
                        "direction": "outgoing",
                        "connected_to": triple.subject,
                    }
                )
                if obj_lower not in visited:
                    visited.add(obj_lower)
                    queue.append((obj_lower, current_depth + 1))

            # Incoming edges (current is object)
            for idx in self._by_object.get(current, []):
                triple = self._triples[idx]
                subj_lower = triple.subject.lower()
                neighbors[triple.subject].append(
                    {
                        "predicate": triple.predicate,
                        "direction": "incoming",
                        "connected_to": triple.object,
                    }
                )
                if subj_lower not in visited:
                    visited.add(subj_lower)
                    queue.append((subj_lower, current_depth + 1))

        # Remove the starting entity from results
        neighbors.pop(entity, None)
        # Also check case-insensitively
        to_remove = [k for k in neighbors if k.lower() == entity_lower]
        for k in to_remove:
            del neighbors[k]

        return dict(neighbors)

    # ---- Triple extraction -------------------------------------------------

    def extract_triples_from_text(self, text: str) -> list[Triple]:
        """Extract triples from text using regex-based NER-lite patterns.

        Uses common relationship patterns to identify subject-predicate-object
        triples. This is a lightweight heuristic, not a full NER pipeline.

        Args:
            text: Input text to extract triples from.

        Returns:
            List of extracted Triple objects (also added to the graph).
        """
        extracted: list[Triple] = []

        # Pattern: "X is/are Y"
        for match in re.finditer(
            r"([A-Z][A-Za-z0-9\s]{1,40}?)\s+(?:is|are)\s+(?:a|an|the)?\s*([A-Za-z0-9\s]{2,40}?)(?:\.|,|;|$)",
            text,
        ):
            subj = match.group(1).strip()
            obj = match.group(2).strip()
            if len(subj) > 2 and len(obj) > 2:
                triple = self.add_triple(subj, "is_a", obj, {"source": "extraction", "pattern": "is_a"})
                extracted.append(triple)

        # Pattern: "X causes/leads to/results in Y"
        for match in re.finditer(
            r"([A-Z][A-Za-z0-9\s]{1,40}?)\s+(?:causes?|leads?\s+to|results?\s+in)\s+([A-Za-z0-9\s]{2,40}?)(?:\.|,|;|$)",
            text,
        ):
            subj = match.group(1).strip()
            obj = match.group(2).strip()
            if len(subj) > 2 and len(obj) > 2:
                triple = self.add_triple(subj, "causes", obj, {"source": "extraction", "pattern": "causal"})
                extracted.append(triple)

        # Pattern: "X uses/utilizes/employs Y"
        for match in re.finditer(
            r"([A-Z][A-Za-z0-9\s]{1,40}?)\s+(?:uses?|utilizes?|employs?)\s+([A-Za-z0-9\s]{2,40}?)(?:\.|,|;|$)",
            text,
        ):
            subj = match.group(1).strip()
            obj = match.group(2).strip()
            if len(subj) > 2 and len(obj) > 2:
                triple = self.add_triple(subj, "uses", obj, {"source": "extraction", "pattern": "usage"})
                extracted.append(triple)

        # Pattern: "X contains/includes/comprises Y"
        for match in re.finditer(
            r"([A-Z][A-Za-z0-9\s]{1,40}?)\s+(?:contains?|includes?|comprises?)\s+([A-Za-z0-9\s]{2,40}?)(?:\.|,|;|$)",
            text,
        ):
            subj = match.group(1).strip()
            obj = match.group(2).strip()
            if len(subj) > 2 and len(obj) > 2:
                triple = self.add_triple(subj, "contains", obj, {"source": "extraction", "pattern": "containment"})
                extracted.append(triple)

        # Pattern: "X is related to/associated with Y"
        for match in re.finditer(
            r"([A-Z][A-Za-z0-9\s]{1,40}?)\s+(?:is\s+related\s+to|is\s+associated\s+with)\s+([A-Za-z0-9\s]{2,40}?)(?:\.|,|;|$)",
            text,
        ):
            subj = match.group(1).strip()
            obj = match.group(2).strip()
            if len(subj) > 2 and len(obj) > 2:
                triple = self.add_triple(subj, "related_to", obj, {"source": "extraction", "pattern": "association"})
                extracted.append(triple)

        return extracted

    # ---- Persistence -------------------------------------------------------

    def save(self, path: str | Path) -> None:
        """Save the graph to a JSON file.

        Args:
            path: File path for the JSON output.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": "1.0",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "triple_count": len(self._triples),
            "triples": [
                {
                    "subject": t.subject,
                    "predicate": t.predicate,
                    "object": t.object,
                    "metadata": t.metadata or {},
                }
                for t in self._triples
            ],
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: str | Path) -> GraphStore:
        """Load a graph from a JSON file.

        Args:
            path: File path to load from.

        Returns:
            A new GraphStore populated with the loaded triples.
        """
        path = Path(path)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        store = cls()
        for t in data.get("triples", []):
            store.add_triple(
                subject=t["subject"],
                predicate=t["predicate"],
                object=t["object"],
                metadata=t.get("metadata"),
            )
        return store

    # ---- Stats and export --------------------------------------------------

    def stats(self) -> dict[str, Any]:
        """Return statistics about the graph.

        Returns:
            Dict with counts of triples, unique entities, unique predicates.
        """
        entities: set[str] = set()
        predicates: set[str] = set()
        for t in self._triples:
            entities.add(t.subject)
            entities.add(t.object)
            predicates.add(t.predicate)

        return {
            "triple_count": len(self._triples),
            "entity_count": len(entities),
            "predicate_count": len(predicates),
            "entities": sorted(entities),
            "predicates": sorted(predicates),
        }

    def to_networkx(self):  # -> nx.DiGraph
        """Export the graph as a NetworkX DiGraph.

        Returns:
            A networkx.DiGraph with edges labeled by predicate.

        Raises:
            ImportError: If networkx is not installed.
        """
        try:
            import networkx as nx
        except ImportError:
            raise ImportError("networkx is required for graph export. Install it with: pip install networkx")

        G = nx.DiGraph()
        for t in self._triples:
            G.add_edge(
                t.subject,
                t.object,
                predicate=t.predicate,
                metadata=t.metadata or {},
            )
        return G
