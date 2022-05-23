import json
import pandas as pd
import os
import glob

from os import listdir
from os.path import isfile, join, dirname, abspath

# relevant paths
raw_data_path = os.path.join(dirname(__file__), "Raw Data")
json_dirs_path = os.path.join(dirname(dirname(abspath(__file__))), "Data")
datafiles = [f for f in listdir(raw_data_path) if isfile(join(raw_data_path, f))]
output_ims_dir_path = os.path.join(dirname(dirname(abspath(__file__))), "Data", "Images")

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
    field = sheet['Codex Input'][i]
    if field == sheet['Original Problem'][i] or field == '':
        return 'Same as original question'
    else:
        return field

def get_program_solution(sheet, i, course_code):
    output_plot_fname = os.path.join(output_ims_dir_path, course_code + "-q" + str(i+1) + "-codex-output-plot.png")
    if os.path.exists(output_plot_fname): # the question produces an image output; return file path
        path = "Data/Images/" + course_code + "-q" + str(i+1) + "-codex-output-plot.png"
        return path
    elif 'Codex Run Output' in sheet and sheet['Codex Run Output'][i] != '': 
        return sheet['Codex Run Output'][i]
    else: # otherwise return normal solution
        return sheet['Solution'][i]


COURSES_TO_PROCESS = [
    "18.01",
    "18.02",
    "18.03",
    "18.05",
    "18.06",
    "6.042",
    "COMS3251"
    ]

if __name__ == "__main__":
    # Writing to jsons
    for filename in datafiles:
        course_name = filename[: -4].strip() # format of: "<course_code>""

        if course_name in COURSES_TO_PROCESS:
            # read in sheet
            sheet = pd.read_csv(os.path.join(raw_data_path, filename))

            # set up file output directory
            out_dir_path = os.path.join(json_dirs_path, course_name)
            if not os.path.isdir(out_dir_path): # make course directory if DNE
                os.makedirs(out_dir_path)
            else:
                for f in glob.glob(out_dir_path + "/*"): # clear directory if exists before writing in new files
                    os.remove(f)

            for i in range(1,26):
                try:
                    if str(sheet['Output Evaluation'][i-1]).lower() == 'correct':
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
                        with open(os.path.join(out_dir_path, course_name +'_'+'Question'+'_'+str(int(sheet['Id'][i-1]))+'.json'), "w") as outfile:
                            outfile.write(json_object)
                except Exception as e:
                    print('\terror', course_name, 'question', i, e)
                    pass