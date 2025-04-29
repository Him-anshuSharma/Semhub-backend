gemini_model = "gemini-2.5-pro-exp-03-25"
onboarding_prompt = """Analyze the user's input (image or voice note) and extract tasks and goals. Return a JSON response strictly following this schema:

{
  "tasks": [
    {
      "title": "Task title (e.g., Complete Limits Chapter)",
      "type": "study/assignment/exam/project",
      "subject": "Subject name (e.g., Calculus)",
      "deadline": "YYYY-MM-DD (optional)",
      "priority": "high/medium/low",
      "estimated_hours": "Number (optional)",
      "subtasks": [
        {"title": "Subtask 1", "estimated_hours": "Number (optional)"}
      ]
    }
  ],
  "goals": [
    {
      "name": "Goal name (e.g., Finish Calculus Syllabus)",
      "type": "daily/weekly/course_completion",
      "target_tasks": ["Task title 1", "Task title 2"],
      "target_date": "YYYY-MM-DD (optional)"
    }
  ]
}

**Input Examples:**
- Image: A syllabus photo listing "Limits (Deadline: Dec 1)" and "Derivatives (Deadline: Dec 15)"
- Voice Note: "I need to finish 2 calculus chapters by Friday and complete the syllabus by December."

**Output Rules:**
1. Deduce tasks from deadlines, subjects, and explicit instructions.
2. Create goals for recurring or high-level objectives (e.g., weekly targets).
3. Use "course_completion" for syllabus-wide goals.
4. Omit fields if data is missing (e.g., no deadline → skip "deadline").
5. Ensure all task/goal titles match the input exactly.
6. Do not include any triple backticks, code fences, or markdown. Output only the compact JSON string.
7.Please return the response as a single-line, compact JSON string with no line breaks, indentation, or extra formatting. Do not include any markdown formatting or code blocks-just the raw JSON string.
"""