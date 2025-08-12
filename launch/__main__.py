from typing import Literal, Optional

import cmd2

from cmdargparse import cmdargument, cmdcommand, cmdfield


class MyApplication(cmd2.Cmd):
    # Use CTRL-Z to exit the application.

    # ################## ARGUMENT ##########################

    @cmdargument
    class _ArgumentCommandArgs(cmdargument):

        arg: str | None = cmdfield.argument(
            ("alpha", "beta"),
            {
                "a": "alpha",
                "b": "beta",
            },
            default=None,
        )

    @cmdcommand(_ArgumentCommandArgs)
    def do_arg(self, args: _ArgumentCommandArgs) -> Optional[bool]:
        args.pfields(self)

    # ################## OPTION ############################

    @cmdargument
    class _OptionCommandArgs(cmdargument):

        xx: str | None = cmdfield.option()
        yy: int | None = cmdfield.option([1, 2, 3])
        zz: str = cmdfield.option(required=True)

        aa: str | None = cmdfield.option()  # -aa  OR  --aa
        bb: str | None = cmdfield.option("--cc")  # -bb, --cc  OR  --cc
        dd: str | None = cmdfield.option("-ee")  # -ee  OR  --dd, -ee
        ff: str | None = cmdfield.option("--gg", "-ii")  # --gg, -ii
        jj: str | None = cmdfield.option(form="--")  # --jj
        kk: str | None = cmdfield.option(form="-")  # -kk
        mm: str | None = cmdfield.option(decls="--mm")  # --mm
        nn: str | None = cmdfield.option(decls="-oo")  # -oo
        pp: str | None = cmdfield.option(decls=("--rr", "-ss"))  # --rr, -ss
        tt: str | None = cmdfield.option(more_decls="-uu")  # -tt, -uu

    @cmdcommand(_OptionCommandArgs)
    def do_opt(self, args: _OptionCommandArgs) -> Optional[bool]:
        args.pfields(self)

    # ################## FLAG ##############################

    @cmdargument
    class _FlagCommandArgs(cmdargument):

        vv: bool = cmdfield.flag()
        ww: bool = cmdfield.flag(invert=True)
        xx: float | None = cmdfield.flag(const=1.23)
        yy: str | None = cmdfield.flag(const="text")
        zz: Literal["ltr"] | None = cmdfield.flag(const="ltr")

        aa: bool = cmdfield.flag()  # -aa  OR  --aa
        bb: bool = cmdfield.flag("--cc")  # -bb, --cc  OR  --cc
        dd: bool = cmdfield.flag("-ee")  # -ee  OR  --dd, -ee
        ff: bool = cmdfield.flag("--gg", "-ii")  # --gg, -ii
        jj: bool = cmdfield.flag(form="--")  # --jj
        kk: bool = cmdfield.flag(form="-")  # -kk
        mm: bool = cmdfield.flag(decls="--mm")  # --mm
        nn: bool = cmdfield.flag(decls="-oo")  # -oo
        pp: bool = cmdfield.flag(decls=("--rr", "-ss"))  # --rr, -ss
        tt: bool = cmdfield.flag(more_decls="-uu")  # -tt, -uu

    @cmdcommand(_FlagCommandArgs)
    def do_flag(self, args: _FlagCommandArgs) -> Optional[bool]:
        args.pfields(self)


MyApplication().cmdloop()
