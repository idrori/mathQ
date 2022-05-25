import openai 
import pandas as pd
import time

openai.api_key = "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" #given by OpenAI
courses_to_few_shot = ['18.01']#, '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
questions_per_course = 3
few_shot_examples_desired = 2 #AT MOST number of few shot examples to include to(if fewer are currently unsolved, then all solved are used)
codex_engine = "code-davinci-002"
engine_temperature = 0
engine_topP = 0


for course in courses_to_few_shot:
    course_location = course + ' results.csv'
    results = pd.read_csv(course_location)
    results['Few Shot Input'] = ''
    results['Few Shot Output'] = ''
    results['Few Shot Evaluation'] = ''
    results.to_csv(course_location, index=False)
    for i in range(questions_per_course):
        k = few_shot_examples_desired

        #correct via zero-shot:
        if results.iloc[i]['Zero-Shot: Correct/Incorrect'] == 1:
            print('no few shot needed for ' + course + ' question ' + str(i+1))
            few_shot_input = 'n/a'
            few_shot_output = 'n/a'

        #incorrect via zero-shot:
        elif results.iloc[i]['Zero-Shot: Correct/Incorrect'] == 0:
            few_shot_input = ''
            print('doing few shot for ' + course + ' question ' + str(i+1))
            for closest in results.iloc[i]["Most Similar Questions"].strip('][').split(', '):
                closest_index = int(closest) - 1
                if results.iloc[closest_index]['Zero-Shot: Correct/Incorrect'] == 1 and k > 0:
                    few_shot_input += results.iloc[closest_index]['Codex Input']
                    few_shot_input += results.iloc[closest_index]['Codex Output']+'\n\n'
                    k -= 1
            few_shot_input += results.iloc[i]['Codex Input']
            start = time.time()
            few_shot_output = openai.Completion.create(engine = codex_engine, 
                                                       prompt = few_shot_input, 
                                                       max_tokens = 256, 
                                                       temperature = engine_temperature, 
                                                       top_p = engine_topP)['choices'][0]['text']
            print(f'API call time: ' + str(time.time()-start))

        #columns not properly labelled with 1's and 0's:
        else:
            print('question not labeled 1 for correct or 0 for incorrect was detected')
            raise ValueError

        
        results.loc[i, 'Few Shot Input'] = few_shot_input
        results.loc[i, 'Few Shot Output'] = few_shot_output
        results.to_csv(course_location, index=False)