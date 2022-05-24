import openai 
import json
import pandas as pd
import time
from sentence_transformers import util
from embedding import get_embeddings

openai.api_key = "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" #given by OpenAI
courses = ['18.01']#, '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
questions_per_course = 3

def get_most_similar(embeddings, i):
    """returns most similar questions to the target, index i, via cosine similarity"""
    #cosine similarity
    cos_sims = []
    cos_to_num = {}
    for j in range(len(embeddings)):
        cos_sim = util.cos_sim(embeddings[i], embeddings[j]).item()
        cos_to_num[cos_sim] = j
        cos_sims.append(cos_sim)
    ordered = sorted(cos_sims, reverse=True)
    closest_qs = []
    for val in ordered:
        closest_qs.append(cos_to_num[val]+1)
    # print("Here are the next closest questions to "+str(i+1)+" :"+str(closest_qs[1:]))
    return closest_qs[1:]

all_embeddings = get_embeddings("code/embeddings.json")

#makes input for each prompt
front_piece = '''"""\n''' #these two lines add triple quotes to the prompt like a doc string
back_piece = '''\n"""\n'''
context = 'Write a program, using numpy, sympy and other python libraries, that answers the following question: '
 
#makes CSV's for each course:
for course_index, course in enumerate(courses):
    course_embeddings = all_embeddings[course_index*questions_per_course:(course_index+1)*questions_per_course]
    questions = []
    for num in [i for i in range(1, questions_per_course+1)]:
        if num<10:
                number='0'+str(num)
        else:
            number=str(num)
        with open('./Data/'+course+'/'+course+'_Question_'+number+'.json', 'r') as f:
            data = json.load(f)
        raw_question = data['Original question']
        questions.append(raw_question)
    entries = [[i+1,questions[i],front_piece+context+questions[i]+back_piece] for i in range(questions_per_course)]
    for i in range(questions_per_course):
        start = time.time()
        print(f"{course} question {i+1}")
        entries[i].append(openai.Completion.create(engine = "code-cushman-001", prompt = entries[i][2], max_tokens = 256, temperature = 0, top_p = 0)['choices'][0]['text'])
        entries[i].append(entries[i][3]+"\n\n'''\nHere's what the above class is doing:\n1.")
        entries[i].append(openai.Completion.create(engine = "code-davinci-002", prompt = entries[i][3]+"\n\n'''\nHere's what the above class is doing:\n1.", max_tokens = 150, temperature = 0, top_p = 0)['choices'][0]['text'])
        entries[i].append(openai.Completion.create(engine= "text-davinci-002", prompt = entries[i][1], max_tokens = 200, temperature = 0, top_p = 0)['choices'][0]['text'])
        entries[i].append('')  #actual solution, will do this later
        entries[i].append('')  #this column is filled in by the person
        entries[i].append(get_most_similar(course_embeddings,i))
        print(f'API call time: '+str(time.time()-start))
    info = pd.DataFrame(entries, columns=['Question', 'Original Question', 'Codex Input', 'Codex Output', 'Codex Explanation Input', 'Codex Explanation', 'GPT-3 Output', 'Actual Solution', 'Codex: Correct or Incorrect?', "Most Similar Questions"])
    info.to_csv(course+'.csv', index=False)