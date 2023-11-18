#!/usr/bin/env python3

"""Update the family_word column in PaliWord with a new value."""

import re

from rich import print

from db.get_db_session import get_db_session
from db.models import PaliWord
from tools.paths import ProjectPaths
from tools.tic_toc import tic, toc


def main():
    tic()
    print("[bright_yellow]update word family")
    pth = ProjectPaths()
    db_session = get_db_session(pth.dpd_db_path)
    db = db_session.query(PaliWord).all()

    find: str = "cīvara"
    replace: str = "cīra"

    for i in db:
        if re.findall(fr"\b{find}\b", str(i.family_word)):
            print(f"[green]{i.pali_1}")
            print(f"[green]{i.family_word}")
            i.family_word = re.sub(
                fr"\b{find}\b", replace, str(i.family_word))
            print(f"[blue]{i.family_word}")
            print()

    db_session.commit()

    toc()


if __name__ == "__main__":
    main()