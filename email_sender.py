from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    def send(self, subject: str, body: str) -> None:
        ...


class ConsoleSender(EmailSender):
    def send(self, subject: str, body: str) -> None:
        divider = "=" * len(subject)
        print(f"{subject}")
        print(divider)
        print(body)
