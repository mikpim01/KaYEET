#  __  ___      ___   ____    ____  _______  _______ .___________.
# |  |/  /     /   \  \   \  /   / |   ____||   ____||           |
# |  '  /     /  ^  \  \   \/   /  |  |__   |  |__   `---|  |----`
# |    <     /  /_\  \  \_    _/   |   __|  |   __|      |  |     
# |  .  \   /  _____  \   |  |     |  |____ |  |____     |  |     
# |__|\__\ /__/     \__\  |__|     |_______||_______|    |__|     
#
#   Made by Josh Boag


#---------------------Editing Guidelines!---------------------
# Frames are assigned to the 'self.master' using .pack()
# Elements inside Frames are assigned to parents using .grid()
# The grid function is for assigning elements to specfic columns and rows for a window
#
# All elements and variables are stored in the QuizGUI class
# New Elements must be assigned to a frame with an unused grid coordinate (eg. column=2, row=3)
# A new element will only be shown when the frame is active (e.g either Homescreen, Quiz, Finish, Quiz Creator)
# If you want to display an element across all frames then you must add that element to each frame
#
# Any function inside the QuizGUI class that is leading with 'self.' can be accessed by any other class function.
# Variables that don't lead with 'self.' cannot be accessed within the QuizGUI class
#
# Encapsulation is used for the Quiz questions so users can't cheat using the console to print out the dictionary

# Install Dependencies 
from tkinter import *           # Import tkinter
#from tkinter import ttk        # Import tkk for special elements
import tkinter as tk            # Import tk for special elements
from tkinter import font        # Import Fonts for custom fonts that arn't natively supported in tkinter
from tkinter import filedialog  # Import filedialog for 'open' files in current or external directories
import os,json,glob             # Import os for getting the filepath, get json for diction loading and exporting, Glob for file finding in current directory
from PIL import ImageTk         # Import Python Image Library to open .png files

# When called, the Questions class converts an entire file (".YEET") to a Python Dictionary.
# This is a faster method than individually appending a value to each key in a dictionary
class Questions:
    def __init__(self, **entries): # Initalize the class
        self.__dict__.update(entries) # Add all values to a class dictionary
        
class QuizGUI: # The entire programs main class
    def __init__(self, master): # 
        self.master=master # Defines the objects binding class
        self.home() # Runs the starting homescreen. This is a function due to the fact it needs to be run mulitiple times (After finishing a Quiz / After Creating a Quiz)

# Homescreen #

    def home(self):  # Homescreen Function 
        # Defines the homescreen frame (That will hold all the Homescreen buttons and other visual elements)
        self.homescreen = tk.Frame(self.master, background='#F0F0F0')
        self.homescreen.pack(expand=True, fill='both', side='right')

        # Homescreen Configure
        # Define the rules of all the grid dimensions
        # Uniform means they are symetrical either side
        # Weight defines the proportiate dimensions of a frame. Weight with a value of 2 will mean it is proportionally twice the size of a weight value of 1.
        self.homescreen.grid_columnconfigure(0, weight=1,uniform="yes")
        self.homescreen.grid_columnconfigure(1, weight=1,uniform="yes")
        self.homescreen.grid_columnconfigure(2, weight=1,uniform="yes")
        self.homescreen.grid_rowconfigure(1, weight=0,uniform="yes")
        self.homescreen.grid_rowconfigure(2, weight=2,uniform="yes")
        self.homescreen.grid_rowconfigure(3, weight=0,uniform="yes")
        self.homescreen.grid_rowconfigure(4, weight=1,uniform="yes")

        # Title Element
        # Full width due to the spanning over 3 columns and being sticky to the West and East
        self.title = Label(self.homescreen, text="KaYEET", bg="#46178f", fg="white",font=('Helvetica Neue',24,"bold"),wraplength=700,pady=5)
        self.title.grid(row=0,column=0,sticky="we",columnspan=3)

        # Meta Variable and Label
        # Stores variable for the Meta Data of the selected Quiz file. Stores Author and the amount of Quiz Questions, the variable changes when a new file is selected
        # Meta label is the element in which the meta variable is displayed
        self.metaVar= StringVar(self.master)
        self.meta = Label(self.homescreen, textvar=self.metaVar, bg="lightgrey", fg="Black",font=('Helvetica Neue',14,"normal"),wraplength=700,pady=10)
        self.meta.grid(row=1,column=0,sticky="we",columnspan=3)
        
        # Selected File Variable and Label
        # 'selectedFileVar' stores the string value of the Quiz name for the selected Quiz file
        # 'selectedFile' is the label element that gets put on the homescreen that displays the selectedFileVar
        self.selectedFileVar= StringVar(self.master)
        self.selectedFileVar.set("Select a Built-in Quiz or click 'Open' to Play your Own")
        self.selectedFile = Label(self.homescreen, textvar=self.selectedFileVar, bg="lightgrey", fg="Black",font=('Helvetica Neue',14,"normal"),wraplength=700,pady=10)
        self.selectedFile.grid(row=3,column=0,sticky="we",columnspan=3) # Full Width 

        # Browse Quiz Listbox
        # Listbox ('browseQuiz') displays the quizes in the programs directory. 
        self.browseQuiz = Listbox(self.homescreen,bg="lightgrey",fg="black",bd=1,height=2,font=("Montserrat",16),activestyle='none',borderwidth=0,relief="flat",highlightthickness=0) # Create listbox element.
        self.browseQuiz.grid(row=2, column=0, sticky="NWES",columnspan=3,padx=150,pady=10,rowspan=1,ipady=10,ipadx=10)
        self.scrollbar = tk.Scrollbar(self.browseQuiz) # Attaches a scrollbar to the listbox if there are too many items to be displayed in a single view
        self.scrollbar.pack( side = RIGHT, fill = Y ) # Place element on frame
        for file in glob.glob("*.YEET"): # Find .YEET quiz files in current directory
            self.browseQuiz.insert(END,file.split(".")[0]) # Insert found Quiz Files into the Listbox
        self.browseQuiz.bind('<<ListboxSelect>>', self.selectQuiz) # Bind <<ListboxSelect>> to a function which deals with a item being selected
        self.browseQuiz.config(yscrollcommand=self.scrollbar.set) # Bind Scrollbar to Listbox
        self.scrollbar.config(command=self.browseQuiz.yview) # Bind Scrollbar to Listbox

        # Homescreen Button styling
        self.buttonWidth=20 # <-
        self.buttonHeight=2 #   | Defines the dimensions of all the Homescreen Buttons. This was used so I didn't have to change each dimension individually when developing
        self.buttonPadY=10  # <-
        self.buttonFont= font.Font(family="Montserrat", size=16, weight='bold') # Defines a font to be used for each of the homescreen buttons

        # Create the button elements to be displayed on the homescreen.
        #
        # Buttons:
        #       - Start  - Starts the quiz. By default, the button is disabled until a Quiz is 'Opened' or selected from the browseQuiz listbox
        #       - Open  - Opens a filedialog where a .YEET file can be selected if not already found by the browseQuiz Listbox
        #       - Create - Opens a new page where a user can create their own quizes
        #
        # Due to the way I have programmed the columns, each button will be centered evenly in thirds (Minus the X axis padding)
        self.button1 = tk.Button(self.homescreen, text = 'Start',state=DISABLED, command = self.startQuiz,relief="flat", bg="#c01733",fg="white",width=self.buttonWidth,height=self.buttonHeight,font=self.buttonFont)
        self.button1.grid(row=4,column=0,pady=self.buttonPadY)
        self.button2 = tk.Button(self.homescreen, text = 'Open', command = self.fileExplore,relief="flat", bg="#c01733",fg="white",width=self.buttonWidth,height=self.buttonHeight,font=self.buttonFont)
        self.button2.grid(row=4,column=1,pady=self.buttonPadY)
        self.button3 = tk.Button(self.homescreen, text = 'Create',command=self.createQuiz,relief="flat", bg="#c01733",fg="white",width=self.buttonWidth,height=self.buttonHeight,font=self.buttonFont)
        self.button3.grid(row=4,column=2,pady=self.buttonPadY)

    # Select Quiz
    # The listbox ONLY has Quizes that have been found with the .YEET file extension. Because of this, we can be confident that the Quiz file exists and is in the valid format
    # If a Quiz has been selected using the Listbox, this function opens the file and gets its meta data for display e.g Author, quiz questions 
    def selectQuiz(self,other):
        self.button1.config(state=NORMAL) # The quiz can start if the button is normal i.e can be clicked
        try:
            self.filename=str(self.browseQuiz.get(self.browseQuiz.curselection())+".YEET") # Find the file with the extension .YEET
        except: # Can't find the file
            self.selectedFileVar.set("File Not Found") # Display Error message
            self.button1.config(state=DISABLED) # Disable Button
            pass # Return to previous function
        
        self.meta= (json.load(open(str(self.browseQuiz.get(self.browseQuiz.curselection())+".YEET")))) # Load file
        self.metaVar.set("Made by: "+self.meta['meta']['author']+"\tQuestions: "+str(self.meta['meta']['length'])) # Present the meta data found in Quiz File
        self.selectedFileVar.set("Selected: "+str(self.browseQuiz.get(self.browseQuiz.curselection()))) # Present the Quiz name in selectedFile element

    # Opens up a file dialog to find .YEET files that arn't already found in this python files immediate directory
    def fileExplore(self):
        self.metaVar.set("")            # <-| Reset variables so nothing is displayed while the filedialog is open
        self.selectedFileVar.set("")    # <-|
        self.browseQuiz.selection_clear(0,END) # Clears selection of the listbox

        # The filedialog box can only open files with the extension .YEET. It is unlikely that there are other files with the same extension so we can safely assume it is valid
        self.filename = filedialog.askopenfilename(initialdir = str(os.getcwd())+"/tests",title = "Select KaYEET Quiz file",filetypes = [("KaYEET Quiz Files","*.YEET"),("Legacy KaYEET Quiz Files","*.json")]) # Calls the file dialog box
        if self.filename: # If a valid file is selected
            print("File Selected:",self.filename)
            self.meta= (json.load(open(str(self.filename))))
            self.metaVar.set("Made by: "+self.meta['meta']['author']+"\tQuestions: "+str(self.meta['meta']['length'])) # Present the meta data found in Quiz File
            self.selectedFileVar.set("Selected: "+str(self.filename)) # Present the Quiz name in selectedFile element
            self.button1.config(state=NORMAL) # Make the 'start' button clickable
        else:
            print("No File Selected")
            self.button1.config(state=DISABLED) # Make the 'start' button unclickable so you can't start a quiz without questions etc
            self.selectedFileVar.set("No File Selected! Try Again or Select a Quiz Above!") # Display this message in selectedFile element

# Quiz Window #
    # When the start button is clicked
    # The start button can only hold one command, but multiple need to be run. This function intializes all those startup functions
    # This function is reused after Quiz create or the results page
    def startQuiz(self):
        self.browseQuiz.destroy() # Destroys the homescreen
        self.clearMaster() # Destroys any other elements that were in the master object

        # This is an encapsulated variable (Private variable), meaing it cannot be called from outside this function
        # This variable holds the entire quiz dictionary
        # This is a faster method than individually appending a value to each key in a dictionary
        self.__quiz= Questions(**(json.load(open(self.filename)))) # The filename is the file that was 'opened' or clicked on in the homescreen
        print("\n"*50,"\t"+str(self.__quiz.meta['title'])+"\t\tBy "+str(self.__quiz.meta['author'])+"\n"+"-"*55)
        self.preload() # Loads the values of the first question
        self.displayFrame() # Loads the
        self.default()

    # This function preloads all the variables and adds elements if they don't already exist
    # I used this function so the user can repeat/reset the quiz without loading an entirely new frame ontop of an existing frame
    def preload(self):
        self.sidebar = tk.Frame(self.master, width=200, bg='#F0F0F0', height=500, relief='sunken', borderwidth=0)
        self.sidebar.pack(expand=False, fill='both', side='left', anchor='nw')
        self.scrollbar = tk.Scrollbar(self.master) # Create scrollbar when the number of quizes exceeds the single view
        self.scrollbar.pack( side = LEFT, fill = Y )
        self.sidelist = Listbox(self.sidebar,height=700,width=15,bg="#F0F0F0",fg="#757515",font=("Montserrat",16),selectmode="tk.BROWSE",activestyle='none',borderwidth=0,relief="flat",highlightthickness=0)
        self.sidelist.pack(padx=5,pady=50) # Creates the listbox that items will be put in

        # Adds the dropdown menu with some basic functions
        self.menubar = Menu(self.master) # Binded to the master window
        self.master.config(menu=self.menubar)
        fileMenu = Menu(self.menubar,tearoff=0) # Creates new menu
        fileMenu.add_command(label="Restart Quiz", command=self.default)  # Resets the quiz to the first question
        fileMenu.add_command(label="Skip Question", command=self.skip)
        fileMenu.add_command(label="Finish Quiz", command=self.quizComplete)
        self.menubar.add_cascade(label="Options", menu=fileMenu) # Assigns the above functions under the Options menu
        quizmenu = Menu(self.master, tearoff=0) # Tearoff 0 means that the menu cannot be open in another mini window
        quizmenu.add_command(label="Debug", command=self.onExit)    # Stops the mainloop so the console be used
        quizmenu.add_command(label="Quiz by "+str(self.__quiz.meta['author']),state="disabled")
        self.menubar.add_cascade(label="About", menu=quizmenu)

        # Defines the variables and images before the main frame elements are placed
        # The images are similar to those found on Kahoot and are stored in the /images folder
        # The images are .png which isn't natively supported by tkinter, so PIL or Pillow (aka Python Image Library) is used to display .png images
        self.titlevar= StringVar(self.master) 
        self.errortitlevar= StringVar(self.master)
        self.choiceOneImg=PhotoImage(file="images/tri.png")
        self.choiceOneVar= StringVar(self.master)
        self.choiceTwoImg=PhotoImage(file="images/dia.png")
        self.choiceTwoVar= StringVar(self.master)
        self.choiceThreeImg=PhotoImage(file="images/cir.png")
        self.choiceThreeVar= StringVar(self.master)
        self.choiceFourImg=PhotoImage(file="images/squ.png")
        self.choiceFourVar= StringVar(self.master)

        # Adds "Question (num)" for each question in the quiz
        for i in range(1,int(self.__quiz.meta['length'])+1):
            self.sidelist.insert(END,"Question "+str(i))
            self.sidelist.bind('<<ListboxSelect>>', self.select) # Binds <<ListboxSelect>> (When user clicks an Item) to self.select function which gets and deals with selection
            self.sidelist.curselection()

        # Binds the scrollbar to the listbox
        self.sidelist.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.sidelist.yview)

        self.itemsPacked= False # To make sure that these items do not get loaded more than once
    
    # Loads the first values when a Quiz Starts or when reset
    def default(self):
        self.sidelist.selection_clear(0, END) # Clears the current selection of the listbox when reset
        self.sidelist.selection_set( first = 0 ) # Selects the first item (Question 1)
        self.titlevar.set(self.__quiz.questions["Q1"]['question'])
        self.choiceOneVar.set(self.__quiz.questions["Q1"]['choices'][0])
        self.choiceTwoVar.set(self.__quiz.questions["Q1"]['choices'][1])
        self.choiceThreeVar.set(self.__quiz.questions["Q1"]['choices'][2])
        self.choiceFourVar.set(self.__quiz.questions["Q1"]['choices'][3])
        self.__answersCorrect=[] # Resets the list of correct answers
        self.questionsAnswered=[] # Resets the list of questions the user has answered
        for i in range(1,int(self.__quiz.meta['length'])+1):    # <-| Adds all the questions to the listbox
            self.sidelist.itemconfig(i-1, {'fg': 'black'})      # <-|
        self.displayQuestion(self,1)    # Runs the displayQuestion function

    # This function will render the items on the frame
    # This frame is for when the user is answering questions (ie. the Question and the four multichoice answers)
    def displayFrame(self):
        if self.itemsPacked == False: # If items have not been rendered
            # KaYEET Title gets rendered before the frame so it appears at the top of the window
            self.title = Label(self.master, text="KaYEET", bg="#46178f", fg="white",font=('Helvetica Neue',24,"bold"),wraplength=700,pady=5)
            self.title.pack(fill="x")
            
            # Create a new frame that will store all the quiz elements
            # It is easier to delete a frame then it is to delete individual elements, thats why I used this method
            self.mainarea = tk.Frame(self.master, background='#F0F0F0', width=500, height=500)
            self.mainarea.pack(expand=True, fill='both', side='right')
            # Configure the grid of the frame
            self.mainarea.grid_columnconfigure(0, weight=1)
            self.mainarea.grid_columnconfigure(1, weight=1)

            # If the user selects a question that has already been answered, then a prompt will appear "You have already answered this question"
            # This element will display the 'errortitlevar' if the variable is .set()
            self.errortitle = Label(self.mainarea, textvar=self.errortitlevar, bg="#F0F0F0", fg="red",font=('Helvetica Neue',12,"bold"),wraplength=700,pady=5)
            self.errortitle.grid(row=0,column=0,sticky="we",columnspan=4)

            # The maintitle element is where the Question string will go
            maintitle = Label(self.mainarea, textvar=self.titlevar, bg="#F0F0F0", fg="black",font=('Helvetica Neue',18),wraplength=700,pady=5)
            maintitle.grid(row=1,column=0,sticky="we",columnspan=4)

            # This defines some basic styling so the multichoice buttons have consistency
            self.choiceFont = font.Font(family="Montserrat", size=24, weight='bold')
            self.choiceWidth= 350 # Button width
            self.choiceHeight= 200 # Button Height
            self.choicePadX= 10 # Distance between the edge of the button and edge of the column
            self.choicePadY= 10 # Distance between the edge of the button and edge of the row

            # All four multichoice buttons
            # Each button follows the styling of the above variables
            # Each button contains an image like that found on Kahoot
            # Each button is assigned to a different row and/or column. This means they don't overlap
            self.choiceOne = Button(self.mainarea,textvar=self.choiceOneVar,relief="flat", bg="#c01733",fg="white", wraplength=310,width=self.choiceWidth,height=self.choiceHeight, highlightcolor="red", font=self.choiceFont,command=lambda: self.answercheck(1))
            self.choiceOne.config(image= self.choiceOneImg, compound = LEFT,width=self.choiceWidth,height=self.choiceHeight,padx=10)
            self.choiceOne.grid(row=2,column=0,sticky="W",padx=self.choicePadX, pady=self.choicePadY)
            self.choiceTwo = Button(self.mainarea,textvar=self.choiceTwoVar,relief="flat",  bg="#1368ce",fg="white", wraplength=310, width=self.choiceWidth,height=self.choiceHeight, highlightcolor="red", font=self.choiceFont,command=lambda: self.answercheck(2))
            self.choiceTwo.config(image= self.choiceTwoImg, compound = LEFT,width=self.choiceWidth,height=self.choiceHeight,padx=10)
            self.choiceTwo.grid(row=2,column=1,sticky="W",padx=self.choicePadX, pady=self.choicePadY)
            self.choiceThree = Button(self.mainarea, textvar=self.choiceThreeVar,relief="flat",  bg="#d89e00", fg="white", wraplength=310,width=self.choiceWidth,height=self.choiceHeight, highlightcolor="red", font=self.choiceFont,command=lambda: self.answercheck(3))
            self.choiceThree.config(image= self.choiceThreeImg, compound = LEFT,width=self.choiceWidth,height=self.choiceHeight,padx=10)
            self.choiceThree.grid(row=4,column=0,sticky="W",padx=self.choicePadX, pady=self.choicePadY)
            self.choiceFour = Button(self.mainarea,image=self.choiceFourImg, textvar=self.choiceFourVar,relief="flat", bg="#298f0d",fg="white", wraplength=310, width=self.choiceWidth,height=self.choiceHeight, highlightcolor="red", font=self.choiceFont,command=lambda: self.answercheck(4))
            self.choiceFour.config(image= self.choiceFourImg, compound = LEFT,width=self.choiceWidth,height=self.choiceHeight,padx=10)
            self.choiceFour.grid(row=4,column=1,sticky="W",padx=self.choicePadX, pady=self.choicePadY)

            # The Skip button will skip the question to the next avaliable unanswered question
            # This button is assigned underneath the multichoice buttons to the left
            self.skip= Button(self.mainarea, text="Skip",relief="flat", bg="#46178f", fg="white", width=10,height=2, highlightcolor="red", font=("Montserrat", '12','bold'),command=self.skip)
            self.skip.grid(row=5,column=0,sticky="W",padx=self.choicePadX, pady=self.choicePadY)

            # The finish button will go straight to the results page
            # This button is assigned underneath the multichoice buttons to the right
            self.finish= Button(self.mainarea, text="Finish",relief="flat", bg="#46178f", fg="white", width=10,height=2, highlightcolor="red", font=("Montserrat", '12','bold'),command=self.quizComplete)
            self.finish.grid(row=5,column=1,sticky="E",padx=self.choicePadX, pady=self.choicePadY)

            self.itemsPacked= True # Make sure these elements don't get rendered again
        else:   # If these items have already been rendered, don't render them again. So the buttons don't appear twice
            pass

    # Hides the Homescreen when called
    def clearMaster(self):
        self.homescreen.pack_forget()

    # Quiz Listbox Select
    # When a listbox item is clicked, this function grabs the value of the selected item (e.g Question 2 grabs two despite the index being 3)
    # I didn't want to use the index method (starting at 0) because we are only working with numbers >= 1. I didn't want to complicate having to add +1 each time to my index
    def select(self,other):
        a = int(str(self.sidelist.get(self.sidelist.curselection())).split(" ")[1])
        self.displayQuestion(self,a) # Displays the question of the question number selected

    # If a question has already been answered then its buttons will be disabled
    def displayQuestion(self,other=None,Qnum=None): # If a number is parsed, then that number will be called to display
        self.displayFrame() # Make sure that the template is showing

        # This function will check if the question has already been answered
        if self.isDisabled() == True: # If question has been answered
            self.errortitlevar.set("You have already answered this Question!") # Display alert message
            # Disable each of the buttons so the answer cannot be modified
            # The questions answer is given imediately hence why it can't be changed
            self.choiceOne.configure(state=DISABLED)
            self.choiceTwo.configure(state=DISABLED)
            self.choiceThree.configure(state=DISABLED)
            self.choiceFour.configure(state=DISABLED)
        elif Qnum != None:  # If the question has not been answered, make the buttons clickable
            self.errortitlevar.set("") # Remove alert message if any
            self.choiceOne.configure(state=NORMAL)
            self.choiceTwo.configure(state=NORMAL)
            self.choiceThree.configure(state=NORMAL)
            self.choiceFour.configure(state=NORMAL)

        if Qnum == None:  # Get current question number
            Qnum= self.getval()

        # Displays the corresponding question and mutlichoice answers for a particular question
        # Qnum is either given or recieved through .getval()
        self.titlevar.set(self.__quiz.questions["Q"+str(Qnum)]['question'])
        self.choiceOneVar.set(self.__quiz.questions["Q"+str(Qnum)]['choices'][0])
        self.choiceTwoVar.set(self.__quiz.questions["Q"+str(Qnum)]['choices'][1])
        self.choiceThreeVar.set(self.__quiz.questions["Q"+str(Qnum)]['choices'][2])
        self.choiceFourVar.set(self.__quiz.questions["Q"+str(Qnum)]['choices'][3])

    # Stop mainloop so the console can be used
    def onExit(self):
        self.master.quit()

    # Gets the value of the current question
    def getval(self,other=None):
        try:
            return int(str(self.sidelist.get(self.sidelist.curselection())).split(" ")[1]) # Get question number from listbox
        except:
            pass    #else Returns 
            
    # Checks the answer to that given in the self.__quiz dictionary
    def answercheck(self,choice):
        getquestionnum= int(str(self.sidelist.get(self.sidelist.curselection())).split(" ")[1]) # Get question number from listbox
        answer= self.__quiz.questions["Q"+str(getquestionnum)]['answer'] # Get answer from corresponding question in the lisbox
        if answer == choice: # If the user selected answer is the same as found in the dictionary
            self.__answersCorrect.append(getquestionnum) # Append this question number to __answersCorrect variable
            print(str(getquestionnum)+": Correct") # Print question number and result
            self.sidelist.itemconfig(getquestionnum-1, {'fg': '#66bf39'}) # Change the curent sidebar listbox item to green
        else:
            print(str(getquestionnum)+": Incorrect") # Print question number and result
            self.sidelist.itemconfig(getquestionnum-1, {'fg': 'red'}) # Change the curent sidebar listbox item to red
        self.disableQuestion() # Disable the question for the future
        self.next() # go to the next question

    # Check if the current question is disabled
    # This returns either true or false
    def isDisabled(self):
        if self.getval() in self.questionsAnswered: # Checks if answer has been given in the questionsAnswered list
            return True
        else:
            return False

    # Appends the answered question to questionsAnswered list
    def disableQuestion(self):
        self.questionsAnswered.append(self.getval())
        self.displayQuestion() # Disables question from being answered twice

    # This function will go to te next avaliable question that is unanswered
    # If all questions are answered, then it will not skip to any questions
    def skip(self):
        if self.getval() == (int(self.__quiz.meta['length'])):  # If the question is the last value on the listbox list
            start=1 # Go back to the top of the listbox list
        else:
            start=self.getval() # else, get the current question
        # Go to the next unanswered question
        for i in range(start,int(self.__quiz.meta['length'])+1):
            if i not in self.questionsAnswered:
                if i == self.getval():
                    continue
                else:
                    self.displayQuestion(Qnum=i) # Display unanswered question
                    self.sidelist.selection_clear(0, END) # clear selection
                    self.sidelist.selection_set( first = i-1 ) # set selection to unanswered question
                    return
    # Next Question           
    # This works the same way as the above function except if all questions are answered, then it will automatically finish the quiz
    def next(self):
        if len(self.questionsAnswered) == int(self.__quiz.meta['length']): # If the question is the last value on the listbox list
            self.quizComplete() # Calls the function to end the quiz and display results
        if self.getval() == (int(self.__quiz.meta['length'])):
            start=1 # Go back to the top of the listbox list
        else:
            start=self.getval()
        for i in range(start,int(self.__quiz.meta['length'])+1):
            if i not in self.questionsAnswered:
                if i == self.getval():
                    continue
                else:
                    self.sidelist.selection_set( first = i-1 )
                    self.displayQuestion(Qnum=i) # Display unanswered question
                    self.sidelist.selection_clear(0, END)
                    self.sidelist.selection_set( first = i-1 )
                    return

# Results Page #

    # When the quiz is complete, this runs a new screen which displays statistics           
    def quizComplete(self):
        self.menubar.destroy()          # <-
        self.sidebar.pack_forget()      #   | Deletes current frames
        self.scrollbar.pack_forget()    #   |
        self.mainarea.pack_forget()     # <-

        # Creates new frame that results will be assigned to
        self.finishFrame= tk.Frame(self.master,width=500, height=500, bg='#F0F0F0', relief='sunken', borderwidth=0)
        self.finishFrame.pack()

        # Displays message plus the score if greater than 0
        self.finishText= StringVar(self.master)
        finishTitle= Label(self.finishFrame, textvar=self.finishText, bg="#F0F0F0", fg="black",font=('Helvetica Neue',24),wraplength=700,pady=10)
        finishTitle.pack(fill='x')

        # A bar graph is drawn which shows the correct and wrong answers
        # The variables below define the dimensions of the graph
        c_width = 600  # Canvas width
        c_height = 340 # Canvas height
        c_linewidth=4 # Underline width
        c_padY=c_width/10  # Defines padding
        c_padX=c_width/10 # Defines padding
        c_barwidth=c_width/3 # Defines the width of the bars

        c = Canvas(self.finishFrame, width=c_width, height=c_height,bd=0) # Displayed on a new canvas
        c.pack()

        # Get local variables for correct and wrong answers
        # Unanswered questions are considered wrong
        correct= len(self.__answersCorrect)
        wrong=int(self.meta['meta']['length'])- correct

        # Calculate the bar height value, the calculation is proportionate to each other and the height of the canvas
        graphY1=((c_height/(correct+wrong)))*correct
        graphY2=((c_height/(correct+wrong)))*wrong

        # Based on the questions answered and answers correct, will a the message and graph output be different
        # If no questions are answered
        if len(self.questionsAnswered) == 0:
            #print("No Questions Answered")
            self.finishText.set("Uhm, did you even try?!") # Displayed message
            graphY1= c_padX+5
            graphY2= c_padX+5

        # If all questions are answered but none are correct
        elif len(self.__answersCorrect) == 0:
            self.finishText.set("Better Luck Nextime!") # Displayed message
            graphY1= c_padX+5
            graphY2= c_height-c_padX

        # If all questions are answered correctly
        elif len(self.__answersCorrect) == int(self.meta['meta']['length']):            
            #print("None Wrong")
            self.finishText.set("Congratulations!\nYou Scored: "+str(int((100/(correct+wrong))*correct))+"%") # Displayed message with percentage
            graphY1= c_height-c_padX
            graphY2= c_padX
            
        # if at least one question is answered
        elif len(self.questionsAnswered) != 0:
            #print("Normal")
            if (100/(correct+wrong))*correct > 50:
                self.finishText.set("Well Done!\nYou Scored: "+str(int((100/(correct+wrong))*correct))+"%") # Displayed message with percentage
            elif (100/(correct+wrong))*correct > 30:
                self.finishText.set("Good Effort!\nYou Scored: "+str(int((100/(correct+wrong))*correct))+"%") # Displayed message with percentage

        # Draws the bar graph based on forementioned bar graph variables
        c.create_rectangle(c_padX, c_height-graphY1, c_barwidth+c_padX, c_height-c_padY, fill="green",outline="green")
        c.create_text(c_padX+(c_barwidth/2), c_height-graphY1-(c_padY/2), text="Correct: "+str(correct),font=('Helvetica Neue',16,"bold"))
        c.create_rectangle((c_padX*2)+c_barwidth, c_height-graphY2, c_barwidth*2+c_padX*2, c_height-c_padY, fill="red",outline="red")
        c.create_text((c_padX*2)+(c_barwidth*1.5), c_height-graphY2-(c_padY/2), text="Wrong: "+str(wrong),font=('Helvetica Neue',16,"bold"))
        c.create_line(0, c_height-c_padY, c_width, c_height-c_padY,width=4) # Draws underline

        # Display a button that when clickedgoes to the homescreen
        self.resetHome= Button(self.finishFrame, text="Home",relief="flat", bg="#46178f", fg="white", width=10,height=2, highlightcolor="red", font=("Montserrat", '12','bold'),command=self.resetAll)
        self.resetHome.pack()

        print("-"*55,"\n\tCorrect: "+str(correct)+"\t\tIncorrect: "+str(wrong))

    # This function destroys the results frame and other elements, then displays homescreen
    def resetAll(self):
        self.itemsPacked= False
        self.finishFrame.destroy()
        self.title.destroy()
        self.sidelist.destroy()
        self.home()
        
# KaYEET QuizCreator #

    # Display a new question or an existing question with the saved answers
    def createQuizListSelect(self,other):
        self.Qnum = int(str(self.createQuizList.get(self.createQuizList.curselection())).split(" ")[1]) # Gets Current Question
        # Tries to set question and multichoice answers to a value if already defined
        try:
            self.questionTitleVar.set(self.Quiz['questions']["Q"+str(self.Qnum)]['question'])
            self.entryOneVar.set(self.Quiz['questions']["Q"+str(self.Qnum)]['choices'][0])
            self.entryTwoVar.set(self.Quiz['questions']["Q"+str(self.Qnum)]['choices'][1])
            self.entryThreeVar.set(self.Quiz['questions']["Q"+str(self.Qnum)]['choices'][2])
            self.entryFourVar.set(self.Quiz['questions']["Q"+str(self.Qnum)]['choices'][3])
        # else set question and multichoice answers to intial values
        except:
            self.questionTitleVar.set("Insert Question Here")
            self.entryOneVar.set("")
            self.entryTwoVar.set("")
            self.entryThreeVar.set("")
            self.entryFourVar.set("")

    # Create a new quiz question
    def createQuizQuestion(self):
        # Can't create a new question if the current question is not completed properly
        if self.entryOneVar.get() == "" or self.entryTwoVar.get() == "" or self.entryThreeVar.get() == "" or self.entryFourVar.get() == "" or self.questionTitleVar.get() == "" or self.questionTitleVar.get() == "Insert Question Here":
            # Save the question to dictionary
            self.saveQuestion()
            return
        else:
            # else create a new question and display that question in the sidebar
            self.createdQuestions=self.createdQuestions+1
            self.Quiz['questions'].update({"Q"+str(self.createdQuestions):{}})
            self.createQuizList.insert(END,"Question "+str(self.createdQuestions))

    # This function defines the layout of the Quiz creator    
    def createQuiz(self):
        self.clearMaster()

        # Below is the creation of a new list and its default contents
        self.Quiz={} # New dictionary
        self.Quiz.update({'meta':{'author':"unknown","title":"unknown",'length':1}}) # Update dictionary to store default values
        self.Quiz.update({'questions':{'Q1':{}}}) # Create first question

        # Create sidebar with listbox that displays each question eg. Question 1, Question 2, Question 3 etc
        self.sidebar = tk.Frame(self.master, width=200, bg='#F0F0F0', height=500, relief='sunken', borderwidth=0)
        self.sidebar.pack(expand=False, fill='both', side='left', anchor='nw')
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.pack( side = LEFT, fill = Y )
        self.createQuizList = Listbox(self.sidebar,height=700,width=15,bg="#F0F0F0",fg="black",font=("Montserrat",16),selectmode="tk.BROWSE", exportselection=False,activestyle='none',borderwidth=0,relief="flat",highlightthickness=0)
        self.createQuizList.pack(padx=5,pady=50)

        # Set default lisbox value
        self.createQuizList.insert(END,"Question 1")
        self.createQuizList.bind('<<ListboxSelect>>', self.createQuizListSelect) # Bind the list item to createQuizListSelect()


        # set default values for the current question number
        self.createdQuestions=1
        self.Qnum=1

        # Create new frame that all elements will be assigned to
        self.mainarea = tk.Frame(self.master, background='#F0F0F0', width=500, height=500)
        self.mainarea.pack(expand=True, fill='both', side='right')

        # create header title
        self.title = Label(self.mainarea, text="KaYEET Quiz Creator", bg="#46178f", fg="white",font=('Helvetica Neue',24,"bold"),wraplength=700,pady=5)
        self.title.grid(row=0,column=0,sticky="we",columnspan=4)

        # Create save button which when pressed, will store the values placed in the entryboxes
        self.save= Button(self.mainarea, text="Save",relief="flat", bg="#46178f", fg="white", width=10,height=2, highlightcolor="red", font=("Montserrat", '12','bold'),command=self.saveQuestion)
        self.save.grid(row=1,column=1,sticky="E",padx=40, pady=10)

        # Create new question button which when pressed, will create a new question that the user can edit
        self.newQuestion= Button(self.mainarea, text="New Question",relief="flat", bg="#46178f", fg="white", width=15,height=2, highlightcolor="red", font=("Montserrat", '12','bold'),command=self.createQuizQuestion)
        self.newQuestion.grid(row=1,column=0,sticky="W",padx=40, pady=10)

        # Create error box if there are any areas, the user will be alerted
        self.errortitleVar= StringVar(self.master)
        self.errortitle = Label(self.mainarea, textvar=self.errortitleVar,relief="flat", bg="#F0F0F0", fg="red",font=('Helvetica Neue',12,"bold"),wraplength=400,pady=5)
        self.errortitle.grid(row=2,column=0,columnspan=4,sticky="EWN")

        # Displays the question that the user has [yet to] input
        self.questionTitleVar = StringVar(self.master)
        self.questionTitle = Entry(self.mainarea, textvar=self.questionTitleVar, bg="lightgrey", fg="black",font=('Helvetica Neue',18))
        self.questionTitle.grid(row=2,column=0,sticky="we",columnspan=4,padx=40,pady=40,ipady=5,ipadx=5)

        # Configure the grid layout, 
        self.mainarea.grid_columnconfigure(0, weight=1)
        self.mainarea.grid_columnconfigure(1, weight=1)
        self.mainarea.grid_rowconfigure(0, weight=0)
        self.mainarea.grid_rowconfigure(1, weight=0)
        self.mainarea.grid_rowconfigure(2, weight=0)
        self.mainarea.grid_rowconfigure(3, weight=2)
        self.mainarea.grid_rowconfigure(4, weight=2)
        self.mainarea.grid_rowconfigure(5, weight=1)

        # Radio buttons are used to store the answer on the corresponding question
        # This is easier to implement than a dropdown for example
        # Radio buttons by default can only have one option selected
        
        # Radio button next to entry boxes that store the multichoice answers
        # Each radio button and entry box is assigned to different parts of the grid
        self.setAnswerVar= tk.IntVar()
        self.setAnswerVar.set(1)
        self.setAnswer= tk.Radiobutton(self.mainarea,padx = 0, variable=self.setAnswerVar,value=1)
        self.setAnswer.grid(row=3,column=0,sticky="W")
        self.entryOneVar= StringVar(self.master)
        self.entryOne = Entry(self.mainarea,textvar=self.entryOneVar,relief="flat", bg="lightgrey",fg="black",font=('Helvetica Neue',16))
        self.entryOne.grid(row=3,column=0,sticky="NWES", pady=10,padx=40,ipady=5,ipadx=5)

        # Radio button next to entry boxes that store the multichoice answers
        self.setAnswer= tk.Radiobutton(self.mainarea,padx = 0, variable=self.setAnswerVar,value=2)
        self.setAnswer.grid(row=3,column=1,sticky="W")
        self.entryTwoVar= StringVar(self.master)
        self.entryTwo = Entry(self.mainarea,textvar=self.entryTwoVar,relief="flat", bg="lightgrey",fg="black",font=('Helvetica Neue',16))
        self.entryTwo.grid(row=3,column=1,sticky="NWES", pady=10,padx=40,ipady=5,ipadx=5)

        # Radio button next to entry boxes that store the multichoice answers
        self.setAnswer= tk.Radiobutton(self.mainarea,padx = 0, variable=self.setAnswerVar,value=3)
        self.setAnswer.grid(row=4,column=0,sticky="W")
        self.entryThreeVar= StringVar(self.master)
        self.entryThree = Entry(self.mainarea,textvar=self.entryThreeVar,relief="flat",bg="lightgrey",fg="black",font=('Helvetica Neue',16))
        self.entryThree.grid(row=4,column=0,sticky="NWES", pady=10,padx=40,ipady=5,ipadx=5)

        # Radio button next to entry boxes that store the multichoice answers
        self.setAnswer= tk.Radiobutton(self.mainarea,padx =0, variable=self.setAnswerVar,value=4)
        self.setAnswer.grid(row=4,column=1,sticky="W")
        self.entryFourVar= StringVar(self.master)
        self.entryFour = Entry(self.mainarea,textvar=self.entryFourVar,relief="flat", bg="lightgrey",fg="black",font=('Helvetica Neue',16))
        self.entryFour.grid(row=4,column=1,sticky="NWES", pady=10,padx=40,ipady=5,ipadx=5)

        # Radio button next to entry boxes that store the multichoice answers
        self.export= Button(self.mainarea, text="Export",relief="flat", bg="#46178f", fg="white", width=15,height=2, highlightcolor="red", font=("Montserrat", '12','bold'),command=self.export)
        self.export.grid(row=5,column=1,sticky="E",padx=40, pady=5)

    # Saves the question to a dictionary
    def saveQuestion(self):
        # Sets each entry background to default colour
        self.entryOne.config(bg="lightgrey")
        self.entryTwo.config(bg="lightgrey")
        self.entryThree.config(bg="lightgrey")
        self.entryFour.config(bg="lightgrey")
        self.questionTitle.config(bg="lightgrey")

        # These statements check that there is a value in each of the entry boxes
        if self.questionTitleVar.get() == "" or self.questionTitleVar.get() == "Insert Question Here":
            self.errortitleVar.set("Error! Please enter Question!") # Alert user that this entry is not valid
            self.questionTitle.config(bg="red") # Alert which entry contains the error
            return
        if self.entryOneVar.get() == "":
            self.errortitleVar.set("Error! Please enter a option value") # Alert user that this entry is not valid
            self.entryOne.config(bg="red") # Alert which entry contains the error
            return
        if self.entryTwoVar.get() == "":
            self.errortitleVar.set("Error! Please enter a option value") # Alert user that this entry is not valid
            self.entryTwo.config(bg="red") # Alert which entry contains the error
            return
        if self.entryThreeVar.get() == "":
            self.errortitleVar.set("Error! Please enter a option value") # Alert user that this entry is not valid
            self.entryThree.config(bg="red") # Alert which entry contains the error
            return
        if self.entryFourVar.get() == "":
            self.errortitleVar.set("Error! Please enter a option value") # Alert user that this entry is not valid
            self.entryFour.config(bg="red") # Alert which entry contains the error
            return
        # Store the question and question multichoice options in the dictionary
        self.Quiz['questions'].update({"Q"+str(self.Qnum):{'question':self.questionTitleVar.get()}})
        self.Quiz['questions']["Q"+str(self.Qnum)].update({'choices':[]})
        self.Quiz['questions']["Q"+str(self.Qnum)].update({'answer':self.setAnswerVar.get()})
        self.Quiz['questions']["Q"+str(self.Qnum)]['choices'].append(self.entryOneVar.get())
        self.Quiz['questions']["Q"+str(self.Qnum)]['choices'].append(self.entryTwoVar.get())
        self.Quiz['questions']["Q"+str(self.Qnum)]['choices'].append(self.entryThreeVar.get())
        self.Quiz['questions']["Q"+str(self.Qnum)]['choices'].append(self.entryFourVar.get())
        self.errortitleVar.set("") # Clear errortitle
            
    # Exports dictionary to .YEET file
    # Users need to create a quiz that has at least 3 questions
    def export(self):
        self.saveQuestion() # Save question if not done already
        if self.createdQuestions < 3:
            self.errortitleVar.set("Error! Must have a minimum of 3 Questions!") 
            return
        
        # Test each of the questions and choices for any index errors
        try:
            for i in range(1,self.createdQuestions+1):
                self.Quiz['questions']["Q"+str(i)]['question']
                for x in range(0,4):
                    self.Quiz['questions']["Q"+str(i)]['choices'][x]
        except: # If there are index errors
            print(i) # print errors if any

        self.mainarea.pack_forget() # Delete mainarea

        # Clear listboxes current questions
        self.createQuizList.delete(0, END)

        # Add 'Export' to listbox and select it
        self.createQuizList.insert(END,"Export")
        self.createQuizList.selection_clear(0, END)
        self.createQuizList.selection_set("end")

        # Create new frame which will hold the author and quiz name text boxes
        self.mainarea = tk.Frame(self.master, background='#F0F0F0', width=900, height=500)
        self.mainarea.pack(expand=True, fill='both', side='right')

        # Configure the new frames grid layout
        self.mainarea.grid_columnconfigure(0, weight=1)
        self.mainarea.grid_columnconfigure(1, weight=1)
        self.mainarea.grid_columnconfigure(2, weight=1)
        self.mainarea.grid_columnconfigure(3, weight=1)

        # Create a new title
        # This is displayed as a full width header
        self.title = Label(self.mainarea, text="KaYEET Quiz Creator", bg="#46178f", fg="white",font=('Helvetica Neue',24,"bold"),wraplength=700,pady=5)
        self.title.grid(row=0,column=0,sticky="we",columnspan=4)

        # Create label for any errors
        # This is displayed as a full width header
        self.errortitleVar= StringVar(self.master)
        self.errortitleVar.set("")
        self.errortitle = Label(self.mainarea, textvar=self.errortitleVar,relief="flat", bg="#F0F0F0", fg="red",font=('Helvetica Neue',12,"bold"),wraplength=400,pady=5)
        self.errortitle.grid(row=1,column=0,columnspan=4,sticky="EWN")

        # Create variable and label for the quiz name
        self.quizNameVar= StringVar(self.master)
        self.quizNameLabel= Label(self.mainarea, text="Quiz Name", bg="#F0F0F0", fg="black",font=('Helvetica Neue',16))
        self.quizNameLabel.grid(row=2,column=0,sticky="E")
        self.quizName = Entry(self.mainarea,textvar=self.quizNameVar,relief="flat", bg="lightgrey",fg="black",font=('Helvetica Neue',16))
        self.quizName.grid(row=2,column=1,sticky="WE", padx=30,pady=30,ipady=5,ipadx=50,columnspan=1)

        # Create variable and label for the quiz author
        self.quizAuthorVar= StringVar(self.master)
        self.quizAuthorLabel= Label(self.mainarea, text="Author", bg="#F0F0F0", fg="black",font=('Helvetica Neue',15))
        self.quizAuthorLabel.grid(row=3,column=0,sticky="E")
        self.quizAuthor = Entry(self.mainarea,textvar=self.quizAuthorVar,relief="flat", bg="lightgrey",fg="black",font=('Helvetica Neue',16))
        self.quizAuthor.grid(row=3,column=1,sticky="WE",padx=30, pady=30,ipady=5,ipadx=50,columnspan=1)

        # Create an export button which when pressed, will export the file to (Quiz name).YEET
        self.export= Button(self.mainarea, text="Export",relief="flat", bg="#46178f", fg="white", width=15,height=2, highlightcolor="red", font=("Montserrat", '12','bold'),command=self.exportFile)
        self.export.grid(row=4,column=1,sticky="E",padx=0, pady=5)

    # Exports the file to (Quiz name).YEET
    def exportFile(self):
        # Reset the values to their default if they were changed
        self.errortitleVar.set("")
        self.quizName.config(bg="lightgrey")
        self.quizAuthor.config(bg="lightgrey")

        # Check that a string has been entered in quizName entry
        if self.quizNameVar.get() == "":
            self.quizName.config(bg="red")
            self.errortitleVar.set("Error! Please Enter Quiz Name!")
            return

         # Check that a string has been entered into the quizAuthor entry
        if self.quizAuthorVar.get() == "":
            self.quizAuthor.config(bg="red")
            self.errortitleVar.set("Error! Please Enter Author Name")
            return

        # Check to make sure the file doesn't already exist
        if glob.glob(self.quizNameVar.get()+".YEET"):
            self.quizName.config(bg="red")
            self.errortitleVar.set("Error! This Quiz Already Exists!")
            return
        
        # Set the length of the quiz
        self.Quiz["meta"]['length']=self.createdQuestions
        
        # Set the author value to the quiz
        self.Quiz["meta"]['author']= self.quizAuthorVar.get()

        # Set the title value to the quiz
        self.Quiz["meta"]['title']= self.quizNameVar.get()

        # Create new file with the extension .YEET
        with open(str(self.quizNameVar.get())+".YEET", "w") as jsonFile:
            # Write the dictionary data to the file
            json.dump(self.Quiz, jsonFile)

        # Clear frame
        self.mainarea.destroy()
        self.scrollbar.destroy()
        self.sidebar.destroy()

        # Go back to home
        self.home()

# Function run on load
def init():   
    root = Tk() # Create Tkinter object 
    root.minsize("1000","750") # Creates static window
    root.maxsize("1000","750") # <-|
    root.title('KaYEET Quiz Game') # Set the window name to 'KaYEET'
    root.iconbitmap('images/icon.ico') # Set the window Icon to that of the KaYeet Logo
    homescreen=QuizGUI(root) # Run the object
    print("\n"*50,"\tKaYEET Started!\t\tMade By Josh Boag\n"+"-"*55) # Print start message
    root.mainloop() # Continue running the program 

init() # call when loaded
