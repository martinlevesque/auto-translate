from dataclasses import dataclass


@dataclass
class Base:
    name: str = "base"

    @staticmethod
    def concatenate_all_content(chunks):
        return " ".join([str(chunk["content"]) for chunk in chunks])
