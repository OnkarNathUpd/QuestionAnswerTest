'''Naukri_txt=""
Naukri_skill_list=[]
with open("Naukri.txt","r") as fp1:
    Naukri_txt=fp1.readlines()
    fp1.close()
#print(Naukri_txt)
Naukri_txt=Naukri_txt[0]
Naukri_txt=Naukri_txt.replace("Jobs","\n")

with open("Naukri.txt","w") as fp1:
    fp1.writelines(Naukri_txt)
    fp1.close()'''

#if __name__ == '__SmallTestLogicCode__':

'''import re
statement = 'Please contact us at: support@datacamp.com'
date=' I worked from 12/2009 to 12/2010'
match = re.search(r'([\w\.-]+)@([\w\.-]+)', statement)
match =re.search(r'[0-9]/[0-9]',date)
if statement:
  print("Email address:", match.group()) # The whole matched text
  #print("Username:", match.group(1)) # The username (group 1)
  #print("Host:", match.group(2)) # The host (group 2)'''