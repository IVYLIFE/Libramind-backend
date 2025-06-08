def generate_remainder_email(
    student_name: str, book_title: str, due_date: str, days_remaining: int
) -> tuple[str, str]:
    subject = f"Library Reminder: '{book_title}' due in {days_remaining} day(s)"
    body = f"""
    <h2>Hi {student_name},</h2>
    <p>This is a friendly reminder that the book <b>'{book_title}'</b> is due on <b>{due_date}</b>.</p>
    <p>Please return or renew it on time to avoid penalties.</p>
    <p>Thank you,<br>Library Management</p>
    """
    return subject, body
