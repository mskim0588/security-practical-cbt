"""Deterministic in-process search of existing learning records."""

from app.services.alias_service import ALIAS_TYPES, AliasService, normalize_alias
from app.services.data_loader import DataLoader


MAX_QUERY_LENGTH = 120
ENTITY_TYPES = ("all", "concept", "topic", "question")
TYPE_ORDER = {"concept": 0, "topic": 1, "question": 2}

# Lower is stronger. Entity type is used only after match strength.
MATCH_PRIORITY = {
    "canonical_exact": 0,
    "alias_exact": 1,
    "canonical_prefix": 2,
    "alias_prefix": 3,
    "canonical_partial": 4,
    "alias_partial": 5,
    "command": 6,
    "keyword": 6,
    "summary": 7,
    "content": 8,
}


def _strings(value):
    """Flatten selected, existing text fields without indexing JSON field names."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in _strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in _strings(item)]
    return []


def _preview(value, limit=150):
    text = " ".join((value or "").split())
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def _contains(text, query):
    """Literal normalized match; short ASCII terms require word boundaries."""
    if not text or not query:
        return False
    if query.isascii() and query.isalnum() and len(query) <= 3:
        start = 0
        while (at := text.find(query, start)) >= 0:
            end = at + len(query)
            before = text[at - 1] if at else ""
            after = text[end] if end < len(text) else ""
            if (not before or not (before.isalnum() or before == "_")) and (
                not after or not (after.isalnum() or after == "_")
            ):
                return True
            start = at + 1
        return False
    return query in text


class SearchService:
    def __init__(self, loader=None, alias_service=None):
        self.loader = loader or DataLoader()
        self.alias_service = alias_service or AliasService(self.loader)
        self.records = self._build_records()

    def _record(self, kind, target_id, title, preview, category, parent_name="",
                topic_id="", question_type="", summary="", content=(),
                keywords=(), commands=()):
        aliases = self.alias_service.group_for_target(kind, target_id) if kind != "question" else {
            alias_type: [] for alias_type in ALIAS_TYPES
        }
        return {
            "type": kind,
            "id": target_id,
            "title": title,
            "preview": _preview(preview),
            "category": category,
            "parent_name": parent_name,
            "topic_id": topic_id,
            "question_type": question_type,
            "normalized_title": normalize_alias(title),
            "normalized_aliases": [
                (normalize_alias(alias), alias_type)
                for alias_type in ALIAS_TYPES for alias in aliases[alias_type]
            ],
            "normalized_summary": normalize_alias(summary),
            "normalized_content": normalize_alias(" ".join(_strings(content))),
            "normalized_keywords": normalize_alias(" ".join(_strings(keywords))),
            "normalized_commands": normalize_alias(" ".join(_strings(commands))),
        }

    def _build_records(self):
        concepts = self.loader.load_concepts()
        topics = self.loader.load_topics()
        questions = self.loader.load_questions()
        contents = self.loader.load_concept_contents()
        explanations = self.loader.load_explanations()
        concept_by_id = {item["id"]: item for item in concepts}
        topic_by_question = {
            item["question_id"]: item["topic_id"]
            for item in self.loader.load_question_topics()
        }

        records = []
        for concept in concepts:
            cid = concept["id"]
            content = contents.get(cid, {})
            summary = content.get("summary") or concept.get("summary", "")
            records.append(self._record(
                "concept", cid, concept["name"], summary, concept["category"],
                summary=summary,
                content=[concept.get("description", ""), content.get("core_points", []),
                         content.get("mechanism", ""), content.get("exam_points", [])],
                commands=content.get("commands_or_examples", []),
            ))

        for topic in topics:
            parent = concept_by_id[topic["parent_concept_id"]]
            records.append(self._record(
                "topic", topic["topic_id"], topic["name"], topic["summary"],
                topic["category"], parent_name=parent["name"],
                summary=topic["summary"],
            ))

        type_labels = {"short": "단답형", "descriptive": "서술형", "practical": "실무형"}
        for question in questions:
            qid = question["id"]
            explanation = explanations.get(qid, {})
            rubric = explanation.get("practical_scoring_criteria") or {}
            required_keywords = [
                part.get("required_keywords", [])
                for part in rubric.get("rubrics", [])
                if isinstance(part, dict)
            ] if isinstance(rubric, dict) else []
            parent = concept_by_id[question["concept_id"]]
            records.append(self._record(
                "question", qid, qid, question["question"], question["category"],
                parent_name=parent["name"], topic_id=topic_by_question.get(qid, ""),
                question_type=type_labels.get(question["type"], question["type"]),
                content=[question["question"], question.get("model_answer", ""),
                         question.get("explanation", ""), explanation.get("overview", ""),
                         explanation.get("key_concept_points", []),
                         explanation.get("why_correct", "")],
                keywords=[question.get("tags", []), required_keywords],
                commands=explanation.get("related_commands", []),
            ))
        return records

    @staticmethod
    def _best_match(record, query, exact_alias_targets):
        matches = []
        name = record["normalized_title"]
        target = (record["type"], record["id"])
        if name == query:
            matches.append(("canonical_exact", "이름 일치"))
        elif name.startswith(query):
            matches.append(("canonical_prefix", "이름 앞부분 일치"))
        elif _contains(name, query):
            matches.append(("canonical_partial", "이름 일부 일치"))

        for alias, alias_type in record["normalized_aliases"]:
            reason = "약어 일치" if alias_type == "acronym" else "별칭 일치"
            if alias == query and target in exact_alias_targets:
                matches.append(("alias_exact", reason))
            elif alias.startswith(query):
                matches.append(("alias_prefix", reason))
            elif _contains(alias, query):
                matches.append(("alias_partial", reason))

        if _contains(record["normalized_commands"], query):
            matches.append(("command", "명령어·기술 용어 일치"))
        if _contains(record["normalized_keywords"], query):
            matches.append(("keyword", "키워드 일치"))
        if _contains(record["normalized_summary"], query):
            label = "Topic 설명 일치" if record["type"] == "topic" else "개념 요약 일치"
            matches.append(("summary", label))
        if _contains(record["normalized_content"], query):
            label = "문제 내용 일치" if record["type"] == "question" else "학습 내용 일치"
            matches.append(("content", label))
        return min(matches, key=lambda item: MATCH_PRIORITY[item[0]]) if matches else None

    def search(self, query, entity_type="all"):
        """Return ranked canonical entities and counts after optional type filtering."""
        query = query if isinstance(query, str) else ""
        selected_type = entity_type if entity_type in ENTITY_TYPES else "all"
        if len(query) > MAX_QUERY_LENGTH:
            return {
                "query": query[:MAX_QUERY_LENGTH], "selected_type": selected_type,
                "error": f"검색어는 {MAX_QUERY_LENGTH}자 이하로 입력해 주세요.",
                "has_query": False, "results": [], "total": 0,
                "type_counts": {kind: 0 for kind in ENTITY_TYPES},
            }
        normalized = normalize_alias(query)
        if not normalized:
            return {
                "query": query, "selected_type": selected_type, "error": None,
                "has_query": False, "results": [], "total": 0,
                "type_counts": {kind: 0 for kind in ENTITY_TYPES},
            }

        # AliasService resolves all targets, including future ambiguous aliases.
        exact_alias_targets = {
            (item["target_type"], item["target_id"])
            for item in self.alias_service.resolve(query)
        }
        ranked = []
        for record in self.records:
            match = self._best_match(record, normalized, exact_alias_targets)
            if match is None:
                continue
            kind, reason = match
            result = {key: record[key] for key in (
                "type", "id", "title", "preview", "category", "parent_name",
                "topic_id", "question_type",
            )}
            result["reason"] = reason
            ranked.append((MATCH_PRIORITY[kind], TYPE_ORDER[record["type"]],
                           record["normalized_title"], record["id"], result))
        ranked.sort(key=lambda item: item[:4])
        all_results = [item[4] for item in ranked]
        counts = {kind: sum(result["type"] == kind for result in all_results)
                  for kind in ENTITY_TYPES if kind != "all"}
        counts["all"] = len(all_results)
        results = all_results if selected_type == "all" else [
            result for result in all_results if result["type"] == selected_type
        ]
        return {
            "query": query, "selected_type": selected_type, "error": None,
            "has_query": True, "results": results, "total": len(results),
            "type_counts": counts,
        }
