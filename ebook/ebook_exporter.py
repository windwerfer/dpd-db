#!/usr/bin/env python3

import csv
import os
import shutil
import subprocess

from datetime import datetime
from mako.template import Template
from rich import print
from zipfile import ZipFile, ZIP_DEFLATED

from db.get_db_session import get_db_session
from db.models import PaliWord, Sandhi
from db.models import DerivedData

from tools.cst_sc_text_sets import make_cst_text_set
from tools.cst_sc_text_sets import make_sc_text_set
from tools.diacritics_cleaner import diacritics_cleaner
from tools.first_letter import find_first_letter
from tools.meaning_construction import make_meaning_html
from tools.meaning_construction import summarize_constr
from tools.meaning_construction import degree_of_completion
from tools.pali_alphabet import pali_alphabet
from tools.pali_sort_key import pali_sort_key
from tools.paths import ProjectPaths as PTH
from tools.sandhi_words import make_words_in_sandhi_set
from tools.tic_toc import tic, toc


ebook_entry_templ = Template(
    filename=str(PTH.ebook_entry_templ_path))
ebook_sandhi_templ = Template(
    filename=str(PTH.ebook_sandhi_templ_path))
ebook_letter_tmpl = Template(
    filename=str(PTH.ebook_letter_templ_path))
ebook_grammar_templ = Template(
    filename=str(PTH.ebook_grammar_templ_path))
ebook_example_templ = Template(
    filename=str(PTH.ebook_example_templ_path))
ebook_abbreviation_entry_templ = Template(
    filename=str(PTH.ebook_abbrev_entry_templ_path))
ebook_title_page_templ = Template(
    filename=str(PTH.ebook_title_page_templ_path))
ebook_content_opf_templ = Template(
    filename=str(PTH.ebook_content_opf_templ_path)
)


def render_xhtml():
    print("[bright_yellow]rendering dpd for ebook")

    print(f"[green]{'querying dpd db':<40}", end="")
    db_sesssion = get_db_session("dpd.db")
    dpd_db = db_sesssion.query(PaliWord).all()
    dpd_db = sorted(dpd_db, key=lambda x: pali_sort_key(x.pali_1))
    print(f"{len(dpd_db):>10,}")

    # limit the extent of the dictionary to an ebt text set
    ebt_books = [
        "vin1", "vin2", "vin3", "vin4",
        "dn1", "dn2", "dn3",
        "mn1", "mn2", "mn3",
        "sn1", "sn2", "sn3", "sn4", "sn5",
        "an1", "an2", "an3", "an4", "an5",
        "an6", "an7", "an8", "an9", "an10", "an11",
        "kn1", "kn2", "kn3", "kn4", "kn5",
        "kn8", "kn9",
        ]

    # all words in cst and sc texts
    print(f"[green]{'making cst text set':<40}", end="")
    cst_text_set = make_cst_text_set(ebt_books)
    print(f"{len(cst_text_set):>10,}")

    print(f"[green]{'making sc text set':<40}", end="")
    sc_text_set = make_sc_text_set(ebt_books)
    print(f"{len(sc_text_set):>10,}")
    combined_text_set = cst_text_set | sc_text_set

    # words in sandhi compounds in cst_text_set & sc_text_set
    print(f"[green]{'querying sandhi db':<40}", end="")
    sandhi_db = db_sesssion.query(Sandhi).filter(
        Sandhi.sandhi.in_(combined_text_set)).all()
    words_in_sandhi_set = make_words_in_sandhi_set(sandhi_db)
    print(f"{len(words_in_sandhi_set):>10,}")

    # all_words_set = cst_text_set + sc_text_set + words in sandhi compounds
    all_words_set = combined_text_set | words_in_sandhi_set
    print(f"[green]{'all_words_set':<40}{len(all_words_set):>10,}")

    # only include inflections which exist in all_words_set
    print(f"[green]{'creating inflections dict':<40}", end="")
    dd_db = db_sesssion.query(DerivedData).all()
    dd_dict = {}
    dd_counter = 0

    for i in dd_db:
        inflection_set = set(i.inflections_list) & all_words_set
        dd_dict[i.id] = inflection_set
        dd_counter += len(inflection_set)
    print(f"{dd_counter:>10,}")

    # add one clean inflection without diacritics
    for i in dpd_db:
        no_diacritics = diacritics_cleaner(i.pali_clean)
        dd_dict[i.id].add(no_diacritics)

    # a dicitonary for entries of each letter of the alphabet
    print(f"[green]{'initialising letter dict':<40}")
    letter_dict: dict = {}
    for letter in pali_alphabet:
        letter_dict[letter] = []

    # add all words
    print("[green]creating entries")
    excluded = []
    id_counter = 1
    for counter, i in enumerate(dpd_db):
        inflections: set = dd_dict[i.id]
        first_letter = find_first_letter(i.pali_1)
        entry = render_ebook_entry(id_counter, i, inflections)
        letter_dict[first_letter] += [entry]
        id_counter += 1

        if counter % 5000 == 0:
            print(f"{counter:>10,} / {len(dpd_db):<10,} {i.pali_1}")

    # add sandhi words which are in all_words_set
    print("[green]add sandhi words")
    for counter, i in enumerate(sandhi_db):
        if bool(set(i.sandhi) & all_words_set):
            first_letter = find_first_letter(i.sandhi)
            entry = render_sandhi_entry(id_counter, i)
            letter_dict[first_letter] += [entry]
            id_counter += 1

        if counter % 5000 == 0:
            print(f"{counter:>10,} / {len(sandhi_db):<10,} {i.sandhi}")

    # save to a single file for each letter of the alphabet
    print(f"[green]{'saving entries xhtml':<40}", end="")
    total = 0

    for counter, (letter, entries) in enumerate(letter_dict.items()):
        ascii_letter = diacritics_cleaner(letter)
        total += len(entries)
        entries = "".join(entries)
        xhtml = render_ebook_letter_tmpl(letter, entries)
        output_path = PTH.epub_text_dir.joinpath(
            f"{counter}_{ascii_letter}.xhtml")

        with open(output_path, "w") as f:
            f.write(xhtml)

    print(f"{total:>10,}")

    return id_counter+1

# -----------------------------------------------------------------------------------------
# functions to create the various templates


def render_ebook_entry(counter: int, i: PaliWord, inflections: set) -> str:
    """Render single word entry."""

    summary = f"{i.pos}. "
    if i.plus_case:
        summary += f"({i.plus_case}) "
    summary += make_meaning_html(i)

    construction = summarize_constr(i)
    if construction:
        summary += f" [{construction}]"

    summary += f" {degree_of_completion(i)}"

    if "&" in summary:
        summary = summary.replace("&", "and")

    grammar_table = render_grammar_templ(i)
    if "&" in grammar_table:
        grammar_table = grammar_table.replace("&", "and")

    examples = render_example_templ(i)

    return str(ebook_entry_templ.render(
            counter=counter,
            pali_1=i.pali_1,
            pali_clean=i.pali_clean,
            inflections=inflections,
            summary=summary,
            grammar_table=grammar_table,
            examples=examples))


def render_grammar_templ(i: PaliWord) -> str:
    """html table of grammatical information"""

    if i.meaning_1 != "":
        i.construction = i.construction.replace("\n", "<br/>")
        i.phonetic = i.phonetic.replace("\n", "<br/>")

        grammar = i.grammar
        if i.neg != "":
            grammar += f", {i.neg}"
        if i.verb != "":
            grammar += f", {i.verb}"
        if i.trans != "":
            grammar += f", {i.trans}"
        if i.plus_case != "":
            grammar += f" ({i.plus_case})"

        meaning = f"{make_meaning_html(i)}"

        return str(
            ebook_grammar_templ.render(
                i=i,
                grammar=grammar,
                meaning=meaning,))

    else:
        return ""


def render_example_templ(i: PaliWord) -> str:
    """render sutta examples html"""
    i.example_1 = i.example_1.replace("\n", "<br/>")
    i.example_2 = i.example_2.replace("\n", "<br/>")
    i.sutta_1 = i.sutta_1.replace("\n", "<br/>")
    i.sutta_2 = i.sutta_2.replace("\n", "<br/>")

    if i.meaning_1 and i.example_1:
        return str(
            ebook_example_templ.render(
                i=i))
    else:
        return ""


def render_sandhi_entry(counter: int, i: Sandhi) -> str:
    """Render sandhi word entry."""

    sandhi = i.sandhi
    splits = "<br/>".join(i.split_list)

    return str(ebook_sandhi_templ.render(
            counter=counter,
            sandhi=sandhi,
            splits=splits))


def render_ebook_letter_tmpl(letter: str, entries: str) -> str:
    """Render all entries for a single letter."""
    return str(
        ebook_letter_tmpl.render(
            letter=letter,
            entries=entries))


def save_abbreviations_xhtml_page(id_counter):
    """Render xhtml of all DPD abbreviaitons and save as a page."""
    print(f"[green]{'saving abbrev xhtml':<40}", end="")
    abbreviations_list = []

    with open(
        PTH.abbreviations_tsv_path, "r",
            newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            abbreviations_list.append(row)

    abbreviation_entries = []
    for i in abbreviations_list:
        abbreviation_entries += [
            render_abbreviation_entry(id_counter, i)]
        id_counter += 1

    entries = "".join(abbreviation_entries)
    entries = entries.replace(" > ", " &gt; ")
    xhtml = render_ebook_letter_tmpl("Abbreviations", entries)

    with open(PTH.epub_abbreviations_path, "w") as f:
        f.write(xhtml)

    print(f"{len(abbreviations_list):>10,}")


def render_abbreviation_entry(counter: int, i: dict) -> str:
    """Render a single abbreviations entry."""

    return str(ebook_abbreviation_entry_templ.render(
            counter=counter,
            i=i))


def save_title_page_xhtml():
    """Save date and time in title page xhtml."""
    print(f"[green]{'saving titlepage xhtml':<40}", end="")
    current_datetime = datetime.now()
    date = current_datetime.strftime("%Y-%m-%d")
    time = current_datetime.strftime("%H:%M")

    xhtml = str(ebook_title_page_templ.render(
            date=date,
            time=time))

    with open(PTH.epub_titlepage_path, "w") as f:
        f.write(xhtml)

    print(f"{'OK':>10}")

    save_content_opf_xhtml(current_datetime)


def save_content_opf_xhtml(current_datetime):
    """Save date and time in content.opf."""
    print(f"[green]{'saving content.opf':<40}", end="")

    date_time_zulu = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    content = str(ebook_content_opf_templ.render(
            date_time_zulu=date_time_zulu))

    with open(PTH.epub_content_opf_path, "w") as f:
        f.write(content)

    print(f"{'OK':>10}")


def zip_epub():
    """Zip up the epub dir and name it dpd-kindle.epub."""
    print("[green]zipping up epub")
    with ZipFile(PTH.dpd_epub_path, "w", ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(PTH.epub_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, PTH.epub_dir))


def make_mobi():
    """Run kindlegen to convert epub to mobi."""
    print("[green]converting epub to mobi")

    process = subprocess.Popen(
        [str(PTH.kindlegen_path), str(PTH.dpd_epub_path)],
        stdout=subprocess.PIPE, text=True)

    for line in process.stdout:
        print(line, end='')
    process.wait()


def copy_mobi():
    """Copy the mobi to the exporter/share dir."""
    print("[green]copying mobi to exporter/share")
    shutil.copy2(PTH.dpd_mobi_path, PTH.dpd_kindle_path)


if __name__ == "__main__":
    tic()
    id_counter = render_xhtml()
    save_abbreviations_xhtml_page(id_counter)
    save_title_page_xhtml()
    zip_epub()
    make_mobi()
    copy_mobi()
    toc()