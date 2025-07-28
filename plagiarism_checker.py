from difflib import SequenceMatcher
from tkinter.filedialog import askopenfilename

def plagiarism_checker(f1, f2):
    with open(f1, errors="ignore") as file1, open(f2, errors="ignore") as file2:
        f1_data = file1.read()
        f2_data = file2.read()
        res = SequenceMatcher(None, f1_data, f2_data).ratio()
        print(f"These files are {res * 100:.2f}% similar")

# Select files interactively
f1 = askopenfilename(title="Select the first file")
if not f1:
    print("No file selected for file 1.")
    exit()

f2 = askopenfilename(title="Select the second file")
if not f2:
    print("No file selected for file 2.")
    exit()

plagiarism_checker(f1, f2)