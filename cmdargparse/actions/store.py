import argparse
from typing import Annotated, Any, Mapping, Sequence

from cmdargparse.custom import (
    TANY,
    ArgumentParser,
    Namespace,
    decorator,
    is_multiple_values,
)


# ################################ ACTION ######################################


class StoreAction(argparse._StoreAction):

    def __init__(
        self,
        *args: Annotated[Any, "passthrough"],
        choicesmap: Mapping[TANY, TANY] | None = None,
        **kwargs: Annotated[Any, "passthrough"],
    ) -> None:
        assert not args, (
            "There should be no positional arguments if not explicitly "
            "specified. (The `argparse` module passes by keyword.)"
        )

        if "choices" in kwargs and choicesmap is not None:
            if any(s not in kwargs["choices"] for s in choicesmap.values()):
                raise ValueError(
                    "All mapped values in the choices mapping must be present "
                    "in the specified choices."
                )
            kwargs["choices"] = (
                *kwargs["choices"],
                *choicesmap.keys(),
            )

        super().__init__(*args, **kwargs)

        self.choicesmap = choicesmap

    @decorator.call
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Sequence[TANY] | TANY,
        option_string: str | None = None,
    ) -> None:
        if self.choicesmap is not None:
            values = (
                [self.choicesmap.get(v, v) for v in values]
                if is_multiple_values(values)
                else self.choicesmap.get(values, values)
            )
        setattr(namespace, self.dest, values)
