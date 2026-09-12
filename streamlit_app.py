
import streamlit as st
import json

from workflow import generate_study_pack


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Study Pack Generator",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📚 AI Study Pack Generator")

st.markdown(
    """
### Personalized learning powered by a 5-stage AI workflow

**Context Parsing → Planning → Content Generation → Assessment Review → Refinement**
"""
)


# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.header("🎓 Student Information")

subject = st.sidebar.text_input(
    "Subject",
    placeholder="e.g. Data Structures"
)

topic = st.sidebar.text_input(
    "Topic",
    placeholder="e.g. Arrays and Indexing"
)

academic_level = st.sidebar.selectbox(
    "Academic Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced",
        "University Undergraduate",
        "Exam Preparation"
    ],
    index=3
)

learning_goal = st.sidebar.text_area(
    "Learning Goal",
    placeholder="e.g. Understand arrays for my university exam"
)

study_time = st.sidebar.text_input(
    "Available Study Time",
    placeholder="e.g. 2 hours"
)

learning_style = st.sidebar.selectbox(
    "Preferred Learning Style",
    [
        "Simple explanations",
        "Examples",
        "Step-by-step",
        "Visual explanations",
        "Practice questions",
        "Mixed"
    ],
    index=5
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    [
        "Easy",
        "Medium",
        "Hard",
        "Exam-level"
    ],
    index=1
)

exam_deadline = st.sidebar.text_input(
    "Exam / Deadline",
    placeholder="e.g. Exam in 10 days"
)

constraints = st.sidebar.text_area(
    "Important Constraints",
    placeholder="e.g. Focus on indexing"
)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate = st.sidebar.button(
    "🚀 Generate Study Pack",
    type="primary"
)


# ============================================================
# GENERATE STUDY PACK
# ============================================================

if generate:

    if not subject or not topic:

        st.warning(
            "Please enter at least the subject and topic."
        )

    else:

        student_input = f"""
Subject: {subject}

Topic: {topic}

Academic Level: {academic_level}

Learning Goal: {learning_goal}

Available Study Time: {study_time}

Preferred Learning Style: {learning_style}

Difficulty Level: {difficulty}

Exam / Deadline: {exam_deadline}

Important Constraints: {constraints}
"""

        try:

            with st.spinner(
                "🤖 AI is generating your personalized study pack..."
            ):

                result = generate_study_pack(
                    student_input
                )

            final_pack = result["final_pack"]

            st.success(
                "🎉 Your study pack is ready!"
            )

            # ------------------------------------------------
            # OVERVIEW
            # ------------------------------------------------

            st.header(
                final_pack.get(
                    "title",
                    "📚 AI Study Pack"
                )
            )

            st.subheader("Overview")

            st.write(
                final_pack.get(
                    "overview",
                    ""
                )
            )

            # ------------------------------------------------
            # LEARNING OBJECTIVES
            # ------------------------------------------------

            st.subheader(
                "🎯 Learning Objectives"
            )

            for item in final_pack.get(
                "learning_objectives",
                []
            ):
                st.markdown(
                    f"- {item}"
                )

            # ------------------------------------------------
            # STUDY NOTES
            # ------------------------------------------------

            st.subheader(
                "📝 Study Notes"
            )

            for item in final_pack.get(
                "study_notes",
                []
            ):
                st.markdown(
                    str(item)
                )

            # ------------------------------------------------
            # KEY CONCEPTS
            # ------------------------------------------------

            st.subheader(
                "🔑 Key Concepts"
            )

            for item in final_pack.get(
                "key_concepts",
                []
            ):
                st.markdown(
                    f"- {item}"
                )

            # ------------------------------------------------
            # DEFINITIONS
            # ------------------------------------------------

            st.subheader(
                "📖 Definitions"
            )

            for item in final_pack.get(
                "definitions",
                []
            ):

                if isinstance(item, dict):

                    st.markdown(
                        f"**{item.get('term', '')}:** "
                        f"{item.get('definition', '')}"
                    )

                else:

                    st.markdown(
                        f"- {item}"
                    )

            # ------------------------------------------------
            # EXAMPLES
            # ------------------------------------------------

            st.subheader(
                "💡 Examples"
            )

            for item in final_pack.get(
                "examples",
                []
            ):
                st.markdown(
                    str(item)
                )

            # ------------------------------------------------
            # COMMON MISTAKES
            # ------------------------------------------------

            st.subheader(
                "⚠️ Common Mistakes"
            )

            for item in final_pack.get(
                "common_mistakes",
                []
            ):
                st.markdown(
                    f"- {item}"
                )

            # ------------------------------------------------
            # FLASHCARDS
            # ------------------------------------------------

            st.subheader(
                "🧠 Flashcards"
            )

            for i, card in enumerate(
                final_pack.get(
                    "flashcards",
                    []
                ),
                start=1
            ):

                with st.expander(
                    f"Flashcard {i}"
                ):

                    if isinstance(card, dict):

                        st.markdown(
                            f"**Question:** "
                            f"{card.get('question', '')}"
                        )

                        st.markdown(
                            f"**Answer:** "
                            f"{card.get('answer', '')}"
                        )

                    else:

                        st.write(card)

            # ------------------------------------------------
            # MCQs
            # ------------------------------------------------

            st.subheader(
                "📝 Multiple Choice Questions"
            )

            for i, mcq in enumerate(
                final_pack.get(
                    "mcqs",
                    []
                ),
                start=1
            ):

                if isinstance(mcq, dict):

                    st.markdown(
                        f"**{i}. "
                        f"{mcq.get('question', '')}**"
                    )

                    for option in mcq.get(
                        "options",
                        []
                    ):
                        st.markdown(
                            f"- {option}"
                        )

                else:

                    st.markdown(
                        f"**{i}. {mcq}**"
                    )

            # ------------------------------------------------
            # SHORT QUESTIONS
            # ------------------------------------------------

            st.subheader(
                "✍️ Short Questions"
            )

            for i, question in enumerate(
                final_pack.get(
                    "short_questions",
                    []
                ),
                start=1
            ):
                st.markdown(
                    f"{i}. {question}"
                )

            # ------------------------------------------------
            # ANSWER KEY
            # ------------------------------------------------

            st.subheader(
                "✅ Answer Key"
            )

            for i, answer in enumerate(
                final_pack.get(
                    "answer_key",
                    []
                ),
                start=1
            ):
                st.markdown(
                    f"**{i}.** {answer}"
                )

            # ------------------------------------------------
            # STUDY PLAN
            # ------------------------------------------------

            st.subheader(
                "🗓️ Recommended Study Plan"
            )

            for item in final_pack.get(
                "study_plan",
                []
            ):
                st.markdown(
                    f"- {item}"
                )

            # ------------------------------------------------
            # DOWNLOAD
            # ------------------------------------------------

            st.subheader(
                "💾 Export"
            )

            json_data = json.dumps(
                final_pack,
                indent=2
            )

            st.download_button(
                "⬇️ Download Study Pack",
                data=json_data,
                file_name="study_pack.json",
                mime="application/json"
            )

        except Exception as error:

            st.error(
                f"❌ Something went wrong: {error}"
            )

else:

    st.info(
        """
        👈 Enter your study information in the sidebar
        and click **Generate Study Pack**.

        Your request will pass through:

        **1. Context Parsing**
        → **2. Planning**
        → **3. Content Generation**
        → **4. Assessment Review**
        → **5. Refinement**
        """
    )
