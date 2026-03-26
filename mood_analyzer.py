# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Optional, Tuple

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

        # Simple extra signals beyond the base word lists.
        self.positive_weights = {
            "love": 2,
            "awesome": 2,
            "amazing": 2,
            "fire": 2,
            "proud": 2,
            "😂": 1,
            "🔥": 1,
            ":)": 1,
            "🙂": 1,
        }
        self.negative_weights = {
            "terrible": 2,
            "awful": 2,
            "hate": 2,
            "boring": 2,
            "exhausted": 2,
            ":(": 1,
            "🥲": 1,
            "😭": 1,
            "💀": 1,
        }
        self.negation_words = {"not", "never", "isnt", "isn't", "dont", "don't", "cant", "can't"}

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Improvements added:
          - Lowercases the text
          - Keeps a few common emojis / emoticons as tokens
          - Removes most punctuation
          - Normalizes long repeated letters like "soooo" -> "soo"
        """
        cleaned = text.strip().lower()
        cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)

        # Put spaces around simple emoji / emoticon signals we want to keep.
        signals = [":)", ":(", "🙂", "😂", "🥲", "😭", "💀", "🔥"]
        for signal in signals:
            cleaned = cleaned.replace(signal, f" {signal} ")

        tokens = re.findall(r"[a-z]+(?:'[a-z]+)?|:\)|:\(|[🙂😂🥲😭💀🔥]", cleaned)
        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _positive_weight(self, token: str) -> int:
        if token in self.positive_weights:
            return self.positive_weights[token]
        if token in self.positive_words:
            return 1
        return 0

    def _negative_weight(self, token: str) -> int:
        if token in self.negative_weights:
            return self.negative_weights[token]
        if token in self.negative_words:
            return 1
        return 0

    def _analyze(self, text: str) -> Tuple[List[str], List[str], List[str], int]:
        tokens = self.preprocess(text)
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Negation handling: flip the mood of the very next sentiment word.
            if token in self.negation_words and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                pos_weight = self._positive_weight(next_token)
                neg_weight = self._negative_weight(next_token)

                if pos_weight > 0:
                    score -= pos_weight
                    negative_hits.append(f"{token} {next_token}")
                    i += 2
                    continue
                if neg_weight > 0:
                    score += neg_weight
                    positive_hits.append(f"{token} {next_token}")
                    i += 2
                    continue

            pos_weight = self._positive_weight(token)
            neg_weight = self._negative_weight(token)

            if pos_weight > 0:
                score += pos_weight
                positive_hits.append(token)
            elif neg_weight > 0:
                score -= neg_weight
                negative_hits.append(token)

            i += 1

        return tokens, positive_hits, negative_hits, score

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        Modeling improvements implemented:
          - simple preprocessing
          - simple negation handling ("not happy", "not bad")
          - light word weighting ("love" stronger than "good")
          - emoji / emoticon handling
        """
        _, _, _, score = self._analyze(text)
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Label rules used here:
          - both positive and negative evidence -> "mixed"
          - only positive evidence -> "positive"
          - only negative evidence -> "negative"
          - no evidence -> "neutral"
        """
        _, positive_hits, negative_hits, score = self._analyze(text)

        if positive_hits and negative_hits:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.
        """
        tokens, positive_hits, negative_hits, score = self._analyze(text)
        return (
            f"tokens={tokens}; score={score}; "
            f"positive={positive_hits or '[]'}; negative={negative_hits or '[]'}"
        )
