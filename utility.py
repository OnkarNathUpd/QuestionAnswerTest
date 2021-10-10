def remove_puctuation(inp_str):
    punctuations = '''!()-[]{};:'"\,–◘○◙•‣⁃<>./?@#$%^&*_~'''

    no_punc = ""
    for char in inp_str:
        if char not in punctuations:
            no_punc = no_punc + char

    return no_punc

