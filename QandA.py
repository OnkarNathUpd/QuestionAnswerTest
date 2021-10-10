import random
import pandas

from UI import *

Question_text=""
Answer_text=""

easy_question_list = []
medium_questions_list = []
difficult_question_list = []

keywords_in_answers=[]

num_of_easy_q_attempted = 0
num_of_medium_q_attempted = 0
num_of_difficult_q_attempted = 0
attempted_question_list = []

total_num_q_to_candidate = 10

max_num_of_easy_question_to_be_asked = 6
max_num_of_medium_question_to_be_asked = 2
max_num_of_difficult_question_to_be_asked = 2

def get_QandA_constraint_values():

    return total_num_q_to_candidate,\
           max_num_of_easy_question_to_be_asked,\
           max_num_of_medium_question_to_be_asked,\
           max_num_of_difficult_question_to_be_asked

def evaluation_question(absolute_index=False,answer_given="",index=0,category=''):

    offset=0

    if absolute_index==False:
        if category=='Easy':
            offset=0
        if category=='Medium':
            offset=len(easy_question_list)
        if category=='Difficult':
            offset=len(easy_question_list)+len(medium_questions_list)
        qb_idx = offset + index
    else:
        qb_idx = index

    keywords=keywords_in_answers[qb_idx]
    print('keywords :',keywords)

    keywords=str(keywords).split(',')
    total_key_word=int(len(keywords))
    key_words_found_in_answer=0
    keyword_list_found_in_answer=[]
    for skill in keywords:
        if skill.lower() in answer_given.lower():
            key_words_found_in_answer+=1
            keyword_list_found_in_answer.append(skill)

    print("Total keywords for answers :",keywords)
    print("Keywords found in answers : ",keyword_list_found_in_answer)
    print("Total keywords :",total_key_word,"Found Keywords :",key_words_found_in_answer)

    score=0.0
    score=float(key_words_found_in_answer)/float(total_key_word)
    print("Score : ",score)

    if score>=0.60:
        return True
    else:
        return False

def get_question_randomly_from_list(category):

    offset=0
    qb_idx=0

    if category=='Easy':
        offset=0
        rand_id = random.randint(0, len(easy_question_list)-1)
        qb_idx = offset + rand_id
        print("offset,qb_idx,rand_id", offset, qb_idx, rand_id)
        return qb_idx, easy_question_list[rand_id], keywords_in_answers[qb_idx]
    if category=='Medium':
        offset=len(easy_question_list)
        rand_id = random.randint(0, len(medium_questions_list)-1)
        qb_idx = offset + rand_id
        print("offset,qb_idx,rand_id", offset, qb_idx, rand_id)
        return qb_idx, medium_questions_list[rand_id], keywords_in_answers[qb_idx]
    if category=='Difficult':
        offset=len(easy_question_list)+len(medium_questions_list)
        rand_id = random.randint(0, len(difficult_question_list)-1)
        qb_idx = offset + rand_id
        print("offset,qb_idx,rand_id",offset,qb_idx,rand_id)
        return qb_idx, difficult_question_list[rand_id], keywords_in_answers[qb_idx]

def ask_level_wise_question(no_of_q_attempt,start_index,last_index,q_list,max_num_q,category):
    attempted_question_list=[]
    print("no_of_q_attempt,start_index,last_index,q_list,max_num_q")
    print(no_of_q_attempt,start_index,last_index,q_list,max_num_q)
    global total_num_q_to_candidate
    while (no_of_q_attempt < max_num_q and total_num_q_to_candidate>0 ):
        random_index = random.randint(start_index, last_index)
        while (random_index in attempted_question_list):
            random_index = random.randint(start_index, last_index)
        print("\n Random index found :", random_index)
        attempted_question_list.append(random_index)

        print(q_list[random_index])
        update_question_text(q_list[random_index])
        answer = input("\n Answer the above question :")

        if evaluation_question(answer,random_index,category) == True:
            print("\n Answered matched for question :", random_index)
            no_of_q_attempt += 1
        else:
            print("\n Question not answered properly")

        total_num_q_to_candidate -= 1
        print("Number of remaining questions :",total_num_q_to_candidate)

    if total_num_q_to_candidate:
        total_num_q_to_candidate -= 1
    print("\n total_num_q_to_candidate :",total_num_q_to_candidate)



def ask_question():
    start_index=0
    print("Easy Questions")
############### Easy Questions ###################
    ask_level_wise_question(
        num_of_easy_q_attempted,
        start_index,
        (len(easy_question_list)- 1),
        easy_question_list,
        max_num_of_easy_question_to_be_asked,
        'Easy'
    )
    if total_num_q_to_candidate > 0:
    ############### Medium Questions ###################
        ask_level_wise_question(
            num_of_medium_q_attempted,
            start_index,
            (len(medium_questions_list) - 1),
            medium_questions_list,
            max_num_of_medium_question_to_be_asked,
            'Medium'
        )

############### Difficult Questions ###################
    if total_num_q_to_candidate > 0:
        ask_level_wise_question(
            num_of_difficult_q_attempted,
            start_index,
            (len(difficult_question_list) - 1),
            difficult_question_list,
            max_num_of_difficult_question_to_be_asked,
            'Difficult'
        )

def question_to_candidate(skill_set):
    different_skill=str(skill_set).split()
    for skill in different_skill:
        ml_df = pandas.read_excel('QuestionBank.xlsx', sheet_name=skill)

    print(ml_df.columns)
    print(ml_df.head(5))
    num_of_row=int(ml_df.shape[0])
    global easy_question_list
    global medium_questions_list
    global difficult_question_list
    global keywords_in_answers

    keywords_in_answers=ml_df["KeyWords"]
    print(keywords_in_answers)
    #return


    for row in range(num_of_row):
        if ml_df['Category'][row]=='Easy':
            easy_question_list.append(ml_df['Question'][row])
        if ml_df['Category'][row]=='Medium':
            medium_questions_list.append(ml_df['Question'][row])
        if ml_df['Category'][row]=='Difficult':
            difficult_question_list.append(ml_df['Question'][row])
    print(easy_question_list)
    print(len(easy_question_list))
    print(difficult_question_list)
    print(len(difficult_question_list))

    #first_window()

    ask_question()

def question_data_base_initilization(skill_set):
    different_skill=str(skill_set).split()
    for skill in different_skill:
        ml_df = pandas.read_excel('QuestionBank.xlsx', sheet_name=skill)

    print(ml_df.columns)
    print(ml_df.head(5))
    num_of_row=int(ml_df.shape[0])
    global easy_question_list
    global medium_questions_list
    global difficult_question_list
    global keywords_in_answers

    keywords_in_answers=ml_df["KeyWords"]
    print(keywords_in_answers)
    #return


    for row in range(num_of_row):
        if ml_df['Category'][row]=='Easy':
            easy_question_list.append(ml_df['Question'][row])
        if ml_df['Category'][row]=='Medium':
            medium_questions_list.append(ml_df['Question'][row])
        if ml_df['Category'][row]=='Difficult':
            difficult_question_list.append(ml_df['Question'][row])
    print(easy_question_list)
    print(len(easy_question_list))
    print(difficult_question_list)
    print(len(difficult_question_list))

