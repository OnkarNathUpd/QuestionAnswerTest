import enchant
from nltk.corpus import words
import enchant
import re
import pandas as pd
from utility import *

from docx import Document
#from ExtractSkills import check_skills
import nltk
import glob
import re


# Importing NLTK for sentence tokenizing
from nltk.tokenize import sent_tokenize


list_of_words=[]

def count_words(item):
    count=0
    for w in list_of_words:
        if w==item:
            count+=1
    return count

def check_skills(file):
    df = pd.read_csv("Skills.csv")
    skills = df.Skills
    print(skills)

    resume_content=[]
    with open(file,"r") as fp:
        resume_content=fp.readlines()
    skill_file_name=file.replace(".txt","_skill.txt")
    fp.close()

    d = enchant.Dict("en_US")

    for line in resume_content:
        line=remove_puctuation(line)
        line=line.split()

        line = " ".join(w.lower() for w in line)
        print(line)

        for common_skill in skills:
            if common_skill.lower() in line:
                print("$$$$$$$$$$$$$$$$$$$$      Common >>> ",common_skill)
                list_of_words.append(common_skill.lower())
        line=line.split()

        line=" ".join(w for w in line if d.check(w)!=True )
        temp=line.split()
        for w in temp:
            list_of_words.append(w.lower())
        print(">>>>>>>>>>>"+line)

    new_dic={w:count_words(w) for w in list_of_words}
    print(new_dic)
    count_list=[]

    for key,value in new_dic.items():
        count_list.append(value)

    count_list.sort(reverse=True)
    print(count_list)
    with open(skill_file_name,"w") as fp_skill:
        i=0
        while(i<(len(count_list)-1)):
            for key,value in new_dic.items():
                try:
                    if count_list[i]==value:
                        if(i<(len(count_list)-1)):
                            i += 1
                            if value > 0:
                                fp_skill.writelines(key + " : " + str(value) + "\n")
                except IndexError:
                    print("The wrong index value is :",i," Count list len is :",len(count_list))
                    break

    fp_skill.close()

nltk.download('punkt')

def getDocxContent(filename):
    doc = Document(filename)
    fullText = ""
    for para in doc.paragraphs:
        fullText += para.text
        fullText += "\n"
    return fullText

def parse_resume_for_skills(path):
    resume=path
    resume_path=resume
    resume = getDocxContent(resume_path)
    sentences = sent_tokenize(resume)
    if ".docx" in resume_path:
        resume_text=resume_path.replace(".docx",".txt")
    elif ".doc" in resume_path:
        resume_text = resume_path.replace(".doc", ".txt")

    with open(resume_text,"w") as fp:
        for sentence in sentences:
            try:
                fp.writelines(sentence)
            except:
                print()
            else:
                fp.writelines("\n")
    fp.close()

    # Check and Frequency of Skills

    check_skills(resume_text)

    # Check the skills year wise
    arrange_skill_year_wise(resume_text)

def arrange_skill_year_wise(file_path):
    file_content=[]

    with open(file_path,"r") as fp:
        file_content=fp.readlines()
    fp.close()
    df=pd.read_csv("Skills.csv")
    skill_list=df.Skills
    skill_map_file_name=file_path.replace(".txt","_mapped_sk.txt")
    new_dic_mapping_year_skill={}
    #6 bool start_adding_skills=False
    year = ''
    match=""
    skills = []
    with open(skill_map_file_name,"w") as fs:
        for line in file_content:
            try:
                match = re.findall(r'\d{4}', line)
                if match:
                    if str(match) != year:
                        new_dic_mapping_year_skill[year] = skills
                        skills.clear()


                    #start_adding_skills
                    print("Matched  :",match)
                    fs.writelines("\n-------------"+str(match)+"---------------\n")
                    year=str(match)
            except:
                pass

            for w in skill_list:
                if w in line:
                    skills.append(w)
                    fs.writelines(w+" ")
            print(skills)


        fs.close()
        print(new_dic_mapping_year_skill)

