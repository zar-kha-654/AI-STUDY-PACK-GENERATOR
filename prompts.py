
SYSTEM_PROMPT = """
You are an expert AI study assistant.

Your job is to create accurate, structured, personalized,
student-friendly educational content.

Follow the user's requested:
- subject
- topic
- academic level
- learning goal
- available study time
- preferred learning style
- difficulty

Never invent facts when you are uncertain.

Return valid JSON whenever JSON output is requested.
"""


CONTEXT_PARSER_PROMPT = """
Analyze the student's input and convert it into a structured
learning context.

Student information:
{student_input}

Extract:

1. Subject
2. Topic
3. Academic level
4. Learning goal
5. Available study time
6. Preferred learning style
7. Difficulty level
8. Exam or deadline information
9. Important constraints
10. Missing information

Return ONLY valid JSON in this format:

{{
    "subject": "",
    "topic": "",
    "academic_level": "",
    "learning_goal": "",
    "study_time": "",
    "learning_style": "",
    "difficulty": "",
    "exam_or_deadline": "",
    "constraints": [],
    "missing_information": []
}}
"""


PLANNING_PROMPT = """
You are the planning stage of an AI study-pack generator.

Use the following learning context:

{context}

Create a personalized learning plan.

The plan should determine:

1. Main learning objectives
2. Important subtopics
3. Recommended study sequence
4. Estimated time for each section
5. Difficulty progression
6. What concepts require special attention
7. Recommended practice strategy

Return ONLY valid JSON:

{{
    "learning_objectives": [],
    "subtopics": [],
    "study_sequence": [],
    "time_allocation": [],
    "difficulty_progression": [],
    "focus_areas": [],
    "practice_strategy": []
}}
"""


CONTENT_GENERATION_PROMPT = """
You are the content-generation stage of an AI study-pack system.

Student context:

{context}

Learning plan:

{plan}

Generate a complete study pack based on the plan.

Include:

1. A concise topic explanation
2. Structured study notes
3. Key concepts
4. Important definitions
5. Examples
6. Common mistakes
7. Flashcards
8. Multiple-choice questions
9. Short-answer questions
10. An answer key

Make the content appropriate for the student's academic level.

Return ONLY valid JSON:

{{
    "overview": "",
    "notes": [],
    "key_concepts": [],
    "definitions": [],
    "examples": [],
    "common_mistakes": [],
    "flashcards": [],
    "mcqs": [],
    "short_questions": [],
    "answer_key": []
}}
"""


ASSESSMENT_REVIEW_PROMPT = """
You are the assessment-review stage of an AI study-pack generator.

Review the following study pack.

Study context:

{context}

Study pack:

{content}

Check:

1. Factual accuracy
2. Relevance to the topic
3. Difficulty level
4. Quality of MCQs
5. Whether MCQ answers are correct
6. Whether explanations are correct
7. Duplicate questions
8. Ambiguous questions
9. Missing important concepts
10. Alignment with the learning objectives

Return ONLY valid JSON:

{{
    "accuracy_score": 0,
    "relevance_score": 0,
    "difficulty_score": 0,
    "assessment_score": 0,
    "issues": [],
    "missing_concepts": [],
    "duplicate_items": [],
    "recommended_changes": [],
    "approved": false
}}
"""


REFINEMENT_PROMPT = """
You are the final refinement stage of an AI study-pack generator.

Student context:

{context}

Original learning plan:

{plan}

Generated study pack:

{content}

Assessment review:

{review}

Improve the study pack according to the review.

Requirements:

1. Fix factual or logical errors.
2. Remove duplicates.
3. Improve unclear explanations.
4. Add missing important concepts.
5. Correct incorrect MCQ answers.
6. Make the difficulty appropriate.
7. Keep the material concise enough to study.
8. Preserve useful content that already works.

Return ONLY valid JSON:

{{
    "title": "",
    "overview": "",
    "learning_objectives": [],
    "study_notes": [],
    "key_concepts": [],
    "definitions": [],
    "examples": [],
    "common_mistakes": [],
    "flashcards": [],
    "mcqs": [],
    "short_questions": [],
    "answer_key": [],
    "study_plan": []
}}
"""
