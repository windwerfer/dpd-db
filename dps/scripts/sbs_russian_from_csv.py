#!/usr/bin/env python3

"""Update the Russian and SBS from dps.ods. Clean Russian and SBS before importing.
Additionally check for duplicate ids."""

import sys
import csv

from rich import print
from typing import Dict, List
from sqlalchemy.orm import Session

from db.models import Russian, SBS, PaliWord
from db.get_db_session import get_db_session
from tools.paths import ProjectPaths as PTH
from dps.tools.paths_dps import DPSPaths as DPSPTH
from tools.tic_toc import tic, toc


def main():
    tic()
    print("[bright_yellow]add dps.csv to db")

    for p in [DPSPTH.dps_csv_path]:
        if not p.exists():
            print(f"[bright_red]File does not exist: {p}")
            sys.exit(1)

    db_session = get_db_session(PTH.dpd_db_path)

    db_session.execute(Russian.__table__.delete())
    db_session.execute(SBS.__table__.delete())
    add_dps_russian(db_session)
    add_dps_sbs(db_session)

    db_session.close()
    toc()


def add_dps_russian(db_session: Session):
    print("[green]processing dps russian")

    rows = []
    with open(DPSPTH.dps_csv_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            for key, value in row.items():
                row[key] = value.replace("<br/>", "\n")
            rows.append(row)

    items: List[Russian] = []
    unmatched_ids: List[str] = []  # Store unmatched IDs
    unique_ids = set()  # Use a set to keep track of unique ids in the CSV data
    duplicated_ids = set()  # Use a set to keep track of duplicated ids

    for r in rows:
        id_search = db_session.query(PaliWord.id).filter(
            PaliWord.user_id == r["id"]).first()

        if id_search is not None:
            id = id_search[0]

            # Check if the id is already in the set of unique ids
            if id in unique_ids:
                duplicated_ids.add(id)  # Add id to the set of duplicated ids
            else:
                # Add the id to the set of unique ids
                unique_ids.add(id)

            items += [_csv_row_to_russian(r, id, db_session)]

        else:
            unmatched_ids.append(r["id"])  # Add unmatched ID to the list

    # Print duplicated ids
    if duplicated_ids:
        print(f"[red]Duplicated IDs found in CSV: {duplicated_ids}")

    print("[green]adding russian to db")
    try:
        for i in items:
            db_session.add(i)

        db_session.commit()

    except Exception as e:
        print(f"[bright_red]ERROR: Adding to db failed:\n{e}")

        # Print unmatched IDs
    if unmatched_ids:
        print(f"[red]IDs not matching the database: {unmatched_ids}")


def _csv_row_to_russian(x: Dict[str, str], id, db_session) -> Russian:
    # Check if the id already exists in the 'russian' table
    existing_russian = db_session.query(Russian).filter_by(id=id).first()

    # If an existing record is found, update
    if existing_russian:
        existing_russian.ru_meaning = x['ru_meaning']
        existing_russian.ru_meaning_lit = x['ru_meaning_lit']
        existing_russian.ru_notes = x['ru_notes']
        return existing_russian
    else:
        # If the id doesn't exist in the table, create a new Russian object
        return Russian(
            id=id,
            ru_meaning=x['ru_meaning'],
            ru_meaning_lit=x['ru_meaning_lit'],
            ru_notes=x['ru_notes'],
        )


def add_dps_sbs(db_session: Session):
    print("[green]processing dps sbs")

    rows = []
    with open(DPSPTH.dps_csv_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            for key, value in row.items():
                row[key] = value.replace("<br/>", "\n")
            rows.append(row)

    items: List[SBS] = []
    unmatched_ids: List[str] = []  # Store unmatched IDs

    for r in rows:
        id_search = db_session.query(PaliWord.id).filter(
            PaliWord.user_id == r["id"]).first()

        if id_search is not None:
            id = id_search[0]
            items += [_csv_row_to_sbs(r, id, db_session)]
        else:
            unmatched_ids.append(r["id"])  # Add unmatched ID to the list

    print("[green]adding sbs to db")
    try:
        for i in items:
            db_session.add(i)

        db_session.commit()

    except Exception as e:
        print(f"[bright_red]ERROR: Adding to db failed:\n{e}")

        # Print unmatched IDs
    if unmatched_ids:
        print(f"[red]IDs not matching the database: {unmatched_ids}")


def _csv_row_to_sbs(x: Dict[str, str], id, db_session) -> SBS:

    return SBS(
        id=id,
        sbs_class_anki=x["sbs_class_anki"],
        sbs_class=x["sbs_class"],
        sbs_meaning=x["sbs_meaning"],
        sbs_notes=x["sbs_notes"],
        sbs_source_1=x["sbs_source_1"],
        sbs_sutta_1=x["sbs_sutta_1"],
        sbs_example_1=x["sbs_example_1"],
        sbs_chant_pali_1=x["sbs_chant_pali_1"],
        sbs_chant_eng_1=x["sbs_chant_eng_1"],
        sbs_chapter_1=x["sbs_chapter_1"],
        sbs_source_2=x["sbs_source_2"],
        sbs_sutta_2=x["sbs_sutta_2"],
        sbs_example_2=x["sbs_example_2"],
        sbs_chant_pali_2=x["sbs_chant_pali_2"],
        sbs_chant_eng_2=x["sbs_chant_eng_2"],
        sbs_chapter_2=x["sbs_chapter_2"],
        sbs_source_3=x["sbs_source_3"],
        sbs_sutta_3=x["sbs_sutta_3"],
        sbs_example_3=x["sbs_example_3"],
        sbs_chant_pali_3=x["sbs_chant_pali_3"],
        sbs_chant_eng_3=x["sbs_chant_eng_3"],
        sbs_chapter_3=x["sbs_chapter_3"],
        sbs_source_4=x["sbs_source_4"],
        sbs_sutta_4=x["sbs_sutta_4"],
        sbs_example_4=x["sbs_example_4"],
        sbs_chant_pali_4=x["sbs_chant_pali_4"],
        sbs_chant_eng_4=x["sbs_chant_eng_4"],
        sbs_chapter_4=x["sbs_chapter_4"],
        sbs_index=x["sbs_index"],
        sbs_category=x["sbs_category"],
        sbs_audio=x["sbs_audio"],
    )


if __name__ == "__main__":
    main()