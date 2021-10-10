import pandas as pd

if __name__ =='main':
    ml_df = pd.read_excel('QuestionBank.xlsx', sheet_name='ML')
    print(ml_df.head(5))
