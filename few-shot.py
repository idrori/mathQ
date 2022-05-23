import openai 
import pandas as pd
import time

openai.api_key = "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" #given by OpenAI
courses = ['18.01']#, '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
questions_per_course = 3

for course in courses:
    results = pd.read_csv(course+'.csv')
    for i in range(questions_per_course):
        if results.iloc[i]['Codex: Correct or Incorrect?'] == 1:
            #already correct 
            print('already solved')
        elif results.iloc[i]['Codex: Correct or Incorrect?'] == 0:
            #do few shot stuff
            print('gotta do few shot')
        else:
            print('something went wrong')
    # for i in results:
    #     print(results[i])
#     print(results['Original Question'])
# print(results['Original Question'][1]) #2nd question

# print(results.iloc[1]['Original Question'])
