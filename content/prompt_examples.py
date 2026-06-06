CONVERSATION_FIELDS = [
    ("build_goal", "What are you trying to build?"),
    ("target_user", "Who is your target user?"),
    ("materials", "What materials or tools are required?"),
    ("progress", "What have you already done?"),
    ("blocker", "What is blocking you right now?"),
    ("help_type", "What kind of help do you want?"),
    ("expected_output", "What output do you expect?"),
]


def suggested_prompt(values: dict[str, str]) -> str:
    return (
        "I am building {build_goal} for {target_user}. "
        "The required materials or tools are {materials}. "
        "So far, I have {progress}. "
        "My current blocker is {blocker}. "
        "Please help with {help_type} and produce {expected_output}."
    ).format(**{key: values.get(key, "not specified") or "not specified" for key, _ in CONVERSATION_FIELDS})
