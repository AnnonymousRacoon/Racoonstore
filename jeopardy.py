import pandas as pd
import re

# In order to disply the full contents of a column, we’ve added this line of code to the top of your file
pd.set_option('display.max_colwidth', -1)
jeopardy = pd.read_csv('jeopardy.csv')


# remove leading whitespace if it existis
for column in jeopardy.columns:
    jeopardy = jeopardy.rename(columns = {column : column[1:]} if column[0] == ' ' else {})
    

# get change values to floats
jeopardy.Value = jeopardy.Value.apply(lambda x: float(x[1:].replace(',','')) if x != "None" else 0)


# ----FUNCTIONS______

# filters string for keywords, returns true if it 
# finds all/any of the keywords. Default is all
# will search for plurals
def filter(keywords,string,all_or_any =True,_isin = False):
    string = string.lower()
    results = []
    search = None
    for word in keywords:
        
        if _isin:
            # also searches for words within words
            pattern = "({word}".format(word = word.lower())
        else:
            # use regex to allow for leading and trailing whitespaces, endpoints, non-letter characters, and plurals
            if word[-1] in ['s','x','z'] or word[-2:] in ['ss','sh','ch']:
                pattern = "([\W]|^){word}(\'|(es)?[\W]|$|(es)?$)".format(word = word.lower())
            else:
                pattern = "([\W]|^){word}(\'|s?[\W]|$)".format(word = word.lower())
        search = re.search(pattern, string)
        
        # if word could already be plural check for singulars
        if search is None and word[-2:] == "es":
            pattern = "([\W]|^){word}(\'|[\W]|$)".format(word = word[:-2].lower())
            search = re.search(pattern, string)
        elif search is None and word[-1:] == "s":
            pattern = "([\W]|^){word}(\'|[\W]|$)".format(word = word[:-1].lower())
            search = re.search(pattern, string)

        results.append(True if search is not None else False)
    # taylor output for searching for all or any of the keywords
    if all_or_any:
        return all(results)
    else:
        return any(results)

# fucntion to test filter
def filter_test(keywords,string,all_or_any = True,_isin = False):
    success = filter(keywords,string,all_or_any,_isin)
    if success:
        print('its a match!')
    else:
        print('these keywords do not match')

# calcultates unique answers by keyword/s
# Takes keywords as a list and data frame 
# Will not print by default
def uniqans_by_keywords(df,keywords,printVals = False):
    Qs = df[df['Question'].apply(lambda string: filter(keywords,string))].reset_index()
    QVals = Qs.Answer.value_counts()
    if printVals:
        print('Unique answers by keyword/s{}:\n'.format(keywords))
        print(QVals)
    return QVals

# calcultates the average difficulty for a question by keyword/s
# Takes keywords as a list and data frame 
# Will print average by default
def difficulty_by_keywords(df,keywords,printAvg = True):
    Qs = df[df['Question'].apply(lambda string: filter(keywords,string))].reset_index()
    if printAvg:
        print('\nThe average difficulty for questions including the keyword/s {ws} is: {mean}\n{x} questions match this combination of keywords.\n'.format(ws = keywords,mean = Qs.Value.mean(), x = len(Qs)))

    return Qs.Value.mean()




# -----TESTS_________

# # test filter func
# filter_test(['king','england'],'Popular Saint-Exupery character waiting around to become king of England\'s')
# filter_test(['king','england'],'Popular Saint-Exupery character waiting around to become England\'s king\'s of England\'s')
# filter_test(['trusses','england'],'truss england')
# filter_test(['blitz','tax','marsh'],'we collect taxes to protect the marshes from blitzes')

# # test difficulty_keywords
# difficulty_by_keywords(jeopardy,['king'],True)
# difficulty_by_keywords(jeopardy,["king","england"],True)

# # test uniqans
# uniqans_by_keywords(jeopardy,['king'],False)
# uniqans_by_keywords(jeopardy,["king","england"],True)



# ------TRIVIA GAME________
Trivia = raw_input("It's Trivia Time!\nDo You Want To Play?\n[Y/N]")
if Trivia.lower() == 'y':
    print("okay, let's play...")
    change = raw_input("You can search questions by topic\nDo you want to do this?\n[Y/N]")
    if change.lower() != 'y':
        pass
    else:
        subj = raw_input("search questions by keyword:")
        # fill question bank
        Qs = jeopardy[jeopardy['Question'].apply(lambda string: filter([subj],string))].reset_index()
        difficulty_by_keywords(jeopardy,[subj],True)
    # Qs = question bank
    Qs = jeopardy
    playing = 1
    while playing:
        

        # get random rows
        row = Qs.sample(n=1).reset_index()

        # Q&A
        print(row.Question.to_string())
        answer = raw_input('Answer: ')
        if answer.lower() == row.Answer.to_string():
            print('Correct!')
        else:
            print('Unlucky\nThe anser was: {}'.format(row.Answer.to_string()))
        
        # play again?
        Cont = raw_input("To play again [Y]\nTo change topics[C]\nTo quit any other key")
        if Cont.lower() == 'y':
            pass
        elif Cont.lower() == 'c':
            subj = raw_input("search questions by keyword:")
            # fill question bank
            Qs = jeopardy[jeopardy['Question'].apply(lambda string: filter([subj],string))].reset_index()
            difficulty_by_keywords(jeopardy,[subj],True)
        else:
            break
        
    
            








