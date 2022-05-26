To run this code make sure you have an OpenAI API key:

1. In your terminal, run `python3 code/embedding.py`

This will embed and save all of the question embeddings from each course(embeddings.json) and create an image of the embeddings after they have had their         dimensionality reduced via UMAP(UMAP.png).

2. In your terminal, run `python3 code/zero-shot.py`

This step creates a csv file for each course, automatically adds context to the prompts, and generates a program for each prompt. Also, each generated program is explained and GPT-3's solution for the original problem is included. 

3. In each of the created CSV's, evaluate each generated program by doing the following: Run each program. Then, under the column "Zero-Shot: Correct/Incorrect", put a 1 if the program is correct, and 0 if the program is incorrect.

This step labels each generated program(1 for correct and 0 for incorrect) to evaluate Codex's performance.

4. In your terminal, run `python3 code/few-shot.py`

This step takes the labels that you have given to each generated program, and does few-shot learning for each prompt by providing (question, code) examples to codex. We create the new prompt with the examples and generate a new program. 

5. Repeat step 3 but for the programs generated via few-shot learning.

This step labels each program generated via few-shot learning in order to evaluate Codex's performance.
