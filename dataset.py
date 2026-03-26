"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "hopeful",
    "proud",
    "fire",
    "glad",
    "best",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "exhausted",
    "nervous",
    "worried",
    "annoyed",
    "miserable",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "Lowkey stressed but proud of myself",
    "That movie was fire 😂",
    "I love getting stuck in traffic",
    "Not bad at all :)",
    "This meeting was boring and exhausting",
    "I'm exhausted but proud I finished",
    "meh, just another day",
    "No cap, this project is awesome",
    "Wow great, another homework packet",
    "I am proud but still nervous",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "Lowkey stressed but proud of myself"
    "positive",  # "That movie was fire 😂"
    "negative",  # "I love getting stuck in traffic" (sarcasm)
    "positive",  # "Not bad at all :)"
    "negative",  # "This meeting was boring and exhausting"
    "mixed",     # "I'm exhausted but proud I finished"
    "neutral",   # "meh, just another day"
    "positive",  # "No cap, this project is awesome"
    "negative",  # "Wow great, another homework packet" (sarcasm)
    "mixed",     # "I am proud but still nervous"
]

# Quick safety check so the program fails early if the dataset is misaligned.
if len(SAMPLE_POSTS) != len(TRUE_LABELS):
    raise ValueError(
        "SAMPLE_POSTS and TRUE_LABELS must have the same length. "
        "Add one label for every post."
    )
