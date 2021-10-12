from math import ceil
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from datetime import datetime

from tkinter.messagebox import showinfo
from tkinter.font import Font

from os import path
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
else:
    print('running in a normal Python process')


# ----------------------------------------------- GLOBAL VARIABLES


REF_FILE_NAME = ""
TEST_FILE_NAME = ""
MAIN_FILE_NAME = ""

INSERTIONS = []
DELETIONS = []  # 69 70 144

THRESHOLD = 1
LVL_SEL = 1

PEP_COLUMNS = ["peptide", "Peptide", "Peptide sequence"]
START_COLUMNS = ["start", "Start", "Peptide start"]

REF_PEPTIDE_MAX_LENGTH = 50  # 9
TEST_PEPTIDE_MAX_LENGTH = 50  # 9
MAIN_PEPTIDE_MAX_LENGTH = 50  # 36


# ----------------------------------------------- CLASSES


class MainApplication:

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=550, height=690)  # width=450, height=500)
        # to make a frame
        self.frame = tk.Frame(master, bg='white')

        ############################################################################################
        # Frame Input
        # this frame is placed in the original frame

        title_font = Font(family="Calibri", size=12, weight="bold")

        self.frame_input = tk.Frame(self.frame, bd='10', padx=3, pady=3)
        self.label_input_files = tk.Label(self.frame_input, text='Input File Paths', bd='3', fg='blue', font=title_font)
        self.label_ref = tk.Label(self.frame_input, text='Ref', bd='3')
        self.label_test = tk.Label(self.frame_input, text='Test', bd='3')
        self.label_main = tk.Label(self.frame_input, text='Main', bd='3')

        self.entry_ref = tk.Entry(self.frame_input, bd='3', justify="center")
        self.entry_test = tk.Entry(self.frame_input, bd='3', justify="center")
        self.entry_main = tk.Entry(self.frame_input, bd='3', justify="center")

        self.button_ref = tk.Button(self.frame_input, text='Browse', command=self.browse_ref)
        self.button_test = tk.Button(self.frame_input, text='Browse', command=self.browse_test)
        self.button_main = tk.Button(self.frame_input, text='Browse', command=self.browse_main)

        self.label_indels_title = tk.Label(self.frame_input, text='Insertions and Deletions', bd='3', fg='blue',
                                           font=title_font)

        self.label_insertions = tk.Label(self.frame_input, text='Insertions', bd='3')
        self.entry_insertions = tk.Entry(self.frame_input, bd='3', justify="center")

        self.label_deletions = tk.Label(self.frame_input, text='Deletions', bd='3')
        self.entry_deletions = tk.Entry(self.frame_input, bd='3', justify="center")

        self.label_indels_helper = tk.Label(self.frame_input,
                                            text='Input should contain numbers with spaces between, eg. 69 70 144',
                                            bd='3', fg='red')

        self.label_indels_or = tk.Label(self.frame_input, text='Or run an insertions and deletions search', bd='3',
                                        fg='blue')

        self.label_indels_alignment = tk.Label(self.frame_input, text='Alignment File', bd='3')
        self.entry_indels_alignment = tk.Entry(self.frame_input, bd='3', justify="center")
        self.button_indels_alignment = tk.Button(self.frame_input, text='Browse', command=self.browse_alignment)

        self.label_threshold_title = tk.Label(self.frame_input, text='Minimum Peptide Length', bd='3', fg='blue',
                                              font=title_font)
        self.entry_threshold = tk.Entry(self.frame_input, bd='3', justify="center")
        self.label_threshold_helper = tk.Label(self.frame_input,
                                               text='Default minimum peptide length is 1',
                                               bd='3', fg='red')

        self.label_radio_title = tk.Label(self.frame_input, text='Level Selection to Run', bd='3', fg='blue',
                                          font=title_font)

        self.frame_radio_buttons = tk.Frame(self.frame_input, bd='0', padx=3, pady=3)
        self.level_selection = IntVar()
        self.level_selection.set(1)
        self.radio_both_lvls = Radiobutton(self.frame_radio_buttons, text="Level 1 and 2",
                                           variable=self.level_selection, value=1).grid(row=0, column=1, padx=50)
        self.radio_lvl_one_only = Radiobutton(self.frame_radio_buttons, text="Level 1 only",
                                              variable=self.level_selection, value=2).grid(row=0, column=2)
        self.radio_lvl_two_only = Radiobutton(self.frame_radio_buttons, text="Level 2 only",
                                              variable=self.level_selection, value=3).grid(row=0, column=3, padx=50)

        self.label_result_file_title = tk.Label(self.frame_input, text='Results File', bd='3', fg='blue',
                                                font=title_font)
        self.entry_result_file = tk.Entry(self.frame_input, bd='3', justify="center")
        self.button_result_path = tk.Button(self.frame_input, text='Browse', command=self.browse_result_path)

        # place used to place the widgets in the frame
        self.label_input_files.place(relx=0.009, rely=-0.01, relheight=0.05)

        self.label_ref.place(relx=0.05, rely=0.06, relheight=0.035)
        self.entry_ref.place(relx=0.20, rely=0.06, relwidth=0.55, relheight=0.035)
        self.button_ref.place(relx=0.80, rely=0.06, relheight=0.030)

        self.label_test.place(relx=0.05, rely=0.14, relheight=0.035)
        self.entry_test.place(relx=0.20, rely=0.14, relwidth=0.55, relheight=0.035)
        self.button_test.place(relx=0.80, rely=0.14, relheight=0.030)

        self.label_main.place(relx=0.05, rely=0.22, relheight=0.035)
        self.entry_main.place(relx=0.20, rely=0.22, relwidth=0.55, relheight=0.035)
        self.button_main.place(relx=0.80, rely=0.22, relheight=0.030)

        self.label_indels_title.place(relx=0.009, rely=0.28, relheight=0.05)

        self.label_insertions.place(relx=0.03, rely=0.34, relheight=0.035)
        self.entry_insertions.place(relx=0.20, rely=0.34, relwidth=0.55, relheight=0.035)

        self.label_deletions.place(relx=0.03, rely=0.40, relheight=0.035)
        self.entry_deletions.place(relx=0.20, rely=0.40, relwidth=0.55, relheight=0.035)

        self.label_indels_helper.place(relx=0.07, rely=0.44, relheight=0.035)

        self.label_indels_or.place(relx=0.20, rely=0.50, relheight=0.035)

        self.label_indels_alignment.place(relx=0.0, rely=0.56, relheight=0.035)
        self.entry_indels_alignment.place(relx=0.20, rely=0.56, relwidth=0.55, relheight=0.035)
        self.button_indels_alignment.place(relx=0.80, rely=0.56, relheight=0.030)

        self.label_threshold_title.place(relx=0.009, rely=0.62, relheight=0.035)
        self.entry_threshold.place(relx=0.10, rely=0.68, relwidth=0.05, relheight=0.035)
        self.label_threshold_helper.place(relx=0.175, rely=0.68, relheight=0.035)

        self.label_radio_title.place(relx=0.009, rely=0.74, relheight=0.035)
        #  Radio buttons are placed in their own frame (self.frame_radio_buttons)

        self.label_result_file_title.place(relx=0.009, rely=0.90, relheight=0.035)
        self.entry_result_file.place(relx=0.20, rely=0.955, relwidth=0.55, relheight=0.035)
        self.button_result_path.place(relx=0.80, rely=0.955, relheight=0.030)

        ############################################################################################
        # placing the buttons below
        self.frame_button = tk.Frame(self.frame, bd='3', padx=3, pady=3)
        self.button_start = tk.Button(self.frame_button, text='Compare', command=self.start_clicked)
        self.button_cancel = tk.Button(self.frame_button, text='Cancel', command=master.destroy)

        self.button_cancel.place(relx=0.6, rely=0.22, relheight=0.6, relwidth=0.18)
        self.button_start.place(relx=0.8, rely=0.22, relheight=0.6, relwidth=0.18)

        ###############################################################################################
        # all the frames are placed in their respective positions

        self.frame_input.place(relx=0.005, rely=0.005, relwidth=0.99, relheight=0.906)
        self.frame_radio_buttons.place(relx=0.005, rely=0.815, relwidth=1, relheight=1)
        self.frame_button.place(relx=0.005, rely=0.915, relwidth=0.99, relheight=0.08)

        self.frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        self.canvas.pack()
        ##############################################################################################

    def start_clicked(self):
        print("Compare Start")
        init_objects(self.level_selection.get())

        print("Reading Ref file")
        ref_raw = init_ref_raw(self.entry_ref.get().strip())
        if ref_raw is None:
            print("Unable to read ref file")
            return
        print("Reading Test file")
        test_raw = init_test_raw(self.entry_test.get().strip())
        if test_raw is None:
            print("Unable to read test file")
            return
        print("Reading main file")
        main_raw = init_main_raw(self.entry_main.get().strip())
        if main_raw is None:
            print("Unable to read main file")
            return

        if self.entry_indels_alignment.get().strip() != "":
            print("Reading alignment file")
            if not init_alignment(self.entry_indels_alignment.get().strip()):
                print("Unable to create insertion and deletion lists")
                return
        else:
            if not init_insertions(self.entry_insertions.get().strip()):
                print("Insertion input error")
                return
            if not init_deletions(self.entry_deletions.get().strip()):
                print("Deletion input error")
                return

        if not init_threshold(self.entry_threshold.get().strip()):
            print("Minimum peptide length input error: minimum length set to 1")

        result_file = generate_result_file(self.entry_result_file.get())

        main_dictionary = create_main_comparison_dict(main_raw.to_dict('split'))
        ref_dictionary = create_test_comparison_dict(ref_raw.to_dict('split'), REF_FILE_NAME)
        test_dictionary = create_test_comparison_dict(test_raw.to_dict('split'), TEST_FILE_NAME)

        generate_test_comparison_results(ref_dictionary, test_dictionary)

        generate_main_comparison_results(L1_matched_dict, main_dictionary, "L1m")
        generate_main_comparison_results(L1_partial_dict, main_dictionary, "L1p")
        generate_main_comparison_results(L1_novel_dict, main_dictionary, "L1n")

        L1m_df = create_match_df(L1_matched)
        L1p_df = create_partial_df(L1_partial)
        L1n_df = create_novel_df(L1_novel)

        L1m_L2m_df = create_match_df(L1_matched_L2_matched)
        L1m_L2p_df = create_partial_df(L1_matched_L2_partial)
        L1m_L2n_df = create_novel_df(L1_matched_L2_novel)

        L1p_L2m_df = create_match_df(L1_partial_L2_matched)
        L1p_L2p_df = create_partial_df(L1_partial_L2_partial)
        L1p_L2n_df = create_novel_df(L1_partial_L2_novel)

        L1n_L2m_df = create_match_df(L1_novel_L2_matched)
        L1n_L2p_df = create_partial_df(L1_novel_L2_partial)
        L1n_L2n_df = create_novel_df(L1_novel_L2_novel)

        L1m_df.to_excel(result_file, sheet_name="L1M", index=False)
        L1p_df.to_excel(result_file, sheet_name="L1P", index=False)
        L1n_df.to_excel(result_file, sheet_name="L1N", index=False)

        L1m_L2m_df.to_excel(result_file, sheet_name="L1M_L2M", index=False)
        L1m_L2p_df.to_excel(result_file, sheet_name="L1M_L2P", index=False)
        L1m_L2n_df.to_excel(result_file, sheet_name="L1M_L2N", index=False)

        L1p_L2m_df.to_excel(result_file, sheet_name="L1P_L2M", index=False)
        L1p_L2p_df.to_excel(result_file, sheet_name="L1P_L2P", index=False)
        L1p_L2n_df.to_excel(result_file, sheet_name="L1P_L2N", index=False)

        L1n_L2m_df.to_excel(result_file, sheet_name="L1N_L2M", index=False)
        L1n_L2p_df.to_excel(result_file, sheet_name="L1N_L2P", index=False)
        L1n_L2n_df.to_excel(result_file, sheet_name="L1N_L2N", index=False)

        result_file.save()

        print("Compared")
        showinfo("CAVES", "Comparison Complete!")

    def browse_ref(self):
        filename = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv")])
        self.entry_ref.delete(0, tk.END)
        self.entry_ref.insert(0, filename)

    def browse_test(self):
        filename = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv")])
        self.entry_test.delete(0, tk.END)
        self.entry_test.insert(0, filename)

    def browse_main(self):
        filename = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv")])
        self.entry_main.delete(0, tk.END)
        self.entry_main.insert(0, filename)

    def browse_alignment(self):
        fasta_exts = [("FASTA files", "*.fasta"), ("FASTA files", "*.fna"), ("FASTA files", "*.ffn"),
                      ("FASTA files", "*.faa"), ("FASTA files", "*.frn"), ("FASTA files", "*.fa"),
                      ("FASTA files", "*.fsa")]
        filename = filedialog.askopenfilename(title="Select a File", filetypes=fasta_exts)
        self.entry_indels_alignment.delete(0, tk.END)
        self.entry_indels_alignment.insert(0, filename)

    def browse_result_path(self):
        time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = filedialog.asksaveasfilename(initialfile="results_"+time, title="Results File",
                                                filetypes=[("Excel files", "*.xlsx")])
        self.entry_result_file.delete(0, tk.END)
        self.entry_result_file.insert(0, filename)


class ResultSheetObject:
    def __init__(self):
        self.origin_file_one = []
        self.peptide_one = []
        self.start_one = []
        self.end_one = []
        self.length_one = []
        self.letters_matched = []
        self.letters_matched_length = []
        self.origin_file_two = []
        self.peptide_two = []
        self.start_two = []
        self.end_two = []
        self.length_two = []


class PeptideObject:
    def __init__(self, new_file, new_pep, new_start, new_end, new_length, new_suffix):
        self.origin_file = new_file
        self.peptide = new_pep
        self.start = new_start
        self.end = new_end
        self.length = new_length
        self.suffix = new_suffix


# ----------------------------------------------- RESULT OBJECTS


L1_novel = ResultSheetObject()
L1_partial = ResultSheetObject()
L1_matched = ResultSheetObject()

L2_novel = ResultSheetObject()
L2_partial = ResultSheetObject()
L2_matched = ResultSheetObject()

L1_novel_L2_novel = ResultSheetObject()
L1_novel_L2_partial = ResultSheetObject()
L1_novel_L2_matched = ResultSheetObject()

L1_partial_L2_novel = ResultSheetObject()
L1_partial_L2_partial = ResultSheetObject()
L1_partial_L2_matched = ResultSheetObject()

L1_matched_L2_novel = ResultSheetObject()
L1_matched_L2_partial = ResultSheetObject()
L1_matched_L2_matched = ResultSheetObject()


# ----------------------------------------------- LEVEL 1 DICTIONARIES


L1_novel_dict = {}
L1_partial_dict = {}
L1_matched_dict = {}


# ----------------------------------------------- FUNCTIONS


def init_objects(lvl_sel):
    global INSERTIONS
    INSERTIONS = []

    global DELETIONS
    DELETIONS = []

    global LVL_SEL
    LVL_SEL = lvl_sel

    if lvl_sel == 1 or lvl_sel == 2:
        global L1_novel
        L1_novel = ResultSheetObject()
        global L1_partial
        L1_partial = ResultSheetObject()
        global L1_matched
        L1_matched = ResultSheetObject()

    if lvl_sel == 3:
        global L2_novel
        L2_novel = ResultSheetObject()
        global L2_partial
        L2_partial = ResultSheetObject()
        global L2_matched
        L2_matched = ResultSheetObject()

    if lvl_sel == 1:
        global L1_novel_L2_novel
        L1_novel_L2_novel = ResultSheetObject()
        global L1_novel_L2_partial
        L1_novel_L2_partial = ResultSheetObject()
        global L1_novel_L2_matched
        L1_novel_L2_matched = ResultSheetObject()

        global L1_partial_L2_novel
        L1_partial_L2_novel = ResultSheetObject()
        global L1_partial_L2_partial
        L1_partial_L2_partial = ResultSheetObject()
        global L1_partial_L2_matched
        L1_partial_L2_matched = ResultSheetObject()

        global L1_matched_L2_novel
        L1_matched_L2_novel = ResultSheetObject()
        global L1_matched_L2_partial
        L1_matched_L2_partial = ResultSheetObject()
        global L1_matched_L2_matched
        L1_matched_L2_matched = ResultSheetObject()

        global L1_novel_dict
        L1_novel_dict = {}
        global L1_partial_dict
        L1_partial_dict = {}
        global L1_matched_dict
        L1_matched_dict = {}


def init_ref_raw(file_path):
    if not path.exists(file_path):
        print("Unable to find ref file: " + file_path)
        return None

    global REF_FILE_NAME
    REF_FILE_NAME = file_path.strip().split("/").pop()  # gives last item in list which is file

    ref_raw = None
    for pep_col in PEP_COLUMNS:
        for start_col in START_COLUMNS:
            try:
                ref_raw = pd.read_csv(file_path, index_col=False, usecols={start_col, pep_col})
                break
            except ValueError:
                ref_raw = None
        else:
            continue
        break

    return ref_raw


def init_test_raw(file_path):
    if not path.exists(file_path):
        print("Unable to find test file from path: " + file_path)
        return None

    global TEST_FILE_NAME
    TEST_FILE_NAME = file_path.strip().split("/").pop()  # gives last item in list which is file

    test_raw = None
    for pep_col in PEP_COLUMNS:
        for start_col in START_COLUMNS:
            try:
                test_raw = pd.read_csv(file_path, index_col=False, usecols={start_col, pep_col})
                break
            except ValueError:
                test_raw = None
        else:
            continue
        break

    return test_raw


def init_main_raw(file_path):
    if not path.exists(file_path):
        print("Unable to find main file: " + file_path)
        return None

    global MAIN_FILE_NAME
    MAIN_FILE_NAME = file_path.strip().split("/").pop()  # gives last item in list which is file

    try:
        main_raw = pd.read_csv(file_path, index_col=False, skiprows=1, usecols={"Description", "Starting Position"})
        return main_raw
    except ValueError:
        return None


def init_alignment(file_path):
    if not path.exists(file_path):
        print("Unable to find alignment file from path: " + file_path)
        return False

    try:
        with open(file_path) as my_file:
            sequences = build_sequences(my_file)

            indelResults = find_indels(sequences["ref"], sequences["test"])
            print("Insertions", indelResults["insertions"], "Deletions", indelResults["deletions"])
            global INSERTIONS
            INSERTIONS = indelResults["insertions"]
            global DELETIONS
            DELETIONS = indelResults["deletions"]

            if indelResults["inFrameshifts"] or indelResults["delFrameshifts"]:
                newWindow = Toplevel(window)
                newWindow.title("Warning")
                text = Text(newWindow)
                text.insert(INSERT,
                            "TOOL found one or more frameshift mutations in the pairwise alignment file provided "
                            "(listed below). Epitopes predicted from these sequences will not produce biologically "
                            "relevant matches when compared due to inherent differences in amino acids caused by the "
                            "frameshifted sequence. TOOL will still run but we do not suggest using these results.")

                frameshift_table = generate_frameshift_table(indelResults["inFrameshifts"],
                                                             indelResults["delFrameshifts"])
                text.insert(INSERT, "\n\n\n\n\n" + frameshift_table)
                text.pack(expand=0, fill=BOTH)

                # adding a tag to a part of text specifying the indices
                text.tag_add("bold1", "1.23", "1.43")
                text.tag_add("bold2", "1.149", "1.186")
                bold_font = Font(family="Calibri", size=10, weight="bold")
                text.tag_config("bold1", font=bold_font)
                text.tag_config("bold2", font=bold_font)
    except:
        print("Alignment file processing error")

    return True


def init_insertions(insertion_entry):
    if not insertion_entry:
        return True
    try:
        global INSERTIONS
        insertions = insertion_entry.split()
        for insertion in insertions:
            if not str.isdigit(insertion):
                raise
            INSERTIONS.append(int(insertion))
    except:
        return False
    return True


def init_deletions(deletion_entry):
    if not deletion_entry:
        return True
    try:
        global DELETIONS
        deletions = deletion_entry.split()
        for deletion in deletions:
            if not str.isdigit(deletion):
                raise
            DELETIONS.append(int(deletion))
    except:
        return False
    return True


def build_sequences(file):
    results = {}

    refSeq = ""
    testSeq = ""
    refCreated = True
    for line in file:
        if line[0] == ">":
            refCreated = not refCreated
        else:
            line = line.rstrip("\n")
            if not refCreated:
                refSeq += line
            else:
                testSeq += line

    results["ref"] = refSeq
    results["test"] = testSeq
    return results


def find_indels(ref_sequence, test_sequence):
    results = {}

    refResults = find_seq_indels(ref_sequence)
    results["insertions"] = refResults["indels"]
    results["inFrameshifts"] = refResults["frameshifts"]

    testResults = find_seq_indels(test_sequence)
    results["deletions"] = testResults["indels"]
    results["delFrameshifts"] = testResults["frameshifts"]

    return results


def find_seq_indels(sequence):
    results = {"indels": [], "frameshifts": {}}

    dashCount = 0
    nucleotidesCount = 0
    for char in sequence:
        nucleotidesCount += 1
        if char == '-':
            if dashCount != 2:
                dashCount += 1
            else:
                results["indels"].append(ceil(nucleotidesCount/3))
                dashCount = 0
        else:
            if dashCount == 1:
                results["frameshifts"][nucleotidesCount-1] = 1
                dashCount = 0
            if dashCount == 2:
                results["frameshifts"][nucleotidesCount - 2] = 2
                dashCount = 0
    if dashCount == 1:
        results["frameshifts"][nucleotidesCount] = 1
    if dashCount == 2:
        results["frameshifts"][nucleotidesCount - 1] = 2
    return results


def generate_frameshift_table(in_frameshifts, del_frameshifts):
    result = "Nucleotide position | # of ins/dels | Insertion/Deletion | Sequence in File\n"
    for key, value in in_frameshifts.items():
        nucleotideString = str(key)
        while len(nucleotideString) < 33:
            nucleotideString += " "
        result += nucleotideString + "| " + str(value) + "                      | Insertion                 | 1\n"

    for key, value in del_frameshifts.items():
        nucleotideString = str(key)
        while len(nucleotideString) < 33:
            nucleotideString += " "
        result += nucleotideString + "| " + str(value) + "                      | Deletion                  | 2\n"

    return result


def init_threshold(threshold_entry):
    global THRESHOLD
    if not threshold_entry:
        THRESHOLD = 1
        return True
    try:
        if not str.isdigit(threshold_entry):
            raise
        THRESHOLD = int(threshold_entry)
    except:
        THRESHOLD = 1
        return False
    return True


def generate_result_file(file_path):
    try:
        filename, file_extension = path.splitext(file_path)
        if file_extension and file_extension == ".xlsx":
            result_file = pd.ExcelWriter(file_path)
        else:
            result_file = pd.ExcelWriter(filename + ".xlsx")
    except:
        time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        print("Results file input error: Default file name used "
              "(" + "results_" + time + ".xlsx). File placed in directory with CAVES executable.")
        result_file = pd.ExcelWriter("results_" + time + ".xlsx")
    return result_file


def create_main_comparison_dict(main_dict_raw):
    main_list = list(main_dict_raw['data'])
    result_dict = {}
    for item in main_list:
        if type(item[0]) is int:
            result_dict = main_comparison_dict_insert(item[0], item[1], result_dict)
        else:
            result_dict = main_comparison_dict_insert(item[1], item[0], result_dict)
    return result_dict


def main_comparison_dict_insert(start, pep, res_dict):
    split = pep.split(" ")
    suffix = ""
    length = len(split[0])
    if len(split) > 1:
        suffix = " " + split[1] + " " + split[2]

    new_peptide = PeptideObject("main.csv", split[0], start, start + length - 1, length, suffix)
    if start not in res_dict:
        res_dict[start] = [new_peptide]
    else:
        res_dict[start].append(new_peptide)
    global MAIN_PEPTIDE_MAX_LENGTH
    MAIN_PEPTIDE_MAX_LENGTH = max(length, MAIN_PEPTIDE_MAX_LENGTH)
    return res_dict


def create_test_comparison_dict(sample_dict_raw, test_file_name):
    sample_list = list(sample_dict_raw['data'])
    result_dict = {}

    for item in sample_list:
        if type(item[0]) is int:
            result_dict = test_comparison_dict_insert(item[0], item[1], test_file_name, result_dict)
        else:
            result_dict = test_comparison_dict_insert(item[1], item[0], test_file_name, result_dict)
    return result_dict


def test_comparison_dict_insert(start, pep, test_file_name, res_dict):
    global THRESHOLD
    if len(pep) >= THRESHOLD:
        res_dict[start] = PeptideObject(test_file_name, pep, start, start + len(pep) - 1, len(pep), "")
        if test_file_name == REF_FILE_NAME:
            global REF_PEPTIDE_MAX_LENGTH
            REF_PEPTIDE_MAX_LENGTH = max(len(pep), REF_PEPTIDE_MAX_LENGTH)
        else:
            global TEST_PEPTIDE_MAX_LENGTH
            TEST_PEPTIDE_MAX_LENGTH = max(len(pep), TEST_PEPTIDE_MAX_LENGTH)
    return res_dict


def align_to_test_position(ref_position):
    test_position = ref_position
    for deletion in DELETIONS:
        if ref_position > deletion:
            test_position -= 1
    for insertion in INSERTIONS:
        if ref_position > insertion:
            test_position += 1
    return test_position


def align_to_ref_position(test_position):
    ref_position = test_position
    for deletion in DELETIONS:
        if test_position > deletion:
            ref_position += 1
    for insertion in INSERTIONS:
        if test_position > insertion:
            ref_position -= 1
    return ref_position


def get_result_object(result_type, input_file, level):
    if result_type == "matched" and level == 1:
        return L1_matched
    if result_type == "partial" and level == 1:
        return L1_partial
    if result_type == "novel" and level == 1:
        return L1_novel

    if result_type == "matched" and level == 2 and input_file == "L1m":
        return L1_matched_L2_matched
    if result_type == "partial" and level == 2 and input_file == "L1m":
        return L1_matched_L2_partial
    if result_type == "novel" and level == 2 and input_file == "L1m":
        return L1_matched_L2_novel

    if result_type == "matched" and level == 2 and input_file == "L1p":
        return L1_partial_L2_matched
    if result_type == "partial" and level == 2 and input_file == "L1p":
        return L1_partial_L2_partial
    if result_type == "novel" and level == 2 and input_file == "L1p":
        return L1_partial_L2_novel

    if result_type == "matched" and level == 2 and input_file == "L1n":
        return L1_novel_L2_matched
    if result_type == "partial" and level == 2 and input_file == "L1n":
        return L1_novel_L2_partial
    if result_type == "novel" and level == 2 and input_file == "L1n":
        return L1_novel_L2_novel


def create_match_df(obj):
    return pd.DataFrame({'Origin 1': obj.origin_file_one, 'Peptide 1': obj.peptide_one, 'Start 1': obj.start_one,
                         'End 1': obj.end_one, 'Length 1': obj.length_one, 'Origin 2': obj.origin_file_two,
                         'Peptide 2': obj.peptide_two, 'Start 2': obj.start_two, 'End 2': obj.end_two,
                         'Length 2': obj.length_two})


def create_partial_df(obj):
    return pd.DataFrame({'Origin 1': obj.origin_file_one, 'Peptide 1': obj.peptide_one, 'Start 1': obj.start_one,
                         'End 1': obj.end_one, 'Length 1': obj.length_one, 'Letters Matched': obj.letters_matched,
                         'Matched Length': obj.letters_matched_length, 'Origin 2': obj.origin_file_two,
                         'Peptide 2': obj.peptide_two, 'Start 2': obj.start_two, 'End 2': obj.end_two,
                         'Length 2': obj.length_two})


def create_novel_df(obj):
    return pd.DataFrame({'Origin': obj.origin_file_one, 'Peptide': obj.peptide_one, 'Start': obj.start_one,
                         'End': obj.end_one, 'Length': obj.length_one})


def insert_level_one_obj(lvl_one_dict, curr_pep):
    if curr_pep.start in lvl_one_dict:
        matched = False
        for item in lvl_one_dict[curr_pep.start]:
            if curr_pep.peptide == item.peptide and curr_pep.origin_file == item.origin_file\
                    and curr_pep.length == item.length:
                matched = True
        if not matched:
            lvl_one_dict[curr_pep.start].append(curr_pep)
            return True
    else:
        lvl_one_dict[curr_pep.start] = [curr_pep]
        return True
    return False


def insert_matched(result_obj, pep_one, pep_two):
    result_obj.origin_file_one.append(pep_one.origin_file + pep_one.suffix)
    result_obj.peptide_one.append(pep_one.peptide)
    result_obj.start_one.append(pep_one.start)
    result_obj.end_one.append(pep_one.end)
    result_obj.length_one.append(pep_one.length)

    result_obj.origin_file_two.append(pep_two.origin_file + pep_two.suffix)
    result_obj.peptide_two.append(pep_two.peptide)
    result_obj.start_two.append(pep_two.start)
    result_obj.end_two.append(pep_two.end)
    result_obj.length_two.append(pep_two.length)


def insert_partial(result_obj, pep_one, partial):
    result_obj.origin_file_one.append(pep_one.origin_file + pep_one.suffix)
    result_obj.peptide_one.append(pep_one.peptide)
    result_obj.start_one.append(pep_one.start)
    result_obj.end_one.append(pep_one.end)
    result_obj.length_one.append(pep_one.length)

    matched_letters = ""
    for pos, letter in sorted(partial[1].items()):
        matched_letters += letter
    result_obj.letters_matched.append(matched_letters)
    result_obj.letters_matched_length.append(len(matched_letters))

    result_obj.origin_file_two.append(partial[0].origin_file + partial[0].suffix)
    result_obj.peptide_two.append(partial[0].peptide)
    result_obj.start_two.append(partial[0].start)
    result_obj.end_two.append(partial[0].end)
    result_obj.length_two.append(partial[0].length)


def insert_novel(result_obj, pep_one):
    result_obj.origin_file_one.append(pep_one.origin_file + pep_one.suffix)
    result_obj.peptide_one.append(pep_one.peptide)
    result_obj.start_one.append(pep_one.start)
    result_obj.end_one.append(pep_one.end)
    result_obj.length_one.append(pep_one.length)


def all_novel_position_covered(partial_matches, novel_positions):
    for partial_match in partial_matches:
        for key in partial_match[1].keys():
            if key in novel_positions:
                del novel_positions[key]

    return len(novel_positions) == 0


def input_main_comparison_result(curr_pep, results, input_file):
    if "matched" in results:
        res_obj = get_result_object("matched", input_file, 2)
        for match in results["matched"]:
            insert_matched(res_obj, curr_pep, match)
    elif "partial" in results:
        res_obj = get_result_object("partial", input_file, 2)
        for partial in results["partial"]:
            insert_partial(res_obj, curr_pep, partial)
    else:
        res_obj = get_result_object("novel", input_file, 2)
        insert_novel(res_obj, curr_pep)


def input_test_comparison_result(curr_pep, results):
    if "novel" in results:
        insert_level_one_obj(L1_novel_dict, curr_pep)
        res_obj = get_result_object("novel", "", 1)
        insert_novel(res_obj, curr_pep)
        for novel in results["novel"]:
            if insert_level_one_obj(L1_novel_dict, novel):
                insert_novel(res_obj, novel)
    else:
        if "matched" in results:
            insert_level_one_obj(L1_matched_dict, curr_pep)
            result_obj = get_result_object("matched", "", 1)
            for match in results["matched"]:
                insert_level_one_obj(L1_matched_dict, match)
                insert_matched(result_obj, curr_pep, match)
        if "partial" in results:
            insert_level_one_obj(L1_partial_dict, curr_pep)
            result_obj = get_result_object("partial", "", 1)
            for partial in results["partial"]:
                insert_level_one_obj(L1_partial_dict, partial[0])
                insert_partial(result_obj, curr_pep, partial)


def calculate_main_comparison_parameters(test_peptide, aligned_start, main_peptide):
    result = {}
    if test_peptide.origin_file == TEST_FILE_NAME:
        if aligned_start > main_peptide.start:
            result["test_start"] = test_peptide.start
            result["main_start"] = aligned_start
        else:
            result["test_start"] = align_to_test_position(main_peptide.start)
            result["main_start"] = main_peptide.start
    else:
        if aligned_start > main_peptide.start:
            result["test_start"] = test_peptide.start
            result["main_start"] = test_peptide.start
        else:
            result["test_start"] = main_peptide.start
            result["main_start"] = main_peptide.start
    if main_peptide.end - result["main_start"] <= test_peptide.end - result["test_start"]:
        result["num_comp"] = main_peptide.end - result["main_start"] + 1
    else:
        result["num_comp"] = test_peptide.end - result["test_start"] + 1
    return result


def calculate_test_comparison_parameters(ref_peptide, test_peptide):
    result = {}

    if align_to_test_position(ref_peptide.start) > test_peptide.start:
        result["ref_start"] = ref_peptide.start
        result["test_start"] = align_to_test_position(ref_peptide.start)
    else:
        result["ref_start"] = align_to_ref_position(test_peptide.start)
        result["test_start"] = test_peptide.start
    if ref_peptide.end - result["ref_start"] <= test_peptide.end - result["test_start"]:
        result["num_comp"] = ref_peptide.end - result["ref_start"] + 1
    else:
        result["num_comp"] = test_peptide.end - result["test_start"] + 1
    return result


def compare_to_test_string(ref_peptide, test_peptide):
    results = []
    novel_positions = {}
    matched_positions = {}

    smallest_max_length = ref_peptide.length if ref_peptide.length < test_peptide.length else test_peptide.length

    comp_params = calculate_test_comparison_parameters(ref_peptide, test_peptide)

    ref_curr = comp_params["ref_start"] - ref_peptide.start
    test_curr = comp_params["test_start"] - test_peptide.start

    for i in range(0, comp_params["num_comp"]):
        if ref_peptide.peptide[ref_curr] == test_peptide.peptide[test_curr]:
            matched_positions[comp_params["ref_start"]+i] = ref_peptide.peptide[ref_curr]
        else:
            novel_positions[comp_params["ref_start"]+i] = ref_peptide.peptide[ref_curr]
        ref_curr += 1
        test_curr += 1

    if len(matched_positions) == smallest_max_length:
        results.append("matched")
    elif len(novel_positions) > 0:
        results.append("novel")
    else:
        results.append("partial")
        results.append(matched_positions)

    return results


def compare_to_main_string(test_peptide, aligned_start, aligned_end, main_peptide):
    results = []
    novel_positions = {}
    matched_positions = {}

    comp_params = calculate_main_comparison_parameters(test_peptide, aligned_start, main_peptide)

    test_curr = comp_params["test_start"] - test_peptide.start
    main_curr = comp_params["main_start"] - main_peptide.start

    for i in range(0, comp_params["num_comp"]):
        if test_peptide.peptide[test_curr] == main_peptide.peptide[main_curr]:
            matched_positions[comp_params["main_start"]+i] = main_peptide.peptide[main_curr]
        else:
            novel_positions[comp_params["main_start"]+i] = main_peptide.peptide[main_curr]
        test_curr += 1
        main_curr += 1

    if len(matched_positions) == test_peptide.length:
        results.append("matched")
    elif len(novel_positions) > 0:
        results.append("novel")
        results.append(novel_positions)
    else:
        results.append("partial")
        results.append(matched_positions)

    return results


def generate_test_comparisons(dictionary, ref_peptide):
    result = {}
    comp_results = {"matched": [], "partial": [], "novel_test_peps": []}
    aligned_test_start = align_to_test_position(ref_peptide.start)
    aligned_test_end = align_to_test_position(ref_peptide.end)

    curr_pos = max(1, aligned_test_start-TEST_PEPTIDE_MAX_LENGTH)

    # gather all possible comparisons for testing string
    while curr_pos <= aligned_test_end:
        if curr_pos in dictionary:
            test_peptide = dictionary[curr_pos]
            if ((test_peptide.start <= aligned_test_start <= test_peptide.end) or
                (test_peptide.start <= aligned_test_end <= test_peptide.end)) or \
                    ((aligned_test_start <= test_peptide.start <= aligned_test_end) or
                     (aligned_test_start <= test_peptide.end <= aligned_test_end)):
                comparison = compare_to_test_string(ref_peptide, test_peptide)
                if comparison[0] == "matched":
                    comp_results["matched"].append(test_peptide)
                elif comparison[0] == "partial":
                    comp_results["partial"].append([test_peptide, comparison[1]])
                elif comparison[0] == "novel":
                    comp_results["novel_test_peps"].append(test_peptide)

        curr_pos += 1

    if len(comp_results["novel_test_peps"]) > 0:
        result["novel"] = []
        for novel_test_pep in comp_results["novel_test_peps"]:
            result["novel"].append(novel_test_pep)
    elif len(comp_results["matched"]) == 0 and len(comp_results["partial"]) == 0:
        result["novel"] = []
    else:
        if len(comp_results["matched"]) > 0:
            result["matched"] = comp_results["matched"]
        if len(comp_results["partial"]) > 0:
            result["partial"] = comp_results["partial"]

    return result


def generate_main_comparisons(dictionary, test_peptide):
    result = {}
    comp_results = {"matched": [], "partial": [], "novel_pos_dict": {}}
    aligned_test_start = test_peptide.start
    aligned_test_end = test_peptide.end
    if test_peptide.origin_file == TEST_FILE_NAME:
        aligned_test_start = align_to_ref_position(aligned_test_start)
        aligned_test_end = align_to_ref_position(aligned_test_end)

    curr_pos = max(1, aligned_test_start-MAIN_PEPTIDE_MAX_LENGTH)

    # gather all possible comparisons for testing string
    while curr_pos <= aligned_test_end:
        if curr_pos in dictionary:
            for main_peptide in dictionary[curr_pos]:
                if ((main_peptide.start <= aligned_test_start <= main_peptide.end) or
                    (main_peptide.start <= aligned_test_end <= main_peptide.end)) or \
                        ((aligned_test_start <= main_peptide.start <= aligned_test_end) or
                         (aligned_test_start <= main_peptide.end <= aligned_test_end)):
                    comparison = \
                        compare_to_main_string(test_peptide, aligned_test_start, aligned_test_end, main_peptide)
                    if comparison[0] == "matched":
                        comp_results["matched"].append(main_peptide)
                    elif comparison[0] == "partial":
                        comp_results["partial"].append([main_peptide, comparison[1]])
                    elif comparison[0] == "novel":
                        for pos, letter in comparison[1].items():
                            comp_results["novel_pos_dict"][pos] = letter
        curr_pos += 1

    if len(comp_results["matched"]) > 0:
        result["matched"] = comp_results["matched"]
    elif len(comp_results["matched"]) == 0 and len(comp_results["partial"]) == 0:
        result["novel"] = test_peptide
    elif len(comp_results["novel_pos_dict"]) > 0:
        if len(comp_results["partial"]) == 0:
            result["novel"] = test_peptide
        else:
            if all_novel_position_covered(comp_results["partial"], comp_results["novel_pos_dict"]):
                result["partial"] = comp_results["partial"]
            else:
                result["novel"] = test_peptide
    elif len(comp_results["partial"]) > 0 and len(comp_results["matched"]) == 0 \
            and len(comp_results["novel_pos_dict"]) == 0:
        result["partial"] = comp_results["partial"]

    return result


def calculate_input_novel_test_peps(test_dict):
    for key, value in sorted(test_dict.items()):
        matched = False
        if key in L1_matched_dict:
            for potential in L1_matched_dict[key]:
                if potential.peptide == value.peptide and potential.origin_file == value.origin_file \
                        and potential.length == value.length:
                    matched = True
        if key in L1_partial_dict:
            for potential in L1_partial_dict[key]:
                if potential.peptide == value.peptide and potential.origin_file == value.origin_file \
                        and potential.length == value.length:
                    matched = True
        if key in L1_novel_dict:
            for potential in L1_novel_dict[key]:
                if potential.peptide == value.peptide and potential.origin_file == value.origin_file \
                        and potential.length == value.length:
                    matched = True
        if not matched:
            insert_level_one_obj(L1_novel_dict, value)
            res_obj = get_result_object("novel", "", 1)
            insert_novel(res_obj, value)


def generate_main_comparison_results(test_dict, main_dict, input_name):
    for key, value in sorted(test_dict.items()):
        for pep in value:
            results = generate_main_comparisons(main_dict, pep)
            input_main_comparison_result(pep, results, input_name)


def generate_test_comparison_results(ref_dict, test_dict):
    for key, value in sorted(ref_dict.items()):
        results = generate_test_comparisons(test_dict, value)
        input_test_comparison_result(value, results)
    calculate_input_novel_test_peps(test_dict)


# ----------------------------------------------- MAIN


if __name__ == '__main__':

    window = tk.Tk()
    font = Font(family="Calibri", size=10)
    window.option_add("*Font", font)

    window.title("CAVES")
    app = MainApplication(window)
    window.mainloop()