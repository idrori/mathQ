import openai 
import json
import pandas as pd
import time
from embedding import get_embeddings, get_most_similar

openai.api_key = "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" #given by OpenAI
courses_to_zero_shot = ['18.01']#, '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
questions_per_course = 3

codex_engine = "code-davinci-002"
gpt3_engine = "text-davinci-002"
engine_temperature = 0
engine_topP = 0
zero_shot_max_tokens = 256  #*****get value stated in paper**********
explanation_max_tokens = 150
gpt3_max_tokens = 200

embedding_location = "code/embeddings.json"

# for prompt formatting
docstring_front = '''"""\n''' 
docstring_back = '''\n"""\n'''
context_array = ['write a program', 'using sympy', 'using simulations']
prompt_prefix = 'that answers the following question:'
explanation_suffix = "\n\n'''\nHere's what the above class is doing:\n1."


all_embeddings = get_embeddings(embedding_location)
for course_index, course in enumerate(courses_to_zero_shot):
    course_embeddings = all_embeddings[course_index*questions_per_course:(course_index+1)*questions_per_course]
    questions = []
    answers = []
    for num in range(1, questions_per_course+1):
        if num < 10:
                q_num = '0' + str(num)
        else:
            q_num = str(num)
        json_location = './Data/' + course + '/' + course + '_Question_' + q_num + '.json'
        with open(json_location, 'r') as f:
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
        codex_output = openai.Completion.create(engine = codex_engine, 
                                                prompt = codex_input, 
                                                max_tokens = zero_shot_max_tokens, 
                                                temperature = engine_temperature, 
                                                top_p = engine_topP)['choices'][0]['text']
        explanation_input = codex_output + explanation_suffix
        explanation_output = openai.Completion.create(engine = codex_engine, 
                                                      prompt = explanation_input, 
                                                      max_tokens = explanation_max_tokens, 
                                                      temperature = engine_temperature, 
                                                      top_p = engine_topP)['choices'][0]['text']
        gpt3_output = openai.Completion.create(engine = gpt3_engine, 
                                               prompt = original_question, 
                                               max_tokens = gpt3_max_tokens, 
                                               temperature = engine_temperature, 
                                               top_p = engine_topP)['choices'][0]['text']
        question_answer = answers[i]
        most_similar_questions = get_most_similar(course_embeddings,i)
        end = time.time()
        print(f'API call time: '+str(end-start))
        rows.append([question_index, original_question, codex_input, codex_output, explanation_input, 
                     explanation_output, gpt3_output, question_answer, '', most_similar_questions])
    info = pd.DataFrame(rows, columns=['Question', 'Original Question', 'Codex Input', 'Codex Output', 'Codex Explanation Input', 
                                       'Codex Explanation', 'GPT-3 Output', 'Actual Solution', 'Zero-Shot: Correct/Incorrect', "Most Similar Questions"])
    course_results_location = course + ' results.csv'
    info.to_csv(course_results_location, index=False)