# User Guide

This directory contains code that reproduces all results and figures in the paper and supplementary information.

## 1. Install required packages

**fill in packages here**
```
pip install openai
pip install umap
pip install sentence_transformers
```

## 2. Set OpenAI API Key
```
export OpenAI_API_Key='(YOUR KEY HERE)'
```

## 3. Embed questions
```
python3 code/embedding.py
```
This will embed and save all of the question embeddings from the courses as `course_embeddings.json` and MATH as `MATH_embeddings.json`. It also creates an image of the embeddings after they have had their dimensionality reduced via UMAP as `UMAP.png`.

## 4. Zero-shot (Codex, GPT-3, GPT-3 CoT, Codex Explanation)

- This step takes a long time due to the API calls(30+ minutes). Make sure to only do operations above that you want!
- Evaluation Column is for **you** to fill in. If the respective response is correct, put 1. If Incorrect, put 0.
- Rerunning ``code/zero-shot.py`` will override the previous answer file for its respective course. Make sure to save any previous outputs that you aren't redoing locally to avoid this.

### Just Codex:

On the MIT Courses:
```
python3 code/zero-shot.py --Codex=True --Do_Courses=True
```
On the MATH Benchmark:
```
python3 code/zero-shot.py --Codex=True --Do_MATH=True
```

### Just GPT-3 CoT:

On the MIT Courses:
```
python3 code/zero-shot.py --GPT3_CoT=True --Do_Courses=True
```
On the MATH Benchmark:
```
python3 code/zero-shot.py --GPT3_CoT=True --Do_MATH=True
```

### Codex, GPT-3, GPT-3 CoT, and Codex Explanation:

On the MIT Courses:
```
python3 code/zero-shot.py --Codex=True --GPT3_CoT=True --GPT3=True --Explain=True --Do_Courses=True
```
On the MATH Benchmark:
```
python3 code/zero-shot.py --Codex=True --GPT3_CoT=True --GPT3=True --Explain=True --Do_MATH=True
```
 
## 5. Evaluate Codex Responses
 
Open the CSV for each Course that looks like this: ``_Course_ results.csv``. Run each program and if it outputs the correct answer, put a 1 in the column titled ``Zero-Shot Evaluation``. If the program is incorrect, put a 0.
 
## 6. Few-shot(Codex, GPT-3 CoT)
 
### Just Codex Few-Shot:
 
On the MIT Courses:
```
python3 code/few-shot.py --Codex_Few_Shot=True --Do_Courses=True
```
On the MATH Benchmark:
```
python3 code/few-shot.py --Codex_Few_Shot=True --Do_MATH=True
```
### Just GPT-3 CoT Few-Shot:

On the MIT Courses:
```
python3 code/few-shot.py --GPT3_CoT_One_Shot=True --Do_Courses=True
```
On the MATH Benchmark:
```
python3 code/few-shot.py --GPT3_CoT_One_Shot=True --Do_MATH=True
```

