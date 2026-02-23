from turtle import pd
from openai import OpenAI 
import os
import json
from tqdm import tqdm
from collections import Counter, defaultdict
from pathlib import Path
import pandas as pd
import random
import csv

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(prompt):
    return client.chat.completions.create(
                model="gpt-5-mini", # gpt-5-mini-2025-08-07
                messages=[{"role": "user", "content": prompt}],
            )

def error_detection(): 
    '''
    Uses a smaller LM to classify whether an answer indicates the student made an error or not.
    '''
    with open('../data/common_ans.json', 'r') as infile: 
        common_ans = json.load(infile) # {answer : count}

    common_ans = Counter(common_ans)

    answer_mapping = {}
    for ans, count in tqdm(common_ans.most_common()):
        prompt = f"When asked about what errors a student makes in their response to a math problem, a teacher writes, '{ans}'. Based on the teacher's feedback, does the student make any error? Respond 'yes' or 'no'."
        response = ''
        for i in range(5): 
            response = completion_with_backoff(prompt)
            response = response.choices[0].message.content.strip().lower()
            if response.startswith('yes') or response.startswith('no'): 
                break
        answer_mapping[ans] = response

    with open('../data/answer_mapping.json', 'w') as outfile:
        json.dump(answer_mapping, outfile)

def map_to_question_cat(question_to_category, q): 
    q = q.strip()
    if q.startswith('What errors does the student make in their response?'): 
        q = 'What errors does the student make in their response?'
    return question_to_category[q]

def binary_questions(): 
    '''
    Uses a smaller LM to classify whether a question is binary (yes/no) or open-ended.
    '''
    print(os.environ.get("OPENAI_API_KEY", ""))
    
    question_cat_file = Path.cwd().parent / "data" / "question_to_category_second.json"
    with open(question_cat_file, 'r') as infile:
        question_to_category = json.load(infile)

    qa = set()
    for q in question_to_category: 
        cat = map_to_question_cat(question_to_category, q)
        if cat.strip() == 'Correctness and errors': 
            qa.add(q)

    random.seed(0)
    qa = list(qa)
    random.shuffle(qa)
    
    if os.path.exists('../data/question_binary.json'):
        with open('../data/question_binary.json', 'r') as infile:
            question_mapping = json.load(infile)
    else:
        question_mapping = {}

    print("Questions done so far:", len(question_mapping))
    print("Total questions to process:", len(qa))

    question_count = 0
    for question in tqdm(qa): 
        if question in question_mapping:
            continue
        prompt = f"Is the following question a binary question that asks whether a student does something correctly or not?\nQuestion: '{question}'\nDecide whether the question above is a binary question that judges a student's correctness. Your response should start with 'Yes' or 'No':"
        response = ''
        for i in range(5): 
            response = completion_with_backoff(prompt)
            response = response.choices[0].message.content.strip().lower()
            if response.startswith('yes') or response.startswith('no'): 
                break
        if response.startswith('yes'):
            response = 'binary'
        else: 
            response = 'other'
        question_mapping[question] = response
        question_count += 1
        if question_count % 20 == 0:
            with open('../data/question_binary.json', 'w') as outfile:
                json.dump(question_mapping, outfile) 

    with open('../data/question_binary.json', 'w') as outfile:
        json.dump(question_mapping, outfile)

def is_student_correct():
    '''
    Given a binary question and a gold answer, ask whether the student is
    correct or not into a simple answer format of "correct" or "incorrect".
    '''
    with open('../data/question_binary.json', 'r') as infile:
        question_binary = json.load(infile)

    if os.path.exists('../data/binary_correctness.json'):
        with open('../data/binary_correctness.json', 'r') as infile:
            question_mapping = json.load(infile)
            question_mapping = defaultdict(dict,question_mapping)
    else:
        question_mapping = defaultdict(dict)

    qa = []
    with open('../data/drawedumath_all_qa.csv', 'r') as infile: 
        reader = csv.DictReader(infile)
        for row in reader: 
            question = row['Question'].strip()
            if question not in question_binary:
                continue
            if question in question_binary and question_binary[question] != 'binary': 
                continue
            answer = row['Answer'].strip()
            qa.append((question, answer))

    question_count = 0
    for question, answer in tqdm(qa): 
        if question in question_mapping and answer in question_mapping[question]:
            continue
        lower_answer = answer.lower()
        if lower_answer.startswith('correct'):
            response = 'correct'
        elif lower_answer.startswith('incorrect'):
            response = 'incorrect'
        else: 
            response = ''
            prompt = f'Teacher A is examining a student\'s solution to a math problem. Teacher B asks Teacher A, \'{question}\'\nTeacher A says, \'{answer}\'.\nDoes this exchange indicate that the student\'s solution has an error? Respond "yes" or "no":'
            for i in range(5): 
                response = completion_with_backoff(prompt)
                response = response.choices[0].message.content.strip().lower()
                if response.startswith('yes') or response.startswith('no'): 
                    break
            if response.startswith('no'):
                response = 'correct'
            else: 
                response = 'incorrect' 
        question_mapping[question][answer] = response
        if question_count % 20 == 0:
            with open('../data/binary_correctness.json', 'w') as outfile:
                json.dump(question_mapping, outfile) 
        question_count += 1

    with open('../data/binary_correctness.json', 'w') as outfile:
        json.dump(question_mapping, outfile)

if __name__ == "__main__":
    is_student_correct()