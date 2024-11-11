import datetime

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class User:
    id: int
    username: str
    created_at: datetime.datetime

    def __eq__(self, other) -> bool:
        return self.created_at == other.created_at
    
    def __lt__(self, other) -> bool:
        return self.created_at < other.created_at
    
    def __gt__(self, other) -> bool:
        return self.created_at > other.created_at

    def convert_to_date(self, format="%d/%m/%Y, %H:%M:%S") -> str:
        return self.created_at.strftime(format)

@dataclass
class Admin:
    id: int