import openai 
import pandas as pd
import time
from embedding import OpenAI_API_Key

openai.api_key = OpenAI_API_Key 
courses_to_few_shot = ['18.01', '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
MATH_sections_to_few_shot = ['MATH_Algebra', 'MATH_Counting_&_Probability', 'MATH_Intermediate_Algebra', 
                             'MATH_Number_Theory', 'MATH_Prealgebra', 'MATH_Precalculus']
questions_per_course = 25
questions_per_MATH_section = 15

#Will use this many few-shot examples if possible: (if fewer are solved, use as many as possible)
few_shot_examples_desired = 5
codex_engine = "code-davinci-002"
gpt3_engine = "text-davinci-002"
engine_temperature = 0
engine_topP = 0
few_shot_max_tokens = 256
gpt3_CoT_max_tokens = 1000
CoT = "Let's think step by step."

def execute_few_shot(courses, questions_per):
    """
    Runs few-shot on questions_per questions for each course in courses.
    """
    for course in courses:
        course_location = course + ' results.csv'
        #initializing new columns in csv
        results = pd.read_csv(course_location)
        results['Few Shot Input'] = ''
        results['Few Shot Output'] = ''
        results['Few Shot Evaluation'] = ''
        results.to_csv(course_location, index=False)

        for i in range(questions_per):
            k = few_shot_examples_desired

            #correct via zero-shot:
            if results.iloc[i]['Zero-Shot Evaluation'] == 1:
                print('no few shot needed for ' + course + ' question ' + str(i+1))
                few_shot_input = 'n/a'
                few_shot_output = 'n/a'

            #incorrect via zero-shot:
            elif results.iloc[i]['Zero-Shot Evaluation'] == 0:
                few_shot_input = ''
                print('doing few-shot for ' + course + ' question ' + str(i+1) + '...')
                for closest in results.iloc[i]["Most Similar Questions"].strip('][').split(', '):
                    closest_index = int(closest) - 1
                    if results.iloc[closest_index]['Zero-Shot Evaluation'] == 1 and k > 0:
                        few_shot_input += results.iloc[closest_index]['Codex Input']
                        few_shot_input += results.iloc[closest_index]['Codex Output']+'\n\n'
                        k -= 1
                few_shot_input += results.iloc[i]['Codex Input']
                start = time.time()
                time.sleep(1.5) #to avoid an openai.error.RateLimitError
                few_shot_output = openai.Completion.create(engine = codex_engine, 
                                                        prompt = few_shot_input, 
                                                        max_tokens = few_shot_max_tokens, 
                                                        temperature = engine_temperature, 
                                                        top_p = engine_topP)['choices'][0]['text']
                print('API call time: ' + str(time.time()-start) + '\n')

            #columns not properly labelled with 1's and 0's:
            else:
                print('question not labeled 1 for correct or 0 for incorrect was detected')
                raise ValueError

            results.loc[i, 'Few Shot Input'] = few_shot_input
            results.loc[i, 'Few Shot Output'] = few_shot_output
            results.to_csv(course_location, index=False)

def execute_GPT3_CoT_one_shot(courses, questions_per):
    """
    Runs one-shot CoT on questions_per questions for each course in courses.
    """
    for course in courses:
        course_location = course + ' results.csv'
        #initializing new columns in csv
        results = pd.read_csv(course_location)
        results['GPT-3 CoT Few Shot Input'] = ''
        results['GPT-3 CoT Few Shot Output'] = ''
        results['GPT-3 CoT Few Show Evaluation'] = ''
        results.to_csv(course_location, index=False)

        for i in range(questions_per):
            closest_index = int(results.iloc[i]["Most Similar Questions"].strip('][').split(', ')[0]) - 1
            similar_question = results.iloc[closest_index]["Original Question"]
            similar_answer = results.iloc[closest_index]["Actual Solution"]
            original_question = results.iloc[i]["Original Question"]
            gpt3_CoT_input = 'Q: ' + similar_question + '\nA: ' + str(similar_answer) + '\n\nQ: ' + original_question + "\nA: " + CoT
            gpt3_CoT_output = openai.Completion.create(engine = gpt3_engine,
                                                       prompt = gpt3_CoT_input,
                                                       max_tokens = gpt3_CoT_max_tokens,
                                                       temperature = engine_temperature,
                                                       top_p = engine_topP)['choices'][0]['text']
            results.loc[i, 'GPT-3 CoT Few Shot Input'] = gpt3_CoT_input
            results.loc[i, 'GPT-3 CoT Few Shot Output'] = gpt3_CoT_output
            results.to_csv(course_location, index=False)
            


if __name__ == "__main__":
    execute_few_shot(courses_to_few_shot, questions_per_course)
    execute_GPT3_CoT_one_shot(courses_to_few_shot, questions_per_course)
    execute_few_shot(MATH_sections_to_few_shot, questions_per_MATH_section)
    execute_GPT3_CoT_one_shot(MATH_sections_to_few_shot, questions_per_MATH_section)