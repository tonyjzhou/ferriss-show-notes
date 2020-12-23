import re
from dataclasses import dataclass


@dataclass
class Notes:
    title: str
    content: list

    def filename(self) -> str:
        title_regexp = re.compile(r'(.+) — .+\(#(.+)\)')
        title_match = title_regexp.match(self.title)
        if title_match:
            simplified, number = title_match.group(1), title_match.group(2)
            return f"{simplified.replace(' ', '_')}_{number}.html"

        title_regexp = re.compile(r'(.+) \(#(.+)\)')
        title_match = title_regexp.match(self.title)
        if title_match:
            simplified, number = title_match.group(1), title_match.group(2)
            simplified = re.sub(r'\W+', ' ', simplified)
            return f"{simplified.replace(' ', '_')}_{number}.html"

        return f"{self.title}.html"


@dataclass
class Note:
    description: str
    time: str
    url: str


@dataclass
class InputUrl:
    blog: str
    youtube: str
