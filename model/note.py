from dataclasses import dataclass


@dataclass
class Notes:
    title: str
    content: list


@dataclass
class Note:
    description: str
    time: str
    url: str
