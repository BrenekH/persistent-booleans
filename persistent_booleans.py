"""(Almost) Transparent Persistent Boolean Values
Based on github.com/zachvance/persistent_switch, this module allows the creation of persistent boolean values that are almost transparent in the code.
The idea sounds solid on paper, but in practice they are very limited for the complex code that creates them.
As such this module should not be used in any serious project. Literally any database system is better than this.
"""

# Original idea: Zach Vance (github.com/zachvance)
# Rewritten with transparency by: Brenek Harrison (github.com/BrenekH)

from __future__ import annotations # This is Python 3.7+ and really only fixes the type hint for ToggleableBoolean.toggle()
from pathlib import Path
from json import dump, load
from typing import TypedDict, Union

default_file = Path.cwd() / "store.json"

def explode_default_store():
    """Delete the default storage file.
The user is expected to manage any other storage files they use.
    """
    default_file.unlink(missing_ok=True)

class Store:
    """Store is the top-level logical container of persistent booleans.
    To avoid data race conditions, only one instance of Store should point to any given file.
    """
    def __init__(self, filename: Union[Path, str]=None):
        self.file: Path = default_file if filename == None else Path(filename)
        self.__store: TypedDict[str, ToggleableBoolean] = {}

        self.load()

    def save(self) -> None:
        """Save to the storage file
        """
        with self.file.open("w") as f:
            dump(self.__store, f, indent=4)

    def load(self) -> None:
        """Load from the storage file
        """
        if not self.file.exists():
            self.save()

        with self.file.open() as f:
            for (k, v) in load(f):
                setattr(self, k, bool(v))

    def __setattr__(self, name: str, value) -> None:
        if isinstance(value, (bool, ToggleableBoolean)):
            tb = ToggleableBoolean(1) if value else ToggleableBoolean(0)
            self.__store[name] = tb
            self.save()
            return super().__setattr__(name, tb)

        return super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        del self.__store[name]

        return super().__delattr__(name)

class ToggleableBoolean(int):
    """Subclass of int that provides a toggle method
    """
    def __new__(cls, value: int):
        if value not in set(0, 1):
            raise ValueError(f"Invalid value {value} for ToggleableBoolean. Must be either 0 or 1.")
        return super(cls, cls).__new__(cls, value)

    def toggle(self) -> ToggleableBoolean:
        """toggle returns a new ToggleableBoolean that is the opposite of the one that toggle is called on.

        Returns:
            ToggleableBoolean: The new toggled boolean.
        """
        return self.__class__(1 if self == 0 else 0)
