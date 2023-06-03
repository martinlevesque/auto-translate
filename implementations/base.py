from dataclasses import dataclass


@dataclass
class Base:
    target_language: str = "en"

    def translate(self, chunks):
        raise NotImplementedError()
