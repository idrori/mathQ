import openai 
import pandas as pd
import time

openai.api_key = "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" #given by OpenAI
courses = ['18.01']#, '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
questions_per_course = 10
few_shot_examples = 3 #AT MOST number of few shot examples to include to(if fewer are currently unsolved, then all solved are used)

for course in courses:
    results = pd.read_csv(course+'.csv')
    results['Few Shot Input'] = ''
    results['Few Shot Output'] = ''
    results['Few Shot Evaluation'] = ''
    results.to_csv(course+'.csv', index=False)
    for i in range(questions_per_course):
        k = few_shot_examples
        if results.iloc[i]['Codex: Correct or Incorrect?'] == 1: #already correct 
            print('already solved, no few shot needed')
            few_shot_input = 'n/a'
            few_shot_output = 'n/a'
        elif results.iloc[i]['Codex: Correct or Incorrect?'] == 0: #do few shot stuff
            few_shot_input = ''
            print('doing few shot for question '+str(i+1))
            for closest in results.iloc[i]["Most Similar Questions"].strip('][').split(', '):
                closest_index = int(closest) - 1
                if results.iloc[closest_index]['Codex: Correct or Incorrect?'] == 1 and k>0: #this one as been solved
                    few_shot_input+=results.iloc[closest_index]['Codex Input']
                    few_shot_input+=results.iloc[closest_index]['Codex Output']+'\n\n'
                    k-=1
            few_shot_input += results.iloc[i]['Codex Input']
            # print('-----')
            # print(few_shot_input)
            # print('-----')
            few_shot_output = openai.Completion.create(engine = "code-davinci-002", prompt = few_shot_input, max_tokens = 256, temperature = 0, top_p = 0)['choices'][0]['text']
        else: #if you didn't label evaluation column
            print('question not labeled 1 for correct or 0 for incorrect')
            raise ValueError
        #add to csv here
        results.loc[i, 'Few Shot Input'] = few_shot_input
        results.loc[i, 'Few Shot Output'] = few_shot_output
        results.to_csv(course+'.csv', index=False)

# print(results['Original Question'][1]) #2nd question
# print(results.iloc[1]['Original Question']) #2nd question