"""
2019-06957 Michael Benjamin C. Morco
CS 150 Extra Lab 1
Wordle Clone

"""

from ctypes import alignment
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import random

class get_word:
    def __init__(self, words):
        self.rando = random.randint(0,2314)
        self.words = words
    def __repr__(self):    
        return self.words[self.rando]
        #return input()

class make_grid:
    def __init__(self):
        self.guess_row = toga.Box(style=Pack(direction=ROW,alignment=CENTER,flex=1,padding_bottom=5))
        for j in range(5):
            if j == 0:
                self.guess_row.add(toga.Button('',style=Pack(alignment=CENTER,font_size=15,width = 50, height = 50,background_color="white")))
            else:
                self.guess_row.add(toga.Button('',style=Pack(alignment=CENTER,font_size=15,width = 50, height = 50,padding_left=5,background_color="white")))

class color_classification:
    def __init__(self, guess: str, answer: str):
        self.guess = guess
        self.answer = answer
        self.color_grid = ["transparent","transparent","transparent","transparent","transparent"]
        self.correct = 0
    def color_check(self):
        if self.guess == self.answer:
            self.correct = 1
            self.color_grid = ['#6aaa64','#6aaa64','#6aaa64','#6aaa64','#6aaa64']
        else:
            guess_list = []
            guess_list[:0] = str(self.guess).upper()
            #print(guess_list)
            ans_list = []
            ans_list[:0] = str(self.answer).upper()
            #print(ans_list)

            for i in range(5):
                if guess_list[i] == ans_list[i]:
                    #print("green: " + guess_list[i])
                    self.color_grid[i] = "#6aaa64"
                    guess_list[i] = "#6aaa64"
                    ans_list[i] = "#6aaa64"


            for i in range(5):
                if guess_list[i] in ans_list:
                    if guess_list[i] != "#6aaa64":
                        #print("yellow: " + guess_list[i])
                        self.color_grid[i] = "#c9b458"

                        ans_list[ans_list.index(guess_list[i])] = "#c9b458"
                        guess_list[i] = "#c9b458"



            for i in range(5):
                if guess_list[i] != "#6aaa64" and guess_list[i] != "#c9b458":
                    #print("grey: " + guess_list[i])
                    self.color_grid[i] = "#787c7e"
                    guess_list[i] = "#787c7e"
                


    


class WordleClone(toga.App):
    

    def startup(self):
        #Opens words.txt
        file = open(str(self.paths.app)+"\\..\\words.txt","r")
        self.words = file.read()
        self.words = self.words.split("\n")
        file.close()

        #Gets random word
        self.chosen_word = str(get_word(self.words))
        #print("Chosen word is",self.chosen_word)
        
        #Opens allowed_guesses.txt
        file = open(str(self.paths.app)+"\\..\\allowed_guesses.txt","r")
        self.allowed_guesses = file.read()
        self.allowed_guesses = self.allowed_guesses.split("\n")
        file.close()

        #initialize variables
        self.green_letters = []
        self.yellow_letters = []
        self.guess_no = 0
        main_box = toga.Box(style=Pack(direction=COLUMN, alignment = CENTER, text_align = CENTER,padding = 5))
        guess_label = toga.Label('Guess: ')
        self.guess_input = toga.TextInput(style=Pack(flex=1))

        #Makea box containing guess_label and self.guess_input
        guess_box = toga.Box(style=Pack(direction=ROW,padding=(5, 0)))
        guess_box.add(guess_label)
        guess_box.add(self.guess_input)

        self.button = toga.Button(
            'Guess',
            on_press=self.guess_answer,
            style=Pack(alignment=CENTER,padding=(5,0))
        )

        #set up the alphabet list, z is separated because we do not want it to have padding to the right
        self.alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.alpha_list = toga.Box(style=Pack(direction=ROW, padding=(5,0), alignment = CENTER))
        for i in range(26):
            self.alpha_list.add(toga.Label(self.alphabet[i],style=Pack(direction = ROW, text_align=CENTER,padding_right = 1,padding_left = 1)))

        #Restart button
        button2 = toga.Button(
            'Restart',
            on_press=self.restart_game,
            style=Pack(padding=(5,0))
        )


        main_box.add(guess_box)
        main_box.add(self.button)
        main_box.add(self.alpha_list)


        self.master = []
        for i in range(6):
            ii = make_grid().guess_row
            self.master.append(ii)
            main_box.add(ii)

        main_box.add(button2)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box

        self.main_window.show()

    def guess_answer(self, widget):
        if self.guess_no > 5:
            msg = "Game over! The word is "+self.chosen_word
            self.main_window.info_dialog("Wordle",msg)
        elif len(self.guess_input.value) != 5:
            #print("Not 5 characters!")
            self.main_window.error_dialog("Wordle","Guess does not have five characters")
        elif self.guess_input.value.isalpha() == False:
            #print("Not alphabet")
            self.main_window.error_dialog("Wordle","Guess has non-letter characters")
        elif self.guess_input.value not in self.allowed_guesses:
            #print("not a valid guess")
            self.main_window.error_dialog("Wordle","Not a valid guess")
        
        else:
            colors = color_classification(self.guess_input.value, self.chosen_word)
            colors.color_check()
            #print(colors.correct)
                

            for i in range(5):
                #setting colors for the tiles
                self.master[self.guess_no].children[i].label = str(self.guess_input.value[i]).upper()
                self.master[self.guess_no].children[i].style.background_color = colors.color_grid[i]
                self.master[self.guess_no].children[i].style.color = "white"
                
                
                #setting colors for the alphabet list
                #yellow -> green, grey-> green, transparent -> green
                #if green already, no change is needed
                #if yellow or transparent, it can be updated (grey and green remains grey/green always)
                
                #print(self.alpha_list.children[self.alphabet.index(self.guess_input.value[i].upper())].style.background_color)
                
                if (str(self.alpha_list.children[self.alphabet.index(self.guess_input.value[i].upper())].style.background_color) == "None") or (str(self.alpha_list.children[self.alphabet.index(self.guess_input.value[i].upper())].style.background_color) == "rgb(201, 180, 88)" and str(colors.color_grid[i]) == "#6aaa64"):                 
                        #print("Updating "+str(self.alpha_list.children[self.alphabet.index(self.guess_input.value[i].upper())].text)+ " to " + str(colors.color_grid[i]))
                        self.alpha_list.children[self.alphabet.index(self.guess_input.value[i].upper())].style.background_color = colors.color_grid[i]
                        self.alpha_list.children[self.alphabet.index(self.guess_input.value[i].upper())].style.color = "white"




            if colors.correct == 1:
                #print("Correct!")
                self.main_window.info_dialog("Wordle","Congratulations!")
                self.button.enabled = False
            
            self.guess_no+=1

            if self.guess_no > 5 and colors.correct == 0:
                msg = "Game over! The word is "+self.chosen_word
                self.main_window.info_dialog("Wordle",msg)
        
        #Erase value of text input box
        self.guess_input.value=""

    def restart_game(self, widget):
        self.guess_no = 0
        self.button.enabled = True
        self.guess_input.value=""

        for i in range(6):
            for ii in range(5):
                self.master[i].children[ii].label = ''
                self.master[i].children[ii].style.background_color = "white"
                self.master[i].children[ii].style.color = "black"
        
        for i in range(26):
            self.alpha_list.children[i].style.color = "black"
            self.alpha_list.children[i].style.background_color = None
            

        self.chosen_word = str(get_word(self.words))
        #print("Chosen word is",self.chosen_word)

    


def main():
    return WordleClone()

