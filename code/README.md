To run this code make sure you have an OpenAI API key and insert it into each of the code files:

1. In your terminal, run `python3 code/embedding.py`.

This will embed and save all of the question embeddings from both the courses(`course_embeddings.json`) and MATH(`MATH_embeddings.json`). It also creates an image of the embeddings after they have had their dimensionality reduced via UMAP(`UMAP.png`).

2. In your terminal, run `python3 code/zero-shot.py`.

This step creates a csv file for each course(`COURSE results.csv`), automatically adds context to the prompts, and generates a program for each prompt. Also, each generated program is explained and GPT-3's solution for the original question is generated. 

3. In each of the created CSV's, do the following: Run each program. Then, under the column `Zero-Shot Evaluation`, put a 1 if the program is correct, and 0 if the program is incorrect(see column `Actual Solution`). Then, label the GPT-3 responses in the same manner under the column `GPT-3 Evaluation`. Make sure all entries under `Zero-Shot Evaluation` are labelled before doing step 4. **Note: This step may take over 30 minutes to run due to the length of API calls.**

This step evaluates each generated program and corresponding GPT-3 response by labeling each generated program(1 for correct and 0 for incorrect) and each GPT-3 response to evaluate Codex's and GPT-3's performance.

4. In your terminal, run `python3 code/few-shot.py`.

This step takes the labels that you have given to each generated program, and does few-shot learning for each prompt by providing (question, code) examples to codex. We create the new prompt with the examples and generate a new program. Also, one-shot learning is done with GPT-3 in combination with the CoT string "Lets think step by step.".

5. Repeat step 3 but for the programs and responses generated via few-shot learning.

This step labels each program generated via few-shot learning in order to evaluate Codex's performance.
