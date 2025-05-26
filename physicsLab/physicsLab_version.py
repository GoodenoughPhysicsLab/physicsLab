from typing import Tuple

class _Version:
    def __init__(self, major: int, minor: int, patch: int) -> None:
        if major < 0 \
                or minor < 0 \
                or patch < 0:
            raise ValueError

        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def to_tuple(self) -> Tuple[int, int, int]:
        return self.major, self.minor, self.patch

    def __eq__(self, value: object) -> bool:
        return self.to_tuple() == value

    def __ne__(self, value: object) -> bool:
        return self.to_tuple() != value

    def __gt__(self, value: object) -> bool:
        return self.to_tuple() > value

    def __ge__(self, value: object) -> bool:
        return self.to_tuple() >= value

    def __lt__(self, value: object) -> bool:
        return self.to_tuple() < value

    def __le__(self, value: object) -> bool:
        return self.to_tuple() <= value

__version__ = _Version(2, 0, 5)
