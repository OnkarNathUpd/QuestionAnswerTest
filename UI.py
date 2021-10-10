import QandA
import tkinter as tk
from tkinter import filedialog
from ExtractSkills import *
from threading import Thread
from time import sleep

###############  GLOBAL VARIABLES #############################

typed_answer_provided = ""
question_counter_label=""
asked_question_list = []
resume_path = ""
question_text_label = ""
answer_text_label = ""
labelResumePath = ""
labelKeySkills = ""
score_label=""
tot_q = 0
max_easy = 0
max_medium = 0
max_difficult = 0
no_easy_attempted = 0
no_medium_attempted = 0
no_difficult_attempted = 0
latest_answer_key_skills = ""
latest_index = 0
latest_category = 0
total_correct_answer=0
maximum_question=0


##########################################################
def on_change(e):
    global typed_answer_provided
    typed_answer_provided = e.widget.get()


def c_open_file(root):
    rep = filedialog.askopenfile(initialdir=r"C:\Users\91957\PycharmProjects\ReadingResumes\resumes")
    print(rep.name)
    return rep.name


def browse_resume():
    global resume_path
    resume_path = c_open_file(screen)
    print("Resume location :", resume_path)
    labelResumePath.config(text=resume_path)


def parse_resume():
    parse_resume_for_skills(resume_path)

    skill_set_path = resume_path.replace(".docx", "_skill.txt")
    skillPathContent = []
    with open(skill_set_path, 'r') as fp:
        skillPathContent = fp.readlines()

    # Taking only top 10 skills as per expertise

    skill_string = ""
    line = ""
    # for i in range(0, len(skillPathContent)):
    for i in range(0, 4):
        line = skillPathContent[i].split(':')
        skill_string += (str(line[0]) + "\n")

    labelKeySkills.config(text=skill_string)


def update_question_text(qtext):
    global question_text_label
    question_text_label.config(text=qtext)

input_entry_typed_answer=""

def submit_answer_data():
    global latest_answer_key_skills
    print(" Submitted answer : ",input_entry_typed_answer.get())
    answer_given = input_entry_typed_answer.get()
    #input_entry_typed_answer.delete(0, 'end')
    input_entry_typed_answer.config(state='disabled')
    keywords = latest_answer_key_skills
    print('keywords :', keywords)

    keywords = str(keywords).split(',')
    total_key_word = int(len(keywords))
    key_words_found_in_answer = 0
    keyword_list_found_in_answer = []
    for skill in keywords:
        if skill.lower() in answer_given.lower():
            key_words_found_in_answer += 1
            keyword_list_found_in_answer.append(skill)

    print("Total keywords for answers :", keywords)
    print("Keywords found in answers : ", keyword_list_found_in_answer)
    print("Total keywords :", total_key_word, "Found Keywords :", key_words_found_in_answer)

    score = 0.0
    score = float(key_words_found_in_answer) / float(total_key_word)
    print("Score : ", score)

    if score >= 0.60:
        global total_correct_answer
        total_correct_answer+=1
        return True

    else:
        return False


def next_question():
    global no_easy_attempted
    global no_medium_attempted
    global no_difficult_attempted
    global latest_answer_key_skills
    global tot_q
    global maximum_question

    q_no= 0
    question=""
    keyword_list=[]

    if tot_q==0:
        global no_easy_attempted
        global no_medium_attempted
        global no_difficult_attempted
        total_q_attempted = no_easy_attempted + no_medium_attempted + no_difficult_attempted
        score = float(total_correct_answer / maximum_question)
        score_label.config(text=f"End of Test !!! "
                                f"\n Score : {score}  {total_correct_answer}/{maximum_question}"
                                f"\n Total questions attempted {total_q_attempted}")

    input_entry_typed_answer.config(state='normal')
    input_entry_typed_answer.delete(0, 'end')
    question_counter_label.config(text=str(tot_q)+"/10")

    if no_easy_attempted <(max_easy-0) and tot_q>0:
        q_no, question, keyword_list = QandA.get_question_randomly_from_list('Easy')
        while True:
            if q_no in asked_question_list:
                q_no, question, keyword_list = QandA.get_question_randomly_from_list('Easy')
                continue
            else:
                break

        no_easy_attempted += 1
        update_question_text(question)
        asked_question_list.append(q_no)
        latest_answer_key_skills=keyword_list
        #latest_index=

        tot_q-=1

        return

    if no_medium_attempted < max_medium and tot_q>0:
        q_no, question, keyword_list = QandA.get_question_randomly_from_list('Medium')
        while True:
            if q_no in asked_question_list:
                print("Repeated questions")
                q_no, question, keyword_list = QandA.get_question_randomly_from_list('Medium')
                continue
            else:
                break
        no_medium_attempted +=1
        update_question_text(question)
        asked_question_list.append(q_no)
        latest_answer_key_skills = keyword_list
        tot_q -=1
        return

    if no_difficult_attempted < max_difficult and tot_q>0:
        q_no, question, keyword_list = QandA.get_question_randomly_from_list('Difficult')
        while True:
            if q_no in asked_question_list:
                q_no, question, keyword_list = QandA.get_question_randomly_from_list('Difficult')
                continue
            else:
                break
        no_difficult_attempted +=1
        update_question_text(question)
        asked_question_list.append(q_no)
        latest_answer_key_skills = keyword_list
        tot_q -=1
        return


def update_answer_text(atext):
    global answer_text_label
    answer_text_label.config(text=atext)


def start_test():
    global asked_question_list
    global no_easy_attempted
    global latest_answer_key_skills
    global tot_q
    print("In Start test")
    q_no, question, latest_answer_key_skills = QandA.get_question_randomly_from_list('Easy')
    no_easy_attempted = +1
    update_question_text(question)
    asked_question_list.append(q_no)
    tot_q -= 1


testprocedure_window = ""


def end_test():
    #testprocedure_window.destroy()
    global no_easy_attempted
    global no_medium_attempted
    global no_difficult_attempted
    total_q_attempted=no_easy_attempted+no_medium_attempted+no_difficult_attempted
    score = float(total_correct_answer / maximum_question)
    score_label.config(text=f"End of Test !!! "
                            f"\n Score : {score}  {total_correct_answer}/{maximum_question}"
                            f"\n Total questions attempted {total_q_attempted}")


def create_testing_window(window):
    global testprocedure_window
    testprocedure_window = window

    global question_counter_label
    question_counter_label = tk.Label(window, text="10/10")
    question_counter_label.grid(row=0, column=0)

    question_voice_play_button = tk.Button(window, text="⏵", font='sans 16 bold', relief="raised")
    question_voice_play_button.grid(row=0, column=1)

    question_voice_pause_button = tk.Button(window, text="⏸", font='sans 16 bold')
    question_voice_pause_button.grid(row=0, column=2)

    question_voice_repeat_button = tk.Button(window, text="⟲", font='sans 16 bold')
    question_voice_repeat_button.grid(row=0, column=3)

    remaining_timer_label = tk.Label(window, text="10:00 mins")
    remaining_timer_label.grid(row=0, column=4)

    label_question = tk.Label(window, text="Question(Audio Format)")
    label_question.grid(row=1, column=1, columnspan=3)

    back_button = tk.Button(window, text="⇦", font='sans 16 bold')
    back_button.grid(row=2, column=0)

    global question_text_label
    question_text_label = tk.Label(window, text="                      \n                      ", borderwidth=2,
                                   relief="sunken")
    question_text_label.grid(row=2, column=1, columnspan=3, sticky='ew')

    next_button = tk.Button(window,text='⇨', font='sans 16 bold',command=next_question)#)
    next_button.grid(row=2, column=4)

    answer_voice_record_button = tk.Button(window, text="⏺", font='sans 16 bold')
    answer_voice_record_button.grid(row=3, column=1)

    answer_voice_pause_button = tk.Button(window, text="⏸", font='sans 16 bold')
    answer_voice_pause_button.grid(row=3, column=2)

    answer_voice_repeat_button = tk.Button(window, text="⟲", font='sans 16 bold')
    answer_voice_repeat_button.grid(row=3, column=3)

    answer_text_label1 = tk.Label(window, text='Answer (Audio Format)')
    answer_text_label1.grid(row=4, column=1, columnspan=3)

    global answer_text_label
    answer_text_label = tk.Label(window, text="                      \n                      ", borderwidth=2,
                                 relief="sunken")
    answer_text_label.grid(row=5, column=1, columnspan=3, sticky='ew')

    answer_type_format = tk.Label(window, text="You may type answer below")
    answer_type_format.grid(row=6, column=1, columnspan=3, sticky='ew')

    global input_entry_typed_answer
    input_entry_typed_answer = tk.Entry(window, text="answer")
    input_entry_typed_answer.grid(row=7, columnspan=4, sticky='ew')
    #input_entry_typed_answer.bind("<Return>", on_change)


    submit_answer = tk.Button(window, text="Submit",command=submit_answer_data)
    submit_answer.grid(row=7, column=4)

    test_start_button = tk.Button(window, text='StartTest', command=start_test)
    test_start_button.grid(row=8, column=0)

    test_pause_button = tk.Button(window, text='Pause Test')
    test_pause_button.grid(row=8, column=2)

    test_end_button = tk.Button(window, text='End Test', command=end_test)
    test_end_button.grid(row=8, column=4)

    global total_correct_answer
    global score_label
    score_label=tk.Label(text="")
    score_label.grid(row=9,column=1)


screen = ""


def start_test_procedure():
    global screen
    global tot_q
    global max_easy
    global max_medium
    global max_difficult
    global maximum_question
    screen.destroy()

    QandA.question_data_base_initilization("ML")

    tot_q,max_easy ,max_medium , max_difficult = QandA.get_QandA_constraint_values()
    maximum_question=tot_q

    test_window = tk.Tk()

    test_window.minsize(width=300, height=300)
    test_window.title("Test")

    create_testing_window(test_window)
    # time.sleep(2)
    test_window.mainloop()


def first_window():
    global screen
    screen = tk.Tk()
    screen.title("Audio Round Test")
    screen.minsize(width=500, height=200)

    label_welcome_message = tk.Label(text="Hello !, \n Welcome to the test")
    label_welcome_message.grid(row=0, column=1)

    label_insruction = tk.Label(text="Upload your resume")
    label_insruction.grid(row=3, column=0)

    button_upload_resume = tk.Button(text="Upload", command=browse_resume)
    button_upload_resume.grid(row=3, column=1)

    labelResume = tk.Label(text="Path:")
    labelResume.grid(row=4, column=0)

    global labelResumePath
    labelResumePath = tk.Label(text="")
    labelResumePath.grid(row=4, column=1)

    buttonParseResume = tk.Button(text="Parse Resume", command=parse_resume)
    buttonParseResume.grid(row=5, column=1)

    global labelKeySkills
    labelKeySkills = tk.Label("")
    labelKeySkills.grid(row=6, column=1)

    labelKS = tk.Label(text="Top Key Skills")
    labelKS.grid(row=6, column=0)
    buttonStartTest = tk.Button(text="Start Test", command=start_test_procedure)
    buttonStartTest.grid(row=7, column=2)

    screen.mainloop()


if __name__ == '__main__':
    first_window()
