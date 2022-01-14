from dataclasses import dataclass

@dataclass
class Mail:
    email: str
    subject: str
    content: str
    id: int = 0