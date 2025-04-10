# coding:utf-8

import os
from typing import List
from typing import Optional
from typing import Sequence

from xkits_command import ArgParser
from xkits_command import Command
from xkits_command import CommandArgument
from xkits_command import CommandExecutor

from xlc.attribute import __urlhome__
from xlc.attribute import __version__
from xlc.database.langtags import LangTag
from xlc.language.message import Message
from xlc.language.segment import Segment


@CommandArgument("xlc-generate", description="Generate xlc files")
def add_cmd(_arg: ArgParser):
    _arg.add_argument("--base", dest="directory", type=str, help="directory",
                      metavar="DIR", default="xlocale")
    _arg.add_argument(dest="languages", type=str, help="language", nargs="*",
                      metavar="LANG", default=["en", "zh-Hans", "zh-Hant"])


@CommandExecutor(add_cmd)
def run_cmd(cmds: Command) -> int:
    directory: str = cmds.args.directory
    languages: List[str] = cmds.args.languages
    os.makedirs(directory, exist_ok=True)
    message: Message = Message(directory)
    for language in languages:
        ltag: LangTag = message.languages.get(language)
        segment: Segment = message.load(ltag) or Segment.generate(ltag)
        filename: str = segment.lang.name + Message.SUFFIX
        segment.dumpf(os.path.join(directory, filename))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = Command()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, epilog=f"For more, please visit {__urlhome__}.")  # noqa:E501
