#KakaaoTalk Conversation Analyzer

#import python modules

#for date and time analysis
from datetime import datetime
#for frequency analysis
from collections import Counter
#for graphical analysis
import turtle

def Introduction():
    '''
        Introduces user to the program
    '''
    print('Welcome, this is the <KakaoTalk Conversation Analyzer> program')
    print('This program will analyze your KakaoTalk conversation with your friend')
    print('Please use PC (not mobile) to open the KakaoTalk coversation you wish to analyze')
    print('Then, click <chat settings>, <storage management>, and <save> to export all data')
    print('Export the data file as a .txt file and place in the same folder as this program')
    print('Once all this is done, you are ready\n')

def OpenFile():
    '''
        Prompts for and opens input file
    '''
    #init
    input_file_opened = False
    attempts = 5
    
    #prompt for file name and attempt to open files until successful
    while (not input_file_opened) and (attempts > 0):
        try:
            if not input_file_opened:
                conversation_file = str(input('Enter input file name (.txt file): '))
                input_file = open(conversation_file, 'r')
                input_file_opened = True
        except IOError:
            print('<',conversation_file, '> file not found. Please re-enter')
            attempts -= 1
            print(attempts, 'attempts left\n')

    #terminate or continue program
    if not input_file_opened:
        raise IOError('Too many attempts. Please restart the program.')
    else:
        return conversation_file

def GetNames():
    '''
        Prompts for user and friend names
    '''
    #prompt for names
    my_name = str(input('Enter your name as saved in your conversation file: '))
    friend_name = str(input("Enter your friend's name as saved in your conversation file: "))
    return (my_name, friend_name)

def FilesNameAssignment(my_name,friend_name):
    '''
        Forms file names for user and friend
    '''
    #create file names by adding .txt at the end of names
    my_file = my_name + '.txt'
    friend_file = friend_name + '.txt'
    return (my_file, friend_file)

def Extractconvo(conversation_file, my_file, friend_file, my_name, friend_name):
    '''
        Extracts conversation contents to create a file each for user and friend
    '''
    #open input file and form a specific string to use as condition in the next step
    input_file = open(conversation_file,'r')
    lines = input_file.readlines()
    me = my_name + '","'
    friend = friend_name + '","'
    
    #extract my chat
    with open(my_file, 'w') as mychat:
        for line in lines:
            if me in line:
                line = line.split(',')[0] + ',' + line.split(',')[2]
                line = line.replace('"','')
                mychat.write(line)
    
    #extract friend chat
    with open(friend_file, 'w') as friendchat:
        for line in lines:
            if friend in line:
                line = line.split(',')[0] + ',' + line.split(',')[2]
                line = line.replace('"','')
                friendchat.write(line)
    
    #close files
    input_file.close()
    mychat.close()
    friendchat.close()

def SetParameter():
    '''
        Prompts for time period to be analyzed
    '''
    #prompt for start and finish date
    start_date = str(input('Enter start date of period you wish to analyze (YYYY-MM-DD): '))
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date
    finish_date = str(input("Enter finish date of period you wish to analyze (YYYY-MM-DD): "))
    finish_date = datetime.strptime(finish_date, "%Y-%m-%d")
    print('\nThe length of given period is',(finish_date - start_date).days, 'days')
    
    #alter my file according to parameter
    mychat = open(my_file, 'r')
    lines = mychat.readlines()
    with open(my_file, 'w') as mychat:
        for line in lines:
            line_date_time = line.split(',')[0]
            line_date = line_date_time.split(' ')[0]
            line_date = datetime.strptime(line_date, "%Y-%m-%d")
            difference1 = (line_date - start_date).days
            difference2 = (finish_date - line_date).days
            if (difference1 >= 0) and (difference2 >= 0):
                mychat.write(line)
    mychat.close()
    print('\nA new file containing all texts you sent has been created')
    
    #alter friend file according to parameter
    friendchat = open(friend_file, 'r')
    lines = friendchat.readlines()
    with open(friend_file, 'w') as friendchat:
        for line in lines:
            line_date_time = line.split(',')[0]
            line_date = line_date_time.split(' ')[0]
            line_date = datetime.strptime(line_date, "%Y-%m-%d")
            difference1 = (line_date - start_date).days
            difference2 = (finish_date - line_date).days
            if (difference1 >= 0) and (difference2 >= 0):
                friendchat.write(line)
    friendchat.close()
    print("A new file containing all texts your friend sent has been created\n")
    
    return (start_date, finish_date)

def ArrangeData(my_file, friend_file):
    '''
        Places all words spoken by each person in respective lists
    '''
    #forms empty lists
    my_words = []
    friend_words = []

    #extract spoken words from line and remove '\n' for words at the end of each line
    mychat = open(my_file, 'r')
    line = mychat.readline()
    for line in mychat:
        #Get words
        my_words_in_single_line = line.split(',', 1)[1]
        my_words_in_single_line = my_words_in_single_line.split(' ')
        for k in range(0,len(my_words_in_single_line)):
            my_words.append(my_words_in_single_line[k])
        my_words = [str.replace('\n', '') for str in my_words]

    #extract spoken words from line and remove '\n' for words at the end of each line
    friendchat = open(friend_file, 'r')
    line = friendchat.readline()
    for line in friendchat:
        #Get words
        friend_words_in_single_line = line.split(',', 1)[1]
        friend_words_in_single_line = friend_words_in_single_line.split(' ')
        for k in range(0,len(friend_words_in_single_line)):
            friend_words.append(friend_words_in_single_line[k])
        friend_words = [str.replace('\n', '') for str in friend_words]

    return (my_words, friend_words)

def TimeDictionary(my_file, friend_file):
    '''
        Places hours in list for easier analysis
    '''
    #form empty list
    talk_time = []
    
    #my time
    with open(my_file, 'r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            #Get time
            talk_time_in_single_line = line.split(',')[0]
            talk_line_time = talk_time_in_single_line.split(' ')[1]
            talk_line_hour = int(talk_line_time.split(':')[0])
            talk_time.append(talk_line_hour)
    #friend time
    with open(friend_file, 'r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            #Get time
            talk_time_in_single_line = line.split(',')[0]
            talk_line_time = talk_time_in_single_line.split(' ')[1]
            talk_line_hour = int(talk_line_time.split(':')[0])
            talk_time.append(talk_line_hour)

    return talk_time

def NumberofLines(my_file, friend_file, my_name, friend_name):
    '''
        Counts total number of texts for each person
    '''
    #form a sub_function to avoid repetition
    def CountingLines(file_name, speaker):
        '''
            Counts and prints the total number of texts
        '''
        #find total number of texts
        input_file = open(file_name,'r')
        line = input_file.readline()
        num_lines = 0
        for line in input_file:
            num_lines += 1
        input_file.close()
        print(speaker, 'sent', num_lines, 'texts in total')

    #sub_main
    CountingLines(my_file, my_name)
    CountingLines(friend_file, friend_name)

def CommonWordsAnalyzer(my_words, friend_words):
    '''
        Analyzes the most common words spoken by each person
    '''
    #prompt for how many most frequenty used words user wishes to find
    x = int(input('\nEnter value of x for which you wish to find the top x most frequently used words: '))
    
    #analyze my conversation
    my_words = Counter(my_words)
    my_most_common_words = list(my_words.most_common(x))
    
    #analyze friend conversation
    friend_words = Counter(friend_words)
    friend_most_common_words = list(friend_words.most_common(x))

    #print my result
    for i in range(0, x):
        word = my_most_common_words[i][0]
        frequency = my_most_common_words[i][1]
        print('Your top', int(i+1), 'most commonly used word is <', word, '> and it was used <', frequency, '> times')
    
    #print friend result
    for j in range(0, x):
        word = friend_most_common_words[j][0]
        frequency = friend_most_common_words[j][1]
        print("Your friend's top", int(j+1), 'most commonly used word is <', word, '> and it was used <', frequency, '> times')
    
    return (my_most_common_words, friend_most_common_words)

def WordFrequencyCounter(my_words, friend_words):
    '''
        Analyzes how many times the input word is spoken by each person
    '''
    #init
    terminate = False

    #repeat until break while loop
    while not terminate:
        inputword = input('\nEnter the word of which you wish to find its frequency: ')
        inputword_frequency_me = my_words.count(str(inputword))
        inputword_frequency_friend = friend_words.count(str(inputword))
        print('You used <', inputword, '>', inputword_frequency_me, ' times')
        print('Your friend used <', inputword, '>', inputword_frequency_friend, ' times')

        #prompt for command to retry or terminate
        response = input('\nDo you wish to enter another word? Press any key to retry or <n> to quit')
        if response == 'n':
            terminate = True
            print('Word Frequency Counter terminated\n')

def ActiveTimeTracker(talk_time):
    '''
        Analyzes the hourly activity of conversation and shows result on barchart
    '''
    def CountHours(talk_time):
        '''
            Adds hour and its frequency to dictionary
        '''
        #add time and its frequency to dictionary
        time = {}
        for a in range(0, 24):
            hour_frequency = talk_time.count(int(a))
            time[str(a)] = int(hour_frequency)

        return time

    def DrawBar(t, height):
        '''
            Creates barchart of the analyzed result
        '''
        #start filling shape
        t.begin_fill()
        t.left(90)
        t.forward(height)
        t.right(90)
        #start writing the data value on top of the column
        t.forward(20)
        t.penup()
        t.left(90)
        t.forward(2)
        t.pendown()
        t.write(str(height), align = "center")
        t.penup()
        t.right(180)
        t.forward(2)
        t.left(90)
        #writing the data value stopped
        t.pendown()
        t.forward(20)
        t.right(90)
        t.forward(height)
        #start writing the group name on the bottom of the column
        t.penup()
        t.right(90)
        t.forward(20)
        t.pendown()
        t.write(str(i)+'h', align = "center")
        t.penup()
        t.right(180)
        t.forward(20)
        t.pendown()
        #stop writing the group name on the bottom of the column
        #stop filling shape
        t.end_fill()                
 
    #sub_main

    #interpret talk time for use in turtle mode
    time = CountHours(talk_time)
    all_values = time.values()
    maxheight = max(all_values)
    numbers = len(time)
    border = 10
  
    #set turtle mode window
    window = turtle.Screen()
    window.title('Talk Activity Graph')
    window.setworldcoordinates(0 - border, 0 - border, 40 * numbers + border, maxheight + border)
    window.bgcolor("white")
  
    #create pen and fix options
    pen = turtle.Turtle()
    pen.color("black")
    pen.fillcolor("gray")
    pen.pensize(3)
    pen.speed(100000)
    pen.hideturtle()

    #run function
    for i in time:
        DrawBar(pen, time[i])

    #explain result
    print('This is a barchart of at what hours in the day the texts were sent')
    print('The numbers on the bottom of the bars indicate the hours in the day')
    print('The numbers on the top of the bars indicate the data value\n')
    print('Click screen to exit graph\n')

    #exit turtle mode on click
    window.exitonclick()

def Outro():
    '''
        Thanks user for using program
    '''
    print('Thank you for using the "KakaoTalk Conversation Analyzer"')


# ----- main -----

#program welcome and introduction
Introduction()

#obtain names and making files
conversation_file = OpenFile()
my_name, friend_name = GetNames()
my_file, friend_file = FilesNameAssignment(my_name,friend_name)

#process data
Extractconvo(conversation_file, my_file, friend_file, my_name, friend_name)
start_data, finish_date = SetParameter()
my_words, friend_words = ArrangeData(my_file, friend_file)
talk_time = TimeDictionary(my_file, friend_file)

#analyze and present results
NumberofLines(my_file, friend_file, my_name, friend_name)
my_most_common_words, friend_most_common_words = CommonWordsAnalyzer(my_words, friend_words)
WordFrequencyCounter(my_words, friend_words)
ActiveTimeTracker(talk_time)

#outro
Outro()

