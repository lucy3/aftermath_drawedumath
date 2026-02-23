# Aftermath of DrawEduMath

This repository contains scripts and notebooks for recreating the results in a follow-up error analysis of 11 VLMs on DrawEduMath. 

Scripts used to update the DrawEduMath leaderboard can be found here: [https://github.com/allenai/DrawEduMath](https://github.com/allenai/DrawEduMath). 

### Code 

We have two key files in the `code` folder: 
- `small_labeling_tasks.py`: how we use an LM to conduct small data labeling tasks (as described in Appendix B in the paper)
- `aftermath.ipynb`: a walkthrough of how to reproduce the plots and numbers in our paper

### Data

Inputs to `aftermath.ipynb` should be placed in the `data` folder: 
- Load model responses
  - `pred_subset.csv`: responses from evaluated VLMs
  - `answer_mapping.json`: a mapping to determine whether the student image contains any errors
  - `questions_to_categories.json`: question categories, e.g. image creation and medium, correctness & errors
- Redrawing experiment
  - `sampled_images_per_problem.json`
  - `exp1_redrawn.csv`
- Textual support experiments
  - `exp2_nl.csv`
  - `exp2_testtime.csv`
- Answer defaults analysis
  - `answer_comparisons.json`
- Open-ended vs. binary error & correctness analysis
  - `binary_correctness.json`
  - `question_binary.json`

Guidance on how to download data is forthcoming. In the meantime, contact `lucyli@cs.wisc.edu` with questions. 
