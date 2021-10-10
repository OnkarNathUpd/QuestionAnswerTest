from docx import Document
from ExtractSkills import check_skills
import nltk
import enchant
from nltk.corpus import words
import enchant

import pandas as pd


nltk.download('punkt')

df=pd.read_csv("Skills.csv")

skills=df.Skills

print(skills)

def remove_puctuation(inp_str):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    no_punc = ""
    for char in inp_str:
        if char not in punctuations:
            no_punc = no_punc + char

    return no_punc

list_of_words=[]
def check_skills(file):
    resume_content=[]
    with open(file,"r") as fp:
        resume_content=fp.readlines()
    skill_file_name=file.replace(".txt","_skill.txt")
    fp.close()

    d = enchant.Dict("en_US")

    for line in resume_content:
        line=remove_puctuation(line)
        print(line)

        for common_skill in skills:
            if common_skill in line:
                print("$$$$$$$$$$$$$$$$$$$$      Common >>> ",common_skill)
                list_of_words.append(common_skill)

        line=line.split()


        line=" ".join(w for w in line if d.check(w)!=True )
        temp=line.split()
        for w in temp:
            list_of_words.append(w.lower())
        print(">>>>>>>>>>>"+line)
        #fp_skill.writelines(line+"\n")
    #fp_skill.close()

    #print(list_of_words)

    def count_words(item):
        count=0
        for w in list_of_words:
            if w==item:
                count+=1
        return count



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


resume=input("Enther the resume that needs to be parsed :")

def getDocxContent(filename):
    doc = Document(filename)
    fullText = ""
    for para in doc.paragraphs:
        fullText += para.text
        fullText+="\n"
    return fullText

resume_path="resumes/"+resume

resume = getDocxContent(resume_path)

# Importing NLTK for sentence tokenizing
from nltk.tokenize import sent_tokenize

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

check_skills(resume_text)

