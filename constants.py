gemini_model = "gemini-2.5-pro-exp-03-25"
onboarding_prompt = """
Analyze the user's input (image or voice note) to identify and extract actionable tasks and broader goals. Return a compact, single-line JSON strictly following this schema:

{ "tasks": [ { "title": "Task title (e.g., Complete Limits Chapter)", "type": "study/assignment/exam/project", "subject": "Subject name (e.g., Calculus)", "deadline": "YYYY-MM-DD (optional)", "priority": "high/medium/low", "estimated_hours": "Number (optional)", "subtasks": [ {"title": "Subtask 1", "estimated_hours": "Number (optional)"} ] } ], "goals": [ { "name": "Goal name (e.g., Finish Calculus Syllabus)", "type": "daily/weekly/course_completion", "target_tasks": ["Exact task titles as listed above"], "target_date": "YYYY-MM-DD (optional)" } ] }

Examples of Input:

Image: A syllabus photo listing "Limits (Deadline: Dec 1)" and "Derivatives (Deadline: Dec 15)"

Voice Note: "I need to finish two calculus chapters by Friday and complete the syllabus by December."

Output Guidelines:

Extract tasks based on clear instructions, deadlines, subjects, or topics.

Group related or high-level tasks under appropriate goals (e.g., course completion or weekly plans).

Use "course_completion" for full syllabus goals, "weekly" for multi-day targets, or "daily" for short-term goals.

If any field is missing from input (like deadline or estimated time), omit it from the JSON.

Ensure goal "target_tasks" strictly reference exact task titles used in the "tasks" array.

Do not add extra formatting—no triple backticks, no line breaks, no indentation, no markdown.

Return the JSON as a compact single-line string only.
"""