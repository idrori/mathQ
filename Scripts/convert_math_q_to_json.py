import json
import pandas as pd
import os
import glob

from os.path import dirname, abspath

# relevant paths
raw_data_path = os.path.join(dirname(__file__), "Raw Data")
json_dirs_path = os.path.join(dirname(dirname(abspath(__file__))), "Data")
math_file = os.path.join(raw_data_path, "MATH.csv")

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

course_name = "MATH"

def get_codex_input(sheet, i):
    field = sheet['Codex Input'][i]
    if field == sheet['Original Problem'][i] or field == '':
        return 'Same as original question'
    else:
        return field

if __name__ == "__main__":
    # read in sheet
    sheet = pd.read_csv(math_file)
    # set up file output directory
    out_dir_path = os.path.join(json_dirs_path, course_name)
    if not os.path.isdir(out_dir_path): # make course directory if DNE
        os.makedirs(out_dir_path)
    else:
        for f in glob.glob(out_dir_path + "/*"): # clear directory if exists before writing in new files
            os.remove(f)

    # write jsons for all questions
    for i in range(1,91):
        try:
            evaluation = str(sheet['Output Evaluation'][i-1]).lower()
            if 'correct' in evaluation and 'incorrect' not in evaluation:
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
                with open(os.path.join(out_dir_path, 'MATH_'+sheet['Topic'][i-1].strip().replace(" ","_")+'_Question_'+str(int(sheet['Id'][i-1]))+'.json'), "w") as outfile:
                    outfile.write(json_object)
        except Exception as e:
            print('\terror', course_name, 'question', i, e)
            pass
