import pandas as pd
import re
from collections import Counter
from sqlalchemy.orm import Session
from .models import Note


def analyze_notes(db: Session):
    notes = db.query(Note).all()
    notes_data = pd.DataFrame(
        [(note.id, note.content) for note in notes], columns=["id", "content"]
    )
    notes_data["word_count"] = notes_data["content"].apply(
        lambda x: len(re.findall(r"\w+", x))
    )

    total_word_count = (
        int(notes_data["word_count"].sum())
        if not notes_data["word_count"].isnull().all()
        else 0
    )
    avg_note_length = (
        float(notes_data["word_count"].mean())
        if not notes_data["word_count"].isnull().all()
        else 0.0
    )

    all_words = " ".join(notes_data["content"]).lower()
    words = re.findall(r"\w+", all_words)
    common_words = Counter(words).most_common(10)
    sorted_notes = notes_data.sort_values(by="word_count")

    longest_notes = sorted_notes.tail(3)["id"].tolist()
    shortest_notes = sorted_notes.head(3)["id"].tolist()

    return {
        "total_notes": int(len(notes)),
        "total_word_count": total_word_count,
        "avg_note_length": avg_note_length,
        "most_common_words": common_words,
        "longest_notes": longest_notes,
        "shortest_notes": shortest_notes,
    }
