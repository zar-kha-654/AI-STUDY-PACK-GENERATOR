
import gradio as gr
from workflow import generate_study_pack


# ============================================================
# GENERATE STUDY PACK
# ============================================================

def create_study_pack(
    subject,
    topic,
    academic_level,
    learning_goal,
    study_time,
    learning_style,
    difficulty,
    exam_deadline,
    constraints
):

    # Combine all user inputs into one structured request
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

        # Run the complete 5-stage AI workflow
        result = generate_study_pack(
            student_input
        )

        # Get final refined study pack
        final_pack = result["final_pack"]

        # Convert final JSON into readable text
        output = f"""
# 📚 {final_pack.get("title", "AI Study Pack")}

## Overview

{final_pack.get("overview", "")}


## 🎯 Learning Objectives

"""

        for item in final_pack.get(
            "learning_objectives", []
        ):
            output += f"- {item}\n"

        output += "\n\n## 📝 Study Notes\n\n"

        for item in final_pack.get(
            "study_notes", []
        ):
            output += f"{item}\n\n"

        output += "\n## 🔑 Key Concepts\n\n"

        for item in final_pack.get(
            "key_concepts", []
        ):
            output += f"- {item}\n"

        output += "\n\n## 📖 Definitions\n\n"

        for item in final_pack.get(
            "definitions", []
        ):
            if isinstance(item, dict):
                term = item.get("term", "")
                definition = item.get(
                    "definition",
                    ""
                )
                output += (
                    f"**{term}:** {definition}\n\n"
                )
            else:
                output += f"- {item}\n"

        output += "\n## 💡 Examples\n\n"

        for item in final_pack.get(
            "examples", []
        ):
            output += f"{item}\n\n"

        output += "\n## ⚠️ Common Mistakes\n\n"

        for item in final_pack.get(
            "common_mistakes", []
        ):
            output += f"- {item}\n"

        output += "\n\n## 🧠 Flashcards\n\n"

        for i, card in enumerate(
            final_pack.get("flashcards", []),
            start=1
        ):

            if isinstance(card, dict):

                question = card.get(
                    "question",
                    ""
                )

                answer = card.get(
                    "answer",
                    ""
                )

                output += (
                    f"### Flashcard {i}\n"
                    f"**Q:** {question}\n\n"
                    f"**A:** {answer}\n\n"
                )

            else:
                output += f"- {card}\n"

        output += "\n## 📝 Multiple Choice Questions\n\n"

        for i, mcq in enumerate(
            final_pack.get("mcqs", []),
            start=1
        ):

            if isinstance(mcq, dict):

                question = mcq.get(
                    "question",
                    ""
                )

                options = mcq.get(
                    "options",
                    []
                )

                output += (
                    f"### {i}. {question}\n\n"
                )

                for option in options:
                    output += f"- {option}\n"

                output += "\n"

            else:
                output += (
                    f"### {i}. {mcq}\n\n"
                )

        output += "\n## ✍️ Short Questions\n\n"

        for i, question in enumerate(
            final_pack.get("short_questions", []),
            start=1
        ):
            output += f"{i}. {question}\n\n"

        output += "\n## ✅ Answer Key\n\n"

        for i, answer in enumerate(
            final_pack.get("answer_key", []),
            start=1
        ):
            output += f"{i}. {answer}\n"

        output += "\n\n## 🗓️ Recommended Study Plan\n\n"

        for item in final_pack.get(
            "study_plan", []
        ):
            output += f"- {item}\n"

        return output

    except Exception as error:

        return (
            "## ❌ Error\n\n"
            f"Something went wrong:\n\n"
            f"`{str(error)}`"
        )


# ============================================================
# GRADIO INTERFACE
# ============================================================

with gr.Blocks(
    title="AI Study Pack Generator"
) as demo:

    gr.Markdown(
        """
# 📚 AI Study Pack Generator

### Personalized learning powered by a 5-stage AI workflow

Generate a customized study pack using:

**Context Parsing → Planning → Content Generation → Assessment Review → Refinement**
"""
    )

    with gr.Row():

        # ----------------------------------------------------
        # LEFT SIDE — USER INPUT
        # ----------------------------------------------------

        with gr.Column(
            scale=1
        ):

            gr.Markdown(
                "## 🎓 Student Information"
            )

            subject = gr.Textbox(
                label="Subject",
                placeholder="e.g. Data Structures",
            )

            topic = gr.Textbox(
                label="Topic",
                placeholder="e.g. Arrays and Indexing",
            )

            academic_level = gr.Dropdown(
                choices=[
                    "Beginner",
                    "Intermediate",
                    "Advanced",
                    "University Undergraduate",
                    "Exam Preparation"
                ],
                label="Academic Level",
                value="University Undergraduate"
            )

            learning_goal = gr.Textbox(
                label="Learning Goal",
                placeholder=(
                    "e.g. Understand arrays and "
                    "prepare for my university exam"
                ),
                lines=3
            )

            study_time = gr.Textbox(
                label="Available Study Time",
                placeholder="e.g. 2 hours"
            )

            learning_style = gr.Dropdown(
                choices=[
                    "Simple explanations",
                    "Examples",
                    "Step-by-step",
                    "Visual explanations",
                    "Practice questions",
                    "Mixed"
                ],
                label="Preferred Learning Style",
                value="Mixed"
            )

            difficulty = gr.Dropdown(
                choices=[
                    "Easy",
                    "Medium",
                    "Hard",
                    "Exam-level"
                ],
                label="Difficulty",
                value="Medium"
            )

            exam_deadline = gr.Textbox(
                label="Exam / Deadline",
                placeholder=(
                    "e.g. Exam in 10 days "
                    "or No deadline"
                )
            )

            constraints = gr.Textbox(
                label="Important Constraints",
                placeholder=(
                    "e.g. Focus on indexing, "
                    "avoid advanced topics"
                ),
                lines=3
            )

            generate_button = gr.Button(
                "🚀 Generate Study Pack",
                variant="primary"
            )


        # ----------------------------------------------------
        # RIGHT SIDE — OUTPUT
        # ----------------------------------------------------

        with gr.Column(
            scale=2
        ):

            gr.Markdown(
                "## 📖 Your Personalized Study Pack"
            )

            output = gr.Markdown(
                value=(
                    "Your generated study pack "
                    "will appear here."
                )
            )


    # --------------------------------------------------------
    # BUTTON ACTION
    # --------------------------------------------------------

    generate_button.click(
        fn=create_study_pack,

        inputs=[
            subject,
            topic,
            academic_level,
            learning_goal,
            study_time,
            learning_style,
            difficulty,
            exam_deadline,
            constraints
        ],

        outputs=output
    )


# ============================================================
# LAUNCH
# ============================================================

if __name__ == "__main__":

    demo.launch(
        share=True
    )
