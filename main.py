from QandA import *
#from UI import *
from ExtractSkills import *

if __name__ == '__main__':
    question_to_candidate("ML")

    '''   line="Silicon Valley Bank, Tempe, AZ	04/2019 – 03/2020 sep 2020"
       match=re.findall(r'\d {4}',line)
       print(match)'''
'''    for path in glob.iglob("resumes/*.*", recursive=True):
            if ".docx" in path:
                print(path)
                parse_resume_for_skills(path)
                break'''


