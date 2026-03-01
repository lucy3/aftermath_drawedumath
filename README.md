# Aftermath of DrawEduMath

This repository contains scripts and notebooks for recreating the results in a follow-up error analysis of 11 VLMs on DrawEduMath. 

Scripts used to update the DrawEduMath leaderboard can be found here: [https://github.com/allenai/DrawEduMath](https://github.com/allenai/DrawEduMath). 

### Code 

We have two key files in the `code` folder: 
- `small_labeling_tasks.py`: how we use an LM to conduct small data labeling tasks (as described in Appendix B in the paper)
- `aftermath.ipynb`: a walkthrough of how to reproduce the plots and numbers in our paper

### Data

Data can be found at: https://huggingface.co/collections/lucy3/aftermath-of-drawedumath

Inputs to `aftermath.ipynb` should be placed in the `data` folder: 
- Load model responses
  - `predictions.csv`: responses from evaluated VLMs
  - `answer_mapping.json`: outputs from an LM remapping teachers' answers around whether the student image contains any errors
  - `questions_to_categories.json`: question categories, e.g. image creation and medium, correctness & errors
- Redrawing experiment
  - `sampled_images_per_problem.json`: the filenames of images we redrew
  - `exp1_redrawn.csv`: model responses on redrawn images
  - 336 redrawn images, all `.png` 
- Textual support experiments
  - `exp2_nl.csv`: model responses when given teachers' descriptions
  - `exp2_testtime.csv`: model responses given their own descriptions
- Answer defaults analysis
  - `answer_comparisons.json`: ratings of answer pairs compared against each other
- Open-ended vs. binary error & correctness analysis
  - `question_binary.json`: outputs from an LM labeling whether a question is "binary" or "other" 
  - `binary_correctness.json`: outputs from an LM labeling whether student is correct/incorrect on binary questions

Contact `lucyli@cs.wisc.edu` with questions. 
