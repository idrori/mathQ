import openai 
import json
import pandas as pd
import time
from embedding import get_embeddings

openai.api_key = "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" #given by OpenAI
courses_to_zero_shot = ['18.01', '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
MATH_sections_to_zero_shot = ['MATH_Algebra', 'MATH_Counting_&_Probability', 'MATH_Intermediate_Algebra',
                              'MATH_Number_Theory', 'MATH_Prealgebra', 'MATH_Precalculus']
questions_per_course = 25
questions_per_MATH_section = 15
# codex_engine = "code-davinci-002"
gpt3_engine = "text-davinci-002"
engine_temperature = 0
engine_topP = 0
zero_shot_max_tokens = 256 
explanation_max_tokens = 150
gpt3_max_tokens = 1000
CoT = "Let's think step by step."

courses_embeddings_location = 'code/course_embeddings.json'
MATH_embeddings_location = 'code/MATH_embeddings.json'


def execute_GPT3_CoT(courses, questions_per, embeddings_location):
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
            question = i + 1
            original_question = questions[i]
            question_answer = answers[i]
            print("GPT-3 CoT on " + course + " question " + str(question) + "...\n")
            gpt3_input = 'Q: ' + original_question + "\nA: " + CoT
            gpt3_output = openai.Completion.create(engine = gpt3_engine,
                                                prompt = gpt3_input,
                                                max_tokens = gpt3_max_tokens,
                                                temperature = engine_temperature,
                                                top_p = engine_topP)['choices'][0]['text']
           
            rows.append([question, original_question, question_answer,
                         gpt3_input, gpt3_output])
        info = pd.DataFrame(rows, columns=['Question', 'Original Question', 'Actual Solution',
                                           'GPT-3 Input', 'GPT-3 Output'])
        course_results_location = course + ' GPT3_CoT_results.csv'
        info.to_csv(course_results_location, index=False)

if __name__ == "__main__":
    #CoT step for courses:
    # execute_GPT3_CoT(courses_to_zero_shot, questions_per_course, courses_embeddings_location)
    #CoT step for MATH benchmark:
    execute_GPT3_CoT(MATH_sections_to_zero_shot, questions_per_MATH_section, MATH_embeddings_location)
