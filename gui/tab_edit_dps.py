"""Render tab to edit a Russian and SBS tables in the database."""

from functions_dps import load_sbs_index
from completion_combo import CompletionCombo

sbs_index = load_sbs_index()
pali_chant_list = [i.pali_chant for i in sbs_index]
pali_class_list = [str(i) for i in range(1, 99)]

dpd_background = "#1c1e23"
dpd_text = "#0a9ce4"
ru_background = "#32363f"
ru_text = "white"
sbs_background = "#272a31"
sbs_text = "white"
other_text = "#2bff00"


def make_tab_edit_dps(sg):

    dps_layout = [
        [
            sg.Text("", size=(15, 1)),
            sg.Input(
                "",
                key="dps_id_or_pali_1",
                size=(35, 1),
                enable_events=True,
                tooltip="enter id or pali_1"),
            sg.Button(
                "Get word from Db",
                key="dps_id_or_pali_1_button",
                tooltip="click to fetch word from db",
                font=(None, 13)),
            sg.Text("", size=(5, 1)),
        ],
        [
            sg.Text("id and pali_1", size=(15, 1)),
            sg.Input(
                key="dps_dpd_id", size=(7, 1),
                text_color=dpd_text,
                background_color=dpd_background),
            sg.Input(
                key="dps_pali_1", size=(43, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("grammar", size=(15, 1)),
            sg.Input(
                key="dps_grammar",
                size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("meaning", size=(15, 1)),
            sg.Multiline(
                key="dps_meaning",
                size=(50, 2),
                enable_events=True,
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("suggestion", size=(15, 1)),
            sg.Multiline(
                key="dps_ru_online_suggestion",
                size=(50, 2),
                enable_events=True,
                text_color=other_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("", size=(15, 1)),
            sg.Button("Google Translate", key="dps_google_translate_button", font=(None, 13)),
            sg.Button("OpenAI", key="dps_openai_translate_button", font=(None, 13)),
            sg.Button("copy", key="dps_copy_meaning_button", font=(None, 13)),
            sg.Text(
                "", key="dps_google_translate_error", size=(100, 1), text_color="red"),
            sg.Text(
                "", key="dps_openai_translate_error", size=(100, 3), text_color="red"),
        ],
        [
            sg.Text("russian", size=(15, 1)),
            sg.Multiline(
                key="dps_ru_meaning",
                size=(50, 2),
                enable_events=True,
                tooltip="type Russian meaning",
                text_color=ru_text,
                background_color=ru_background),
            sg.Text(
                "", key="dps_ru_meaning_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("ru_add_spelling", size=(15, 1)),
            sg.Input(
                key="dps_ru_add_spelling", size=(25, 1), enable_events=True,
                tooltip="Add a word to the user russian dictionary."),
            sg.Button("Add", key="dps_ru_add_spelling_button", font=(None, 13)),
            sg.Button("Edit", key="dps_ru_edit_spelling_button", font=(None, 13)),
            sg.Button("Check", key="dps_ru_check_spelling_button", font=(None, 13)),
            sg.Text(
                "", key="dps_ru_add_spelling_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("russian lit", size=(15, 1)),
            sg.Input(
                key="dps_ru_meaning_lit",
                size=(50, 1),
                enable_events=True,
                tooltip="type Russian literal meaning",
                text_color=ru_text,
                background_color=ru_background),
            sg.Text(
                "", key="dps_ru_meaning_lit_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs meaning", size=(15, 1)),
            sg.Multiline(
                key="dps_sbs_meaning",
                size=(50, 2),
                enable_events=True,
                tooltip="type Russian literal meaning",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_meaning_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("root", size=(15, 1)),
            sg.Input(
                key="dps_root",
                size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("base or comp", size=(15, 1)),
            sg.Input(
                key="dps_base_or_comp",
                size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("constr", size=(15, 1)),
            sg.Input(
                key="dps_constr_or_comp_constr",
                size=(50, 2),
                tooltip="",
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("synonym", size=(15, 1)),
            sg.Input(
                key="dps_synonym",
                size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("antonym", size=(15, 1)),
            sg.Input(
                key="dps_antonym",
                size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("notes", size=(15, 1)),
            sg.Multiline(
                key="dps_notes",
                size=(50, 3),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("russian note", size=(15, 1)),
            sg.Multiline(
                key="dps_ru_notes",
                size=(50, 2),
                enable_events=True,
                tooltip="",
                text_color=ru_text,
                background_color=ru_background),
            sg.Text(
                "", key="dps_ru_notes_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs note", size=(15, 1)),
            sg.Multiline(
                key="dps_sbs_notes",
                size=(50, 2),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_notes_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("dpd_source_1", size=(15, 1)),
            sg.Input(
                key="dps_source_1", size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("dpd_sutta_1", size=(15, 1)),
            sg.Input(
                key="dps_sutta_1", size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("dpd_example_1", size=(15, 5)),
            sg.Multiline(
                key="dps_example_1", size=(49, 5),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("ex_1 copy to", size=(15, 1)),
            sg.Button("sbs_ex_1", key="dps_copy_ex_1_to_1_button", font=(None, 13)),
            sg.Button("sbs_ex_2", key="dps_copy_ex_1_to_2_button", font=(None, 13)),
            sg.Button("sbs_ex_3", key="dps_copy_ex_1_to_3_button", font=(None, 13)),
            sg.Button("sbs_ex_4", key="dps_copy_ex_1_to_4_button", font=(None, 13)),
            sg.Text(
                "", key="dps_copy_ex_1_to_1_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_copy_ex_1_to_2_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_copy_ex_1_to_3_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_copy_ex_1_to_4_error", size=(50, 1), text_color="red"),
        ],
        [
            sg.Text("dpd_source_2", size=(15, 1)),
            sg.Input(
                key="dps_source_2", size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("dpd_sutta_2", size=(15, 1)),
            sg.Input(
                key="dps_sutta_2", size=(50, 1),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("dpd_example_2", size=(15, 5)),
            sg.Multiline(
                key="dps_example_2", size=(49, 5),
                text_color=dpd_text,
                background_color=dpd_background),
        ],
        [
            sg.Text("ex_2 copy to", size=(15, 1)),
            sg.Button("sbs_ex_1", key="dps_copy_ex_2_to_1_button", font=(None, 13)),
            sg.Button("sbs_ex_2", key="dps_copy_ex_2_to_2_button", font=(None, 13)),
            sg.Button("sbs_ex_3", key="dps_copy_ex_2_to_3_button", font=(None, 13)),
            sg.Button("sbs_ex_4", key="dps_copy_ex_2_to_4_button", font=(None, 13)),
            sg.Text(
                "", key="dps_copy_ex_2_to_1_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_copy_ex_2_to_2_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_copy_ex_2_to_3_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_copy_ex_2_to_4_error", size=(50, 1), text_color="red"),
        ],
        [
            sg.Text("sbs_source_1", size=(15, 1)),
            sg.Input(
                key="dps_sbs_source_1",
                size=(50, 1),
                enable_events=True,
                tooltip="Sutta code using DPR system",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_source_1_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_sutta_1", size=(15, 1)),
            sg.Input(
                key="dps_sbs_sutta_1",
                size=(50, 1),
                enable_events=True,
                tooltip="Sutta name",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_sutta_1_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_example_1", size=(15, 1)),
            sg.Multiline(
                key="dps_sbs_example_1",
                size=(50, 4),
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_example_1_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("", size=(15, 1)),
            sg.Input(
                key="dps_bold_1", size=(20, 1),
                tooltip="Bold the word"),
            sg.Button("Bold", key="dps_bold_1_button", font=(None, 13)),
            sg.Button(
                "Another Eg",
                key="dps_another_eg_1",
                tooltip="Find another sutta example",
                font=(None, 13)),
            sg.Button("Lower", key="dps_example_1_lower", font=(None, 13)),
            sg.Button("Clean", key="dps_example_1_clean", font=(None, 13)),
            sg.Text("", key="dps_bold_1_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("ex_1 swap with", size=(15, 1)),
            sg.Button("sbs_ex_2", key="dps_swap_ex_1_with_2_button", font=(None, 13)),
            sg.Button("sbs_ex_3", key="dps_swap_ex_1_with_3_button", font=(None, 13)),
            sg.Button("sbs_ex_4", key="dps_swap_ex_1_with_4_button", font=(None, 13)),
            sg.Button("clean ex 1", key="dps_remove_example_1_button", font=(None, 13)),
            sg.Text(
                "", key="dps_swap_ex_1_with_2_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_swap_ex_1_with_3_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_swap_ex_1_with_4_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_remove_example_1_error", size=(50, 1), text_color="red"),
        ],
        [
            sg.Text("sbs_chant_pali_1", size=(15, 1)),
            CompletionCombo(
                pali_chant_list,
                key="dps_sbs_chant_pali_1",
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_chant_pali_1_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_chant_eng_1", size=(15, 1)),
            sg.Input(
                key="dps_sbs_chant_eng_1",
                size=(50, 1),
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("sbs_chapter_1", size=(15, 1)),
            sg.Input(
                key="dps_sbs_chapter_1",
                size=(50, 1),
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background,
                tooltip=""),
        ],
        [
            sg.Text("sbs_source_2", size=(15, 1)),
            sg.Input(
                key="dps_sbs_source_2",
                size=(50, 1),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_source_2_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_sutta_2", size=(15, 1)),
            sg.Input(
                key="dps_sbs_sutta_2",
                size=(50, 1),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_sutta_2_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_example_2", size=(15, 1)),
            sg.Multiline(
                key="dps_sbs_example_2",
                size=(50, 4),
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_example_2_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("", size=(15, 1)),
            sg.Input(
                key="dps_bold_2", size=(20, 1),
                tooltip="Bold the word"),
            sg.Button("Bold", key="dps_bold_2_button", font=(None, 13)),
            sg.Button(
                "Another Eg",
                key="dps_another_eg_2",
                tooltip="Find another sutta example",
                font=(None, 13)),
            sg.Button("Lower", key="dps_example_2_lower", font=(None, 13)),
            sg.Button("Clean", key="dps_example_2_clean", font=(None, 13)),
            sg.Text("", key="dps_bold_2_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("ex_2 swap with", size=(15, 1)),
            sg.Button("sbs_ex_1", key="dps_swap_ex_2_with_1_button", font=(None, 13)),
            sg.Button("sbs_ex_3", key="dps_swap_ex_2_with_3_button", font=(None, 13)),
            sg.Button("sbs_ex_4", key="dps_swap_ex_2_with_4_button", font=(None, 13)),
            sg.Button("clean ex 2", key="dps_remove_example_2_button", font=(None, 13)),
            sg.Text(
                "", key="dps_swap_ex_2_with_1_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_swap_ex_2_with_3_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_swap_ex_2_with_4_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_remove_example_2_error", size=(50, 1), text_color="red"),
        ],
        [
            sg.Text("sbs_chant_pali_2", size=(15, 1)),
            CompletionCombo(
                pali_chant_list,
                key="dps_sbs_chant_pali_2",
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_chant_pali_2_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_chant_eng_2", size=(15, 1)),
            sg.Input(
                key="dps_sbs_chant_eng_2",
                size=(50, 1),
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("sbs_chapter_2", size=(15, 1)),
            sg.Input(
                key="dps_sbs_chapter_2",
                size=(50, 1),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("sbs_source_3", size=(15, 1)),
            sg.Input(
                key="dps_sbs_source_3",
                size=(50, 1),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_source_3_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_sutta_3", size=(15, 1)),
            sg.Input(
                key="dps_sbs_sutta_3",
                size=(50, 1),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_sutta_3_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_example_3", size=(15, 1)),
            sg.Multiline(
                key="dps_sbs_example_3",
                size=(50, 4),
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_example_3_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("", size=(15, 1)),
            sg.Input(
                key="dps_bold_3", size=(20, 1),
                tooltip="Bold the word"),
            sg.Button("Bold", key="dps_bold_3_button", font=(None, 13)),
            sg.Button(
                "Another Eg",
                key="dps_another_eg_3",
                tooltip="Find another sutta example",
                font=(None, 13)),
            sg.Button("Lower", key="dps_example_3_lower", font=(None, 13)),
            sg.Button("Clean", key="dps_example_3_clean", font=(None, 13)),
            sg.Text("", key="dps_bold_3_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("ex_3 swap with", size=(15, 1)),
            sg.Button("sbs_ex_1", key="dps_swap_ex_3_with_1_button", font=(None, 13)),
            sg.Button("sbs_ex_2", key="dps_swap_ex_3_with_2_button", font=(None, 13)),
            sg.Button("sbs_ex_4", key="dps_swap_ex_3_with_4_button", font=(None, 13)),
            sg.Button("clean ex 3", key="dps_remove_example_3_button", font=(None, 13)),
            sg.Text(
                "", key="dps_swap_ex_3_with_1_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_swap_ex_3_with_2_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_swap_ex_3_with_4_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_remove_example_3_error", size=(50, 1), text_color="red"),
        ],
        [
            sg.Text("sbs_chant_pali_3", size=(15, 1)),
            CompletionCombo(
                pali_chant_list,
                key="dps_sbs_chant_pali_3",
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_chant_pali_3_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_chant_eng_3", size=(15, 1)),
            sg.Input(
                key="dps_sbs_chant_eng_3",
                size=(50, 1),
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("sbs_chapter_3", size=(15, 1)),
            sg.Input(
                key="dps_sbs_chapter_3",
                size=(50, 1),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("sbs_source_4", size=(15, 1)),
            sg.Input(
                key="dps_sbs_source_4",
                size=(50, 1),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_source_4_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_sutta_4", size=(15, 1)),
            sg.Input(
                key="dps_sbs_sutta_4",
                size=(50, 1),
                enable_events=True,
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_sutta_4_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_example_4", size=(15, 1)),
            sg.Multiline(
                key="dps_sbs_example_4",
                size=(50, 4),
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_example_4_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("", size=(15, 1)),
            sg.Input(
                key="dps_bold_4", size=(20, 1),
                tooltip="Bold the word"),
            sg.Button("Bold", key="dps_bold_4_button", font=(None, 13)),
            sg.Button(
                "Another Eg",
                key="dps_another_eg_4",
                tooltip="Find another sutta example",
                font=(None, 13)),
            sg.Button("Lower", key="dps_example_4_lower", font=(None, 13)),
            sg.Button("Clean", key="dps_example_4_clean", font=(None, 13)),
            sg.Text("", key="dps_bold_4_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("ex_4 swap with", size=(15, 1)),
            sg.Button("sbs_ex_1", key="dps_swap_ex_4_with_1_button", font=(None, 13)),
            sg.Button("sbs_ex_2", key="dps_swap_ex_4_with_2_button", font=(None, 13)),
            sg.Button("sbs_ex_3", key="dps_swap_ex_4_with_3_button", font=(None, 13)),
            sg.Button("clean ex 4", key="dps_remove_example_4_button", font=(None, 13)),
            sg.Text(
                "", key="dps_swap_ex_4_with_1_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_swap_ex_4_with_2_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_swap_ex_4_with_3_error", size=(50, 1), text_color="red"),
            sg.Text(
                "", key="dps_remove_example_4_error", size=(50, 1), text_color="red"),
        ],
        [
            sg.Text("sbs_chant_pali_4", size=(15, 1)),
            CompletionCombo(
                pali_chant_list,
                key="dps_sbs_chant_pali_4",
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background),
            sg.Text(
                "", key="dps_sbs_chant_pali_4_error", size=(50, 1), text_color="red")
        ],
        [
            sg.Text("sbs_chant_eng_4", size=(15, 1)),
            sg.Input(
                key="dps_sbs_chant_eng_4",
                size=(50, 1),
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("sbs_chapter_4", size=(15, 1)),
            sg.Input(
                key="dps_sbs_chapter_4",
                size=(50, 1),
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background,
                tooltip=""),
        ],
        [
            sg.Text("class anki", size=(15, 1)),
            CompletionCombo(
                pali_class_list,
                key="dps_sbs_class_anki",
                default_value="",
                size=(3, 1),
                enable_events=True,
                text_color=sbs_text,
                background_color=sbs_background,
                tooltip=""),
        ],
        [
            sg.Text("sbs_audio", size=(15, 1)),
            sg.Input(
                key="dps_sbs_audio",
                size=(50, 1),
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("sbs_category", size=(15, 1)),
            sg.Input(
                key="dps_sbs_category",
                size=(50, 1),
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("sbs_index", size=(15, 1)),
            sg.Input(
                key="dps_sbs_index",
                size=(50, 1),
                tooltip="",
                text_color=sbs_text,
                background_color=sbs_background),
        ],
        [
            sg.Text("", size=(55, 1))
        ],
    ]

    tab_edit_dps = [
        [
            sg.Column(
                dps_layout,
                scrollable=True,
                vertical_scroll_only=True,
                expand_y=True,
                expand_x=True,
                size=(None, 850),
            ),
        ],
        [
            sg.HSep(),
        ],
        [
            sg.Button("Clear", key="dps_clear_button", 
                tooltip="Clear all the fields"),
            sg.Button("Reset", key="dps_reset_button",
                tooltip="Reset all fields as they was before editing"),
            sg.Button("Update DB", key="dps_update_db_button",
                tooltip="Add a sbs or ru info into the db"),
            sg.Button("Summary", key="dps_summary_button", 
                tooltip="See a summary of filled fields"),
        ],
    ]

    return tab_edit_dps
