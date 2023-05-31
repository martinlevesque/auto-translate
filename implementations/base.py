from dataclasses import dataclass


@dataclass
class Base:
    target_language: str = "english"

    def translate(self, chunks):
        raise NotImplementedError()
