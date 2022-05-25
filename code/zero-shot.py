import openai 
import json
import pandas as pd
import time
from embedding import get_embeddings, get_most_similar

openai.api_key = "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" #given by OpenAI
courses_to_zero_shot = ['18.01']#, '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
questions_per_course = 3

embedding_location = "code/embeddings.json"
all_embeddings = get_embeddings(embedding_location)

docstring_front = '''"""\n''' 
docstring_back = '''\n"""\n'''
context_array = ['write a program', 'using sympy', 'using simulations']
prompt_prefix = 'that answers the following question:'
explanation_suffix = "\n\n'''\nHere's what the above class is doing:\n1."

#makes CSV's for each course:
for course_index, course in enumerate(courses_to_zero_shot):
    course_embeddings = all_embeddings[course_index*questions_per_course:(course_index+1)*questions_per_course]
    questions = []
    answers = []
    for num in range(1, questions_per_course+1):
        if num < 10:
                number = '0' + str(num)
        else:
            number = str(num)
        with open('./Data/'+course+'/'+course+'_Question_'+number+'.json', 'r') as f:
            data = json.load(f)
        raw_question = data['Original question']
        answer_to_question = data['Program solution']
        questions.append(raw_question)
        answers.append(answer_to_question)

    rows = []
    for i in range(questions_per_course):
        question_index = i
        original_question = questions[i]
        codex_input = docstring_front + context_array[0] + ' ' + prompt_prefix + ' ' + questions[i] + docstring_back
        start = time.time()
        print("Running Codex on " + course + " question " + str(i+1) + "...")
        codex_output = openai.Completion.create(engine = "code-davinci-002", 
                                                prompt = codex_input, 
                                                max_tokens = 256, 
                                                temperature = 0, 
                                                top_p = 0)['choices'][0]['text']
        explanation_input = codex_output + explanation_suffix
        explanation_output = openai.Completion.create(engine = "code-davinci-002", 
                                                      prompt = explanation_input, 
                                                      max_tokens = 150, 
                                                      temperature = 0, 
                                                      top_p = 0)['choices'][0]['text']
        gpt3_output = openai.Completion.create(engine = "text-davinci-002", 
                                               prompt = original_question, 
                                               max_tokens = 200, 
                                               temperature = 0, 
                                               top_p = 0)['choices'][0]['text']
        question_answer = answers[i]
        most_similar_questions = get_most_similar(course_embeddings,i)
        print(f'API call time: '+str(time.time()-start))
        rows.append([question_index, original_question, codex_input, codex_output, explanation_input, 
                     explanation_output, gpt3_output, question_answer, '', most_similar_questions])
    info = pd.DataFrame(rows, columns=['Question', 'Original Question', 'Codex Input', 'Codex Output', 'Codex Explanation Input', 
                                       'Codex Explanation', 'GPT-3 Output', 'Actual Solution', 'Codex: Correct or Incorrect?', "Most Similar Questions"])
    course_results_location = course + ' results.csv'
    info.to_csv(course_results_location, index=False)