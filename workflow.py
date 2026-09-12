
# ============================================================
# AI STUDY PACK GENERATOR
# workflow.py
# ============================================================

import os
import json
import re

from groq import Groq

from prompts import (
    SYSTEM_PROMPT,
    CONTEXT_PARSER_PROMPT,
    PLANNING_PROMPT,
    CONTENT_GENERATION_PROMPT,
    ASSESSMENT_REVIEW_PROMPT,
    REFINEMENT_PROMPT,
)


# ============================================================
# CONFIGURATION
# ============================================================

# Current Groq model
MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

MAX_RETRIES = 3


# ============================================================
# GROQ CLIENT
# ============================================================

def get_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Please add your Groq API key."
        )

    return Groq(api_key=api_key)


# ============================================================
# JSON EXTRACTION
# ============================================================

def extract_json(text):

    text = text.strip()

    text = re.sub(
        r"```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```\s*$",
        "",
        text
    )

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL
    )

    if match:

        try:
            return json.loads(match.group())

        except json.JSONDecodeError:
            pass

    raise ValueError(
        "The AI returned invalid JSON."
    )


# ============================================================
# AI CALL WITH ERROR HANDLING
# ============================================================

def call_ai(
    prompt,
    temperature=0.3
):

    client = get_client()

    last_error = None

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:

            response = client.chat.completions.create(

                model=MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=temperature,

                response_format={
                    "type": "json_object"
                }
            )

            result = (
                response
                .choices[0]
                .message
                .content
            )

            return extract_json(result)

        except Exception as error:

            last_error = error

            print(
                f"AI call failed "
                f"(attempt {attempt}/{MAX_RETRIES})"
            )

            print(error)

    raise RuntimeError(
        f"AI workflow failed after "
        f"{MAX_RETRIES} attempts: "
        f"{last_error}"
    )


# ============================================================
# STAGE 1
# CONTEXT PARSING
# ============================================================

def parse_context(student_input):

    print(
        "Running 1/5 Context Parsing..."
    )

    prompt = CONTEXT_PARSER_PROMPT.format(
        student_input=student_input
    )

    context = call_ai(
        prompt,
        temperature=0.2
    )

    print(
        "1/5 Context Parsing complete"
    )

    return context


# ============================================================
# STAGE 2
# PLANNING
# ============================================================

def create_plan(context):

    print(
        "Running 2/5 Planning..."
    )

    prompt = PLANNING_PROMPT.format(
        context=json.dumps(
            context,
            indent=2
        )
    )

    plan = call_ai(
        prompt,
        temperature=0.3
    )

    print(
        "2/5 Planning complete"
    )

    return plan


# ============================================================
# STAGE 3
# CONTENT GENERATION
# ============================================================

def generate_content(context, plan):

    print(
        "Running 3/5 Content Generation..."
    )

    prompt = CONTENT_GENERATION_PROMPT.format(

        context=json.dumps(
            context,
            indent=2
        ),

        plan=json.dumps(
            plan,
            indent=2
        )
    )

    content = call_ai(
        prompt,
        temperature=0.5
    )

    print(
        "3/5 Content Generation complete"
    )

    return content


# ============================================================
# STAGE 4
# ASSESSMENT REVIEW
# ============================================================

def review_assessment(context, content):

    print(
        "Running 4/5 Assessment Review..."
    )

    prompt = ASSESSMENT_REVIEW_PROMPT.format(

        context=json.dumps(
            context,
            indent=2
        ),

        content=json.dumps(
            content,
            indent=2
        )
    )

    review = call_ai(
        prompt,
        temperature=0.2
    )

    print(
        "4/5 Assessment Review complete"
    )

    return review


# ============================================================
# STAGE 5
# REFINEMENT
# ============================================================

def refine_pack(
    context,
    plan,
    content,
    review
):

    print(
        "Running 5/5 Refinement..."
    )

    prompt = REFINEMENT_PROMPT.format(

        context=json.dumps(
            context,
            indent=2
        ),

        plan=json.dumps(
            plan,
            indent=2
        ),

        content=json.dumps(
            content,
            indent=2
        ),

        review=json.dumps(
            review,
            indent=2
        )
    )

    final_pack = call_ai(
        prompt,
        temperature=0.4
    )

    print(
        "5/5 Refinement complete"
    )

    return final_pack


# ============================================================
# COMPLETE AI WORKFLOW
# ============================================================

def generate_study_pack(student_input):

    workflow_log = []

    # STAGE 1
    workflow_log.append(
        "Running 1/5 Context Parsing"
    )

    context = parse_context(
        student_input
    )

    workflow_log.append(
        "1/5 Context Parsing complete"
    )

    # STAGE 2
    workflow_log.append(
        "Running 2/5 Planning"
    )

    plan = create_plan(
        context
    )

    workflow_log.append(
        "2/5 Planning complete"
    )

    # STAGE 3
    workflow_log.append(
        "Running 3/5 Content Generation"
    )

    content = generate_content(
        context,
        plan
    )

    workflow_log.append(
        "3/5 Content Generation complete"
    )

    # STAGE 4
    workflow_log.append(
        "Running 4/5 Assessment Review"
    )

    review = review_assessment(
        context,
        content
    )

    workflow_log.append(
        "4/5 Assessment Review complete"
    )

    # STAGE 5
    workflow_log.append(
        "Running 5/5 Refinement"
    )

    final_pack = refine_pack(
        context,
        plan,
        content,
        review
    )

    workflow_log.append(
        "5/5 Refinement complete"
    )

    return {

        "context": context,

        "plan": plan,

        "content": content,

        "review": review,

        "final_pack": final_pack,

        "workflow_log": workflow_log
    }
