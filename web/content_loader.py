"""Helpers for loading lesson content modules for the Flask UI."""

from __future__ import annotations

import importlib
from dataclasses import dataclass

import config


@dataclass
class TopicContent:
    title: str
    intro: str
    concept_cards: list[dict]
    worked_examples: list[dict]
    common_mistakes: list[dict]
    key_vocabulary: dict
    available: bool = True


def load_topic_content(subject: str, topic: str) -> TopicContent:
    """Import and normalize content.<subject>.<topic> for templates."""
    try:
        module = importlib.import_module(f"content.{subject}.{topic}")
    except ImportError:
        return TopicContent(
            title=config.TOPIC_LABELS.get(topic, topic),
            intro="Lesson content for this topic is not available yet.",
            concept_cards=[],
            worked_examples=[],
            common_mistakes=[],
            key_vocabulary={},
            available=False,
        )

    return TopicContent(
        title=getattr(module, "TOPIC_TITLE", config.TOPIC_LABELS.get(topic, topic)),
        intro=getattr(module, "TOPIC_INTRO", ""),
        concept_cards=list(getattr(module, "CONCEPT_CARDS", [])),
        worked_examples=list(getattr(module, "WORKED_EXAMPLES", [])),
        common_mistakes=list(getattr(module, "COMMON_MISTAKES", [])),
        key_vocabulary=dict(getattr(module, "KEY_VOCABULARY", {})),
        available=True,
    )

