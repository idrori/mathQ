To run this code, make sure to have an OpenAI API key inserted into each of the code files:

1. In a terminal, run `python3 code/embedding.py`.

This step embeds and saves all question embeddings from the university math courses (`course_embeddings.json`) and MATH benchmark (`MATH_embeddings.json`). It also creates an image of the embeddings after reducing dimensionality by UMAP(`UMAP.png`).

2. In a terminal, run `python3 code/zero-shot.py`.

This step creates a CSV file for each course(`COURSE results.csv`), automatically adds context to the prompts, and generates a program for each prompt. Each program is automatically explained, and GPT-3's response to the original question is generated. 

3. In each of the created CSVs: Run each program. Then, under the column `Zero-Shot Evaluation,` place a one if the program is correct and 0 otherwise (see column `Actual Solution`). Then, label the GPT-3 responses in the same manner under the column `GPT-3 Evaluation`. Make sure all entries under `Zero-Shot Evaluation` are labeled before step 4. **Note: This step may take over 30 minutes to run due to the length of API calls.**

This step evaluates each generated program and corresponding GPT-3 response by labeling each generated program(1 for correct and 0 for incorrect) and each GPT-3 response to evaluate Codex's and GPT-3's performance.

4. In a terminal, run `python3 code/few-shot.py`.

This step takes the labels given to each generated program and performs few-shot learning for each prompt by providing (question, code) examples to Codex. We create the new prompt with the examples and generate a new program. Also, few-shot learning performed with GPT-3 combined with the chain of thought (CoT) string "Let's think step by step.".

5. Repeat step 3 but for the programs and responses generated via few-shot learning.

This step labels each program generated via few-shot learning to evaluate Codex's performance.

\
Figures: directory figures contains code and data that reproduce the figures in the paper.
