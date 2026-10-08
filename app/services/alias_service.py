"""Validated, exact alias metadata for Concept and Topic learning views.

This is a deterministic lookup layer, not a search or ranking implementation.
"""

from collections import defaultdict
import unicodedata

from app.services.data_loader import DataLoader


ALIAS_TYPES = ("ko_alt", "en_full", "acronym", "synonym")
LANGUAGES = ("ko", "en")
TARGET_TYPES = ("concept", "topic")


def normalize_alias(value):
    """NFC, Unicode whitespace collapse, and casefold; retain punctuation."""
    if not isinstance(value, str):
        return ""
    return " ".join(unicodedata.normalize("NFC", value).split()).casefold()


class AliasService:
    def __init__(self, loader=None, aliases=None):
        self.loader = loader or DataLoader()
        self.aliases = aliases if aliases is not None else self.loader.load_aliases()
        self.targets = {
            ("concept", item["id"]): item["name"]
            for item in self.loader.load_concepts()
        }
        self.targets.update({
            ("topic", item["topic_id"]): item["name"]
            for item in self.loader.load_topics()
        })
        self.audit = self.audit_inventory(self.aliases, self.targets)
        invalid = (
            self.audit["invalid_records"]
            or self.audit["duplicate_ids"]
            or self.audit["exact_duplicates"]
            or self.audit["normalized_duplicates"]
            or self.audit["invalid_mapping_collisions"]
        )
        if invalid:
            raise ValueError("Invalid alias inventory: " + repr(invalid))

        self._by_term = defaultdict(set)
        self._by_target = defaultdict(lambda: {kind: [] for kind in ALIAS_TYPES})
        for target, name in self.targets.items():
            self._by_term[normalize_alias(name)].add(target)
        for item in self.aliases:
            target = (item["target_type"], item["target_id"])
            self._by_term[normalize_alias(item["alias"])].add(target)
            self._by_target[target][item["alias_type"]].append(item["alias"])

    @staticmethod
    def audit_inventory(aliases, targets):
        """Return all duplicate, target, and cross-target collision findings."""
        result = {
            "invalid_records": [], "duplicate_ids": [],
            "exact_duplicates": [], "normalized_duplicates": [],
            "cross_target_collisions": [], "invalid_mapping_collisions": [],
            "canonical_name_collisions": [],
        }
        ids = set()
        exact = {}
        normalized = {}
        term_targets = defaultdict(set)
        canonical = defaultdict(set)
        for target, name in targets.items():
            canonical[normalize_alias(name)].add(target)
        for item in aliases:
            alias_id = item.get("alias_id")
            target = (item.get("target_type"), item.get("target_id"))
            value = item.get("alias")
            if not isinstance(alias_id, str) or not alias_id.strip() or alias_id in ids:
                result["duplicate_ids"].append(alias_id)
            ids.add(alias_id)
            if (
                item.get("target_type") not in TARGET_TYPES
                or target not in targets
                or item.get("alias_type") not in ALIAS_TYPES
                or item.get("language") not in LANGUAGES
                or not isinstance(value, str)
                or not normalize_alias(value)
            ):
                result["invalid_records"].append(alias_id)
                continue
            key = (target, value)
            norm = normalize_alias(value)
            norm_key = (target, norm)
            if key in exact:
                result["exact_duplicates"].append((exact[key], alias_id))
            exact[key] = alias_id
            if norm_key in normalized:
                result["normalized_duplicates"].append((normalized[norm_key], alias_id))
            normalized[norm_key] = alias_id
            term_targets[norm].add(target)
            if target in canonical[norm]:
                result["normalized_duplicates"].append(("canonical name", alias_id))
            for other in canonical[norm] - {target}:
                result["canonical_name_collisions"].append((alias_id, target, other))
                result["invalid_mapping_collisions"].append((norm, target, other))
        for norm, matched in sorted(term_targets.items()):
            if len(matched) > 1:
                classification = (
                    "INVALID_MAPPING" if any(row[0] == norm for row in result["invalid_mapping_collisions"])
                    else "SAFE_DISAMBIGUATION_REQUIRED"
                )
                result["cross_target_collisions"].append({
                    "alias": norm, "targets": sorted(matched), "classification": classification,
                })
        return result

    def resolve(self, term):
        """Return zero, one, or all matching canonical targets in stable order."""
        targets = sorted(self._by_term.get(normalize_alias(term), ()))
        return [
            {"target_type": kind, "target_id": target_id, "name": self.targets[(kind, target_id)]}
            for kind, target_id in targets
        ]

    def group_for_target(self, target_type, target_id):
        """Return display-ready aliases, grouped by the controlled type vocabulary."""
        return self._by_target.get(
            (target_type, target_id), {kind: [] for kind in ALIAS_TYPES}
        )
