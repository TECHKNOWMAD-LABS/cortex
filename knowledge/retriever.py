"""Knowledge retriever — FTS5 search interface for the knowledge store.

Provides semantic search retrieval with ranked results.
Phase 15: GraphRAG integration via retrieve_with_graph() for
combined FTS5 + knowledge graph traversal.

Usage:
    python -m knowledge.retriever --query "AKI prediction bias"
    python -m knowledge.retriever --query "nephrology triage" --source research --top-k 5
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from knowledge.store import KnowledgeStore, SearchResult


class KnowledgeRetriever:
    """Search interface for the knowledge store.

    Uses TF-IDF search with optional GraphRAG enrichment via
    retrieve_with_graph() for combined FTS5 + graph traversal.
    """

    def __init__(self, store: KnowledgeStore) -> None:
        self._store = store

    def search(
        self,
        query: str,
        top_k: int = 10,
        source: str | None = None,
        min_score: float = 0.0,
    ) -> list[SearchResult]:
        """Search the knowledge store with optional filtering."""
        results = self._store.search(query, top_k=top_k, source=source)
        if min_score > 0:
            results = [r for r in results if r.score >= min_score]
        return results

    def retrieve_for_debate(self, topic: str, max_tokens: int = 2000) -> str:
        """Retrieve context formatted for debate engine injection."""
        return self._store.retrieve_context(topic, max_tokens=max_tokens)

    def retrieve_for_research(self, topic: str, max_items: int = 10) -> list[dict[str, Any]]:
        """Retrieve evidence items for the research pipeline."""
        results = self.search(topic, top_k=max_items, source="evidence")
        return [
            {
                "source": r.entry.title,
                "finding": r.entry.content,
                "relevance_score": r.score,
                "tags": r.entry.tags,
            }
            for r in results
        ]

    def retrieve_with_graph(
        self,
        query: str,
        graph_store: Any,
        max_hops: int = 2,
        top_k: int = 10,
        source: str | None = None,
    ) -> list[dict[str, Any]]:
        """Combine FTS5 search with knowledge graph traversal.

        Performs a standard text search, then enriches each result by
        traversing the graph store for related entities up to *max_hops*
        away. Returns a merged list of search results augmented with
        graph context.

        Args:
            query: The search query string.
            graph_store: A ``knowledge.graph_store.GraphStore`` instance.
            max_hops: Maximum graph traversal depth (default 2).
            top_k: Maximum number of search results to enrich.
            source: Optional source filter for the FTS5 search.

        Returns:
            List of dicts, each containing the search result fields plus
            a ``graph_context`` key with neighbor information.
        """
        # Step 1: FTS5 text search
        results = self.search(query, top_k=top_k, source=source)

        enriched: list[dict[str, Any]] = []
        seen_entities: set[str] = set()

        for r in results:
            entry_dict = r.to_dict()

            # Step 2: Extract entity candidates from the result title/content
            entities = self._extract_entity_candidates(r.entry.title, r.entry.content)

            # Step 3: Traverse graph for each entity
            graph_context: dict[str, Any] = {}
            for entity in entities:
                if entity.lower() in seen_entities:
                    continue
                seen_entities.add(entity.lower())
                neighbors = graph_store.get_neighbors(entity, depth=max_hops)
                if neighbors:
                    graph_context[entity] = neighbors

            # Step 4: Also query graph directly for the search query terms
            query_triples = graph_store.query(subject=query)
            query_triples += graph_store.query(object=query)
            if query_triples:
                graph_context["_query_triples"] = [
                    {
                        "subject": t.subject,
                        "predicate": t.predicate,
                        "object": t.object,
                    }
                    for t in query_triples
                ]

            entry_dict["graph_context"] = graph_context
            enriched.append(entry_dict)

        return enriched

    @staticmethod
    def _extract_entity_candidates(title: str, content: str) -> list[str]:
        """Extract candidate entity names from title and content.

        Uses a simple heuristic: capitalized multi-word phrases and
        standalone capitalized words longer than 2 characters.
        """
        import re

        text = f"{title} {content}"
        # Find capitalized phrases (e.g., "Acute Kidney Injury")
        phrases = re.findall(r"(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", text)
        # Find standalone capitalized words / acronyms
        acronyms = re.findall(r"\b[A-Z]{2,6}\b", text)
        # Deduplicate while preserving order
        seen: set[str] = set()
        entities: list[str] = []
        for e in phrases + acronyms:
            e_stripped = e.strip()
            if e_stripped.lower() not in seen and len(e_stripped) > 2:
                seen.add(e_stripped.lower())
                entities.append(e_stripped)
        return entities[:10]  # cap to avoid excessive traversal

    def stats(self) -> dict[str, Any]:
        return self._store.stats()


def main() -> int:
    parser = argparse.ArgumentParser(description="Knowledge store search")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--top-k", type=int, default=10, help="Max results")
    parser.add_argument("--source", default=None, help="Filter by source")
    parser.add_argument("--min-score", type=float, default=0.0, help="Minimum score threshold")
    parser.add_argument("--db", default="knowledge/knowledge.db", help="Knowledge store DB path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    store = KnowledgeStore(db_path=args.db)
    retriever = KnowledgeRetriever(store)

    results = retriever.search(args.query, top_k=args.top_k, source=args.source, min_score=args.min_score)

    if args.json:
        output = [r.to_dict() for r in results]
        print(json.dumps(output, indent=2))
    else:
        print(f"Query: {args.query}")
        print(f"Results: {len(results)}")
        print()
        for r in results:
            print(f"  [{r.score:.4f}] {r.entry.title}")
            print(f"           Source: {r.entry.source} | Tags: {', '.join(r.entry.tags)}")
            print(f"           {r.entry.content[:150]}...")
            print()

    store.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
