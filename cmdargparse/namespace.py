import argparse
from typing import Any

import cmd2


# ################################ NAMESPACE ###################################


class Namespace(argparse.Namespace):

    def subcommand(self) -> Any:
        """Calls the selected subcommand."""

        # The function is 'None' for commands without subcommands.
        if self.cmd2_subcommand_func is None:
            raise RuntimeError(
                f"Command '{self.cmd2_statement.command}' does not have "
                "subcommands"
            )

        return self.cmd2_subcommand_func(self)

    def pfields(self, cmd: cmd2.Cmd, /) -> None:
        """Prints all fields using the feedback output function."""

        fields = tuple(
            attr
            for attr in self.__dict__
            if (
                # Skip all internalized attributes.
                not attr.startswith("_")
                # Skip all cmd2-related attributes.
                and not attr.startswith("cmd2")
            )
        )

        cmd.pfeedback("[Namespace]")

        if not fields:
            cmd.pfeedback("  (no fields)")
            return

        maxlen = max(
            len(attr)
            for attr in fields
            # <format-break>
        )

        for name in fields:
            cmd.pfeedback(
                f"  {str.ljust(name, maxlen)!s} :  {self.__dict__[name]!r}"
            )
