import json
import random
from pathlib import Path

import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "pyqs.json"


def load_questions(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def init_state():
    if "bookmarks" not in st.session_state:
        st.session_state.bookmarks = set()
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempted" not in st.session_state:
        st.session_state.attempted = 0
    if "answered" not in st.session_state:
        st.session_state.answered = {}


def apply_filters(questions, years, subjects, levels, search_text):
    filtered = []
    for q in questions:
        if years and q["year"] not in years:
            continue
        if subjects and q["subject"] not in subjects:
            continue
        if levels and q["difficulty"] not in levels:
            continue
        if search_text and search_text.lower() not in q["question"].lower():
            continue
        filtered.append(q)
    return filtered


def main():
    st.set_page_config(page_title="UPSC PYQ App", page_icon=":books:", layout="wide")
    st.title("UPSC PYQ Practice App")
    st.caption("Practice UPSC previous year questions with filters and quiz mode.")

    questions = load_questions(DATA_PATH)
    init_state()

    all_years = sorted({q["year"] for q in questions}, reverse=True)
    all_subjects = sorted({q["subject"] for q in questions})
    all_levels = sorted({q["difficulty"] for q in questions})

    with st.sidebar:
        st.header("Filters")
        years = st.multiselect("Year", all_years)
        subjects = st.multiselect("Subject", all_subjects)
        levels = st.multiselect("Difficulty", all_levels)
        search_text = st.text_input("Search question")

        st.divider()
        st.header("Session Stats")
        st.metric("Attempted", st.session_state.attempted)
        st.metric("Correct", st.session_state.score)
        accuracy = (
            (st.session_state.score / st.session_state.attempted) * 100
            if st.session_state.attempted
            else 0
        )
        st.metric("Accuracy", f"{accuracy:.1f}%")

        if st.button("Reset Session"):
            st.session_state.score = 0
            st.session_state.attempted = 0
            st.session_state.answered = {}
            st.rerun()

    filtered_questions = apply_filters(questions, years, subjects, levels, search_text)

    top_col1, top_col2 = st.columns([1, 1])
    with top_col1:
        st.write(f"Showing **{len(filtered_questions)}** question(s)")
    with top_col2:
        random_mode = st.toggle("Random Question Mode", value=False)

    display_questions = filtered_questions[:]
    if random_mode and filtered_questions:
        display_questions = [random.choice(filtered_questions)]

    tabs = st.tabs(["Practice", "Bookmarks"])

    with tabs[0]:
        if not display_questions:
            st.info("No questions found for selected filters.")
        for q in display_questions:
            with st.container(border=True):
                st.subheader(f"Q{q['id']} ({q['year']} - {q['subject']} - {q['difficulty']})")
                st.write(q["question"])

                selected = st.radio(
                    "Choose your answer",
                    options=list(range(len(q["options"]))),
                    format_func=lambda i: q["options"][i],
                    key=f"choice_{q['id']}",
                )

                action_col1, action_col2, _ = st.columns([1, 1, 2])
                with action_col1:
                    if st.button("Submit", key=f"submit_{q['id']}"):
                        if q["id"] not in st.session_state.answered:
                            answer_index = q.get("answer")
                            if answer_index is None:
                                st.session_state.answered[q["id"]] = {
                                    "selected": selected,
                                    "correct": None,
                                }
                            else:
                                st.session_state.attempted += 1
                                correct = selected == answer_index
                                if correct:
                                    st.session_state.score += 1
                                st.session_state.answered[q["id"]] = {
                                    "selected": selected,
                                    "correct": correct,
                                }

                with action_col2:
                    bookmarked = q["id"] in st.session_state.bookmarks
                    label = "Unbookmark" if bookmarked else "Bookmark"
                    if st.button(label, key=f"bookmark_{q['id']}"):
                        if bookmarked:
                            st.session_state.bookmarks.remove(q["id"])
                        else:
                            st.session_state.bookmarks.add(q["id"])
                        st.rerun()

                if q["id"] in st.session_state.answered:
                    result = st.session_state.answered[q["id"]]
                    if result["correct"] is True:
                        st.success("Correct answer")
                    elif result["correct"] is False:
                        st.error("Incorrect answer")
                    else:
                        st.info("Answer key not available for this question.")

                    if q.get("answer") is not None:
                        st.write(f"**Correct Option:** {q['options'][q['answer']]}")
                    else:
                        st.write("**Correct Option:** Not available")

                    st.caption(f"Explanation: {q['explanation']}")
                    st.caption(f"Source: {q['source']}")

    with tabs[1]:
        bookmarked_items = [q for q in questions if q["id"] in st.session_state.bookmarks]
        if not bookmarked_items:
            st.info("No bookmarked questions yet.")
        for q in bookmarked_items:
            with st.container(border=True):
                st.subheader(f"Q{q['id']} ({q['year']} - {q['subject']})")
                st.write(q["question"])
                if q.get("answer") is not None:
                    st.write(f"**Answer:** {q['options'][q['answer']]}")
                else:
                    st.write("**Answer:** Not available")


if __name__ == "__main__":
    main()
