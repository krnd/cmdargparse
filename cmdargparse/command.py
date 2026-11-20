import argparse
import dataclasses
import types
import typing
from typing import Any, Callable, Optional, Tuple, Type, TypeVar

import cmd2

from .field import _DeclFormSpecifier, _FieldDecls
from .namespace import Namespace
from .parser import ArgumentParser


# ################################ TYPING ######################################


TSELF = TypeVar("TSELF", cmd2.Cmd, cmd2.CommandSet)
TARGUMENT = TypeVar("TARGUMENT", bound=object)
TRETURN = TypeVar("TRETURN", Optional[bool], bool, None)


# ################################ METACLASS ###################################


class _cmdcommand(type):

    # ################## DECORATOR #########################

    def __call__(
        cls,
        argtype: Type[TARGUMENT],
        /,
        *,
        subcommands: bool = False,
        subcommand_to: str | Tuple[str, str] | None = None,
    ) -> Callable[
        [Callable[[TSELF, TARGUMENT], TRETURN]],
        Callable[[TSELF, TARGUMENT], TRETURN],
    ]:
        """Decorate as command function."""

        parser = ArgumentParser()

        _dcfields = dataclasses.fields(
            argtype  # pyright: ignore[reportArgumentType]
        )
        _fieldtypes = typing.get_type_hints(argtype, include_extras=True)

        if subcommand_to is not None:
            _inherited = {
                field.name
                for base in argtype.__bases__
                if dataclasses.is_dataclass(base)
                for field in dataclasses.fields(base)
            }
            _dcfields = tuple(
                field for field in _dcfields if field.name not in _inherited
            )

        default_form: _DeclFormSpecifier
        default_form = getattr(argtype, "_cmdargparse_default_form")

        for field in _dcfields:
            decls: _FieldDecls | None
            decls = field.metadata["decls"]

            name_or_flags = (
                ()  # Arguments are solely specified using the 'dest' keyword.
                if decls is None
                else argparse_name_or_flags(
                    field.name,
                    decls,
                    default_form=default_form,
                )
            )

            args: dict[str, Any]
            args = dict(field.metadata["args"])

            assert "dest" not in args, (
                "Specifying 'dest' directly is not supported."
                # <format-break>
            )
            args["dest"] = field.name

            if (
                args.get("action", None)
                in ("store_true", "store_false", "store_const")
                # <format-break>
            ):
                # Remove arguments for 'const' and 'type' if specified.
                if args["action"] != "store_const":
                    args.pop("const", ...)
                args.pop("type", ...)

                parser.add_argument(*name_or_flags, **args)

                continue

            # Resolve the type from the fields type annotation.
            (_type, _nargs) = argparse_type(_fieldtypes[field.name])
            if args.get("type", None) is None:
                args["type"] = _type
            if args.get("nargs", None) is None and _nargs is not None:
                args["nargs"] = _nargs

            # Remove custom unspecified arguments.
            if args.get("choicesmap", None) is None:
                args.pop("choicesmap", ...)

            parser.add_argument(*name_or_flags, **args)

        if subcommands:
            parser.add_subparsers(
                title="subcommands",
                metavar="SUBCOMMAND",
                required=True,
            )

        _cmdargparse_command_decorator = (
            cmd2.with_argparser(
                parser,
                ns_provider=cls.namespace_provider(argtype),
            )
            if subcommand_to is None
            else cls.subcommand_decorator(parser, subcommand_to)
        )

        return _cmdargparse_command_decorator  # type: ignore

    # ################## HELPERS ###########################

    @staticmethod
    def subcommand_decorator(
        parser: ArgumentParser,
        subcommand_to: Tuple[str, str] | str,
        /,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def _decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            if isinstance(subcommand_to, tuple):
                (command, subcommand) = subcommand_to

            else:
                command = subcommand_to

                (_, _, subcommand) = func.__name__.rpartition("_")

            if func.__doc__:
                help = cmd2.utils.strip_doc_annotations(func.__doc__)
            else:
                help = None

            return cmd2.as_subcommand_to(
                command,
                subcommand,
                parser,
                help=help,
            )(func)

        return _decorator

    @staticmethod
    def namespace_provider(
        argtype: Type[TARGUMENT],
        /,
    ) -> Callable[
        [cmd2.Cmd | cmd2.CommandSet],
        argparse.Namespace,
    ]:
        # Inherit all attributes that are assumed to be constants.
        # (This includes all uppercase attributes not starting with an '_'.)
        namespace = {
            attr: getattr(argtype, attr)
            for attr in dir(argtype)
            if (
                not attr.startswith("_")
                and attr.isupper()
                # <format-break>
            )
        }

        def _provider(cmd: cmd2.Cmd | cmd2.CommandSet) -> Namespace:
            return Namespace(**namespace)

        return _provider


# ################################ CLASS #######################################


class cmdcommand(metaclass=_cmdcommand):

    pass


# ################################ HELPERS #####################################


def argparse_name_or_flags(
    field: str,
    /,
    decls: _FieldDecls,
    *,
    default_form: _DeclFormSpecifier,
) -> Tuple[str, ...]:
    (decl, altdecl) = (decls.decl, decls.altdecl)

    form = decls.form or default_form
    more_decls = decls.more_decls or ()

    # In the augmented declaration specification format the automatically
    # derived declaration is replaced if it has the same form.
    if (decl is None and altdecl is not None) and (
        (form == "-" and not altdecl.startswith("--"))
        or (form == "--" and altdecl.startswith("--"))
    ):
        decl, altdecl = altdecl, None

    return tuple(
        _decl
        for _decl in (
            decl or (form + field.replace("_", "-")),
            altdecl,
            *more_decls,
        )
        if _decl is not None
    )


def argparse_type(type: Any, /) -> Tuple[Type[Any], str | None]:
    origin = typing.get_origin(type)
    if origin is None:
        return (type, None)

    if origin is typing.Annotated:
        (argtype, *_) = typing.get_args(type)
        return argparse_type(argtype)

    # We assume the first argument of the union type is the primary type that
    # should be passed to the `argparse` module.
    if isinstance(type, types.UnionType):
        (argtype, *_) = typing.get_args(type)
        return argparse_type(argtype)
    elif origin is typing.Union:
        (argtype, *_) = typing.get_args(type)
        return argparse_type(argtype)
    elif origin is list:
        (argtype, *_) = typing.get_args(type)
        return (argparse_type(argtype)[0], "*")

    raise TypeError("unsupported type annotation")
