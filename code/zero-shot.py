import openai 
import json
import pandas as pd
import time
from embedding import get_embeddings, get_most_similar

openai.api_key = "" #given by OpenAI
courses_to_zero_shot = ['18.01', '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
MATH_sections_to_zero_shot = ['MATH_Algebra', 'MATH_Counting_&_Probability', 'MATH_Intermediate_Algebra', 
                              'MATH_Number_Theory', 'MATH_Prealgebra', 'MATH_Precalculus']
questions_per_course = 25
questions_per_MATH_section = 15
codex_engine = "code-davinci-002"
gpt3_engine = "text-davinci-002"
engine_temperature = 0
engine_topP = 0
zero_shot_max_tokens = 256 
explanation_max_tokens = 150
gpt3_max_tokens = 200

courses_embeddings_location = 'code/course_embeddings.json'
MATH_embeddings_location = 'code/MATH_embeddings.json'

# for prompt formatting:
docstring_front = '''"""\n''' 
docstring_back = '''\n"""\n'''
context_array = ['write a program', 'using sympy', 'using simulations']
prompt_prefix = 'that answers the following question:'
explanation_suffix = "\n\n'''\nHere's what the above code is doing:\n1."

def execute_zero_shot(courses, questions_per, embeddings_location):
    """
    Runs zero-shot on questions_per questions for each course in courses. 
    An individual CSV file of the results is made for each course in courses.
    The embeddings for all of the questions for all of the courses in courses are located in embeddings_location.
    """
    all_embeddings = get_embeddings(embeddings_location)
    for course_index, course in enumerate(courses):
        course_embeddings = all_embeddings[course_index*questions_per:(course_index+1)*questions_per]
        questions = []
        answers = []
        for num in range(1, questions_per + 1):
            if num < 10:
                q_num = '0' + str(num)
            else:
                q_num = str(num)
            json_location = './Data/' + course.split('_')[0] + '/' + course + '_Question_' + q_num + '.json'
            with open(json_location, 'r') as f:
                data = json.load(f)
            raw_question = data['Original question']
            answer_to_question = data['Program solution']
            questions.append(raw_question)
            answers.append(answer_to_question)

        rows = []
        for i in range(questions_per):
            question = i+1
            original_question = questions[i]
            codex_input = docstring_front + context_array[0] + ' ' + prompt_prefix + ' ' + questions[i] + docstring_back
            start = time.time()
            time.sleep(1.5) #to avoid an openai.error.RateLimitError
            print("Running Codex on " + course + " question " + str(i+1) + "...")
            codex_output = openai.Completion.create(engine = codex_engine, 
                                                    prompt = codex_input, 
                                                    max_tokens = zero_shot_max_tokens, 
                                                    temperature = engine_temperature, 
                                                    top_p = engine_topP)['choices'][0]['text']
            explanation_input = codex_input + codex_output + explanation_suffix
            time.sleep(1.5) #to avoid an openai.error.RateLimitError
            explanation_output = openai.Completion.create(engine = codex_engine, 
                                                        prompt = explanation_input, 
                                                        max_tokens = explanation_max_tokens, 
                                                        temperature = engine_temperature, 
                                                        top_p = engine_topP)['choices'][0]['text']
            time.sleep(1.5) #to avoid an openai.error.RateLimitError
            gpt3_output = openai.Completion.create(engine = gpt3_engine, 
                                                prompt = original_question, 
                                                max_tokens = gpt3_max_tokens, 
                                                temperature = engine_temperature, 
                                                top_p = engine_topP)['choices'][0]['text']
            question_answer = answers[i]
            most_similar_questions = get_most_similar(course_embeddings,i)
            end = time.time()
            print('API call time: ' + str(end-start) + '\n')
            rows.append([question, original_question, codex_input, codex_output, explanation_input, 
                        explanation_output, gpt3_output, question_answer, '', most_similar_questions])
        info = pd.DataFrame(rows, columns=['Question', 'Original Question', 'Codex Input', 'Codex Output', 'Codex Explanation Input', 
                                        'Codex Explanation', 'GPT-3 Output', 'Actual Solution', 'Zero-Shot Evaluation', 'Most Similar Questions'])
        course_results_location = course + ' results.csv'
        info.to_csv(course_results_location, index=False)

if __name__ == "__main__":
    #zero-shot step for courses:
    execute_zero_shot(courses_to_zero_shot, questions_per_course, courses_embeddings_location)
    #zero-shot step for MATH benchmark:
    execute_zero_shot(MATH_sections_to_zero_shot, questions_per_MATH_section, MATH_embeddings_location)