import json
import pandas as pd
import os
import glob

from os.path import join, dirname, abspath, exists, isdir

# relevant paths
home_path = dirname(dirname(dirname(abspath(__file__))))
output_ims_dir_path = join(home_path, "data", "images")

# list of csv files in current directory
datafiles = [f for f in os.listdir(dirname(__file__)) if (f.endswith('csv') and f != "MATH.csv")]

# json fields
question  =  {
    'Course': None,
    'Topic': None,
    'Original question' : None,
    'Codex input' : None,
    'Codex code' : None,
    'Codex code explanation' : None,
    'Program solution' : None,
    'Solution type': None,
    'GPT-3 response': None,
    'GPT-3 evaluation': None
}

COURSES_TO_PROCESS = [
    "18.01",
    "18.02",
    "18.03",
    "18.05",
    "18.06",
    "6.042",
    "COMS3251"
    ]

def get_codex_input(sheet, i):
    """
    retrieve the codex input for a given problem from a course
    """
    field = sheet['Codex Input'][i]
    if field == sheet['Original Problem'][i] or field == '':
        return 'Same as original question'
    else:
        return field

def get_program_solution(sheet, i, course_code):
    """
    retrieve the solution to a given problem from a course, in the form of text or path to image when applicable
    """
    output_plot_fname = join(output_ims_dir_path, course_code + "-q" + str(i+1) + "-codex-output-plot.png")
    if exists(output_plot_fname): # the question produces an image output; return file path
        path = "data/images/" + course_code + "-q" + str(i+1) + "-codex-output-plot.png"
        return path
    else: # otherwise return solution as in csv
        return sheet['Solution'][i]

def get_file_q_num(n):
    """
    returns 2-digit string representing a given number n
    """
    if n < 10:
        return "0" + str(n)
    else:
        return str(n)

if __name__ == "__main__":
    # Writing to jsons
    for filename in datafiles:
        course_name = filename[: -4].strip() # format of: "<course_code>""

        # read in sheet
        sheet = pd.read_csv(join(dirname(__file__),  filename))

        # set up file output directory
        out_dir_path = join(home_path, "data", course_name)
        if isdir(out_dir_path): # make course directory if DNE
            os.makedirs(out_dir_path)
        else:
            for f in glob.glob(out_dir_path + "/*"): # clear directory if exists before writing in new files
                os.remove(f)

        for i in range(1,26):
            question['Course'] = sheet['Course'][i-1]
            question['Topic'] = sheet['Topic'][i-1]
            question['Original question'] = sheet['Original Problem'][i-1]
            question['Program solution'] = get_program_solution(sheet, i-1, course_name)
            question['Codex input'] = get_codex_input(sheet, i-1)
            question['Codex code'] = sheet['Codex Code'][i-1]
            question['Codex code explanation'] = sheet['Codex Code Explanation'][i-1]
            question['Solution type'] = sheet['Solution Type'][i-1]
            question['GPT-3 response'] = sheet['GPT-3 Response'][i-1]
            question['GPT-3 evaluation'] = sheet['GPT-3 Evaluation'][i-1]
        
            json_object = json.dumps(question, indent = 7)
            fname = join(out_dir_path, course_name +'_'+'Question'+'_'+get_file_q_num(int(sheet['Id'][i-1]))+'.json')
            with open(fname, "w") as outfile:
                outfile.write(json_object)
