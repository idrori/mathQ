import json
import pandas as pd
import os
import glob

from os.path import join, dirname, abspath, isdir

# relevant paths
home_path = dirname(dirname(dirname(abspath(__file__))))
math_file = join(home_path, "code", "csv", "MATH.csv") # data source
out_dir_path = join(home_path, "data", "MATH") # output directory

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

def get_codex_input(sheet, i):
    """
    retrieve the codex input for a given problem from a course
    """
    field = sheet['Codex Input'][i]
    if field == sheet['Original Problem'][i] or field == '':
        return 'Same as original question'
    else:
        return field

def get_file_q_num(n):
    """
    returns 2-digit string representing a given number n
    """
    if n < 10:
        return "0" + str(n)
    else:
        return str(n)

if __name__ == "__main__":
    # read in sheet
    sheet = pd.read_csv(math_file)

    if not isdir(out_dir_path): # make course directory if DNE
        os.makedirs(out_dir_path)
    else:
        for f in glob.glob(out_dir_path + "/*"): # clear directory if exists before writing in new files
            os.remove(f)

    # write jsons for all questions
    for i in range(1,91):
        question['Course'] = sheet['Course'][i-1]
        question['Topic'] = sheet['Topic'][i-1]
        question['Original question'] = sheet['Original Problem'][i-1]
        question['Program solution'] = sheet['Solution'][i-1]
        question['Codex input'] = get_codex_input(sheet, i-1)
        question['Codex code'] = sheet['Codex Code'][i-1]
        question['Codex code explanation'] = sheet['Codex Code Explanation'][i-1]
        question['Solution type'] = sheet['Solution Type'][i-1]
        question['GPT-3 response'] = sheet['GPT-3 Response'][i-1]
        question['GPT-3 evaluation'] = sheet['GPT-3 Evaluation'][i-1]
    
        json_object = json.dumps(question, indent = 7)
        fname = join(out_dir_path, 'MATH_'+sheet['Topic'][i-1].strip().replace(" ","_")+'_Question_'+get_file_q_num(int(sheet['Id'][i-1]))+'.json')
        with open(fname, "w") as outfile:
            outfile.write(json_object)
