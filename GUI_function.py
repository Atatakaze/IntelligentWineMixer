#!usr/bin/python3
# Program:
#	Provide GUI_main.py with GUI window class and functions.
# Author:
# 	bobo
# History:
# 	2022/04/11	@bobo 


from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
from motor_function import motor_init, motor_run, motor_param, Mixing

# ====== <parameters> ====== #
motor1 = [17, 18, 27, 22]
motor2 = [10, 9, 11, 8]
# ======</parameters> ====== #

# root window
class Tkwindow():
    # create root window
    def __init__(self):
        # initialize window name, size
        self.window = tk.Tk()
        self.window.title('Burette Motor')
        self.window.geometry('450x150')

        # setting frame of the widget
        div1 = tk.Frame(self.window, width=450, height=100, bg='blue')
        div2 = tk.Frame(self.window, width=225, height=50, bg='green')
        div3 = tk.Frame(self.window, width=225, height=50, bg='red')
        # setting widget position = (column, row)
        div1.grid(column=0, row=0, columnspan=2, padx=5)
        div2.grid(column=0, row=1, padx=50, pady=5)
        div3.grid(column=1, row=1, padx=50, pady=5)

        self.define_layout(self.window, cols=2, rows=2)
        self.define_layout([div1, div2, div3])
        
        lb1 = tk.Label(div1, text="Which mode do you want to choose?\nAuto or Custom mode.", font=('Arial', 18))
        lb1.grid()
        
        bt_1 = tk.Button(div2, text='Auto Mode', font=('Arial', 14), bg='gray', fg='white', command=self.autoMode)
        bt_1.grid(sticky='e')
        bt_2 = tk.Button(div3, text='Custom Mode', font=('Arial', 14), bg='gray', fg='white', command=self.customMode)
        bt_2.grid(sticky='w')

        self.define_layout(self.window, cols=2, rows=2)
        self.define_layout([div1, div2, div3])
        
        self.window.mainloop()

    # quit window
    def quit(self):
        self.window.destroy()

    # create root frame layout
    def define_layout(self, obj, cols=1, rows=1):
        def method(trg, col, row):
            for c in range(cols):
                trg.columnconfigure(c, weight=1)
            for r in range(rows):
                trg.rowconfigure(r, weight=1)
        if type(obj) == list:
            [ method(trg, cols, rows) for trg in obj ]
        else:
            trg = obj
            method(trg, cols, rows)

    # basic message box
    def msg_box(self):
        messagebox.showinfo('Burette Motor', 'This service is not ready yet.')
        #messagebox.showwarning('MessageBox Warning', 'There is a warning.')
        #messagebox.showerror('MessageBox Error', 'There is an error.')
        #messagebox.askquestion('MessageBox Question', 'Confirm ?')

    def autoMode(self):
        messagebox.showinfo('Burette Motor <info>', "You choose the auto mode.\nPress OK to start mixing.")
        # initial motor1 and motor2
        MOTOR1_STEPS, MOTOR2_STEPS = motor_param()
        SEQUENCE1, SEQUENCE_COUNT1, PIN_COUNT1 = motor_init(motor1)
        SEQUENCE2, SEQUENCE_COUNT2, PIN_COUNT2 = motor_init(motor2)
        # best ratio = 2:8 
        # total volume = 40
        DURATION1, DURATION2 = Mixing(8, 32)

        # start mixing
        motor_run(motor1, 1, DURATION1, MOTOR1_STEPS)
        motor_run(motor2, 2, DURATION2, MOTOR2_STEPS)
        score_msg = "Evaluation score: 6.66"
        messagebox.showinfo('Burette Motor <info>', 'Mixing finish.')
        messagebox.showinfo('Burette Motor <info>', score_msg)

    def customMode(self):
        custom_window = Custom()

# custom mode window
class Custom(Tkwindow):
    # custom mode window
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Burette Motor <Custom Mode>')
        self.window.geometry('350x90')

        # setting frame of the widget
        cMode_div1 = tk.Frame(self.window, width=350, height=50, bg='blue')
        cMode_div2 = tk.Frame(self.window, width=350, height=40, bg='orange')

        cMode_div1.grid(column=0, row=0, padx=5, pady=5)
        cMode_div2.grid(column=0, row=1, padx=5)

        self.define_layout(self.window, cols=1, rows=3)
        self.define_layout([cMode_div1, cMode_div2])
        
        lb1 = tk.Label(cMode_div1, text='Choose one parameter to adjust.', font=('Arial', 14))
        lb1.grid()
        
        # seleced is the choise that user make
        selected = tk.StringVar()
        # initial radio button
        selected.set = 'Sweet'
        
        # radiobutton
        bt1 = tk.Radiobutton(cMode_div2, text='Sweetness', variable=selected, value='Sweet', font=('Arial', 12), command=self.sweetAdjust)
        bt1.grid(column=0, row=0, sticky='w')
        bt2 = tk.Radiobutton(cMode_div2, text='Acidity', variable=selected, value='Acid', font=('Arial', 12), command=self.acidAdjust)  
        bt2.grid(column=1, row=0, sticky='e')

        self.define_layout(self.window, cols=1, rows=3)
        self.define_layout([cMode_div1, cMode_div2])
        
        self.window.mainloop()

    # adjust sweetness
    def sweetAdjust(self):
        self.quit()
        sweetAdustWindow = Sweet()
    # adjust sweetness
    def acidAdjust(self):
        self.quit()
        acidAdustWindow = Acid()
        
# adjust sweetness window 
class Sweet(Custom):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Burette Motor <Adjust Sweeetness>')
        self.window.geometry('350x70')
        # setting frame of the widget
        sweet_div1 = tk.Frame(self.window, width=350, height=40, bg='blue')
        sweet_div2 = tk.Frame(self.window, width=230, height=30, bg='green')
        sweet_div3 = tk.Frame(self.window, width=120, height=30, bg='red')

        # setting widget position = (column, row)
        sweet_div1.grid(column=0, row=0, columnspan=2, padx=5)
        sweet_div2.grid(column=0, row=1, padx=10, pady=5)
        sweet_div3.grid(column=1, row=1, padx=10, pady=5)
        
        self.define_layout(self.window, cols=2, rows=2)
        self.define_layout([sweet_div1, sweet_div2, sweet_div3])
        
        lb1 = tk.Label(sweet_div1, text='Adjust how sweet you want.', font=('Arial', 14))
        lb1.grid()
        
        # sweetness menu options (default as normal sweet)
        self.opt = ttk.Combobox(sweet_div2, state='readonly')
        self.opt['values'] = ['No Sweet', 'Quarter Sweet', 'Half Sweet', 'Less Sweet', 'Normal Sweet', 'Very Sweet', 'Super Sweet']
        self.opt.current(4)
        self.opt.grid(sticky='e')

        bt_1 = tk.Button(sweet_div3, text='Confirm', font=('Arial', 10), bg='gray', fg='white', command=self.set_sweet)
        bt_1.grid(sticky='w')
        
        self.define_layout(self.window, cols=2, rows=2)
        self.define_layout([sweet_div1, sweet_div2, sweet_div3])
        
        self.window.mainloop()

        # confirm sweet choose
    def set_sweet(self):
        # Enable SWEETNESS_ENABLE and disable ACIDITY_ENABLE
        # Get custom parameters
        global SWEETNESS, SWEETNESS_ENABLE, ACIDITY, ACIDITY_ENABLE
        SWEETNESS_ENABLE = 'True'
        ACIDITY_ENABLE = 'False'
        print('set <SWEETNESS_ENABLE> ', SWEETNESS_ENABLE)
        SWEETNESS = self.opt.get()
        print('set <SWEETNESS> ', SWEETNESS)

        messagebox.showinfo('Burette Motor <info>', "You choose the custom mode.\nPress OK to start mixing.")
        # initial motor1 and motor2
        MOTOR1_STEPS, MOTOR2_STEPS = motor_param()
        SEQUENCE1, SEQUENCE_COUNT1, PIN_COUNT1 = motor_init(motor1)
        SEQUENCE2, SEQUENCE_COUNT2, PIN_COUNT2 = motor_init(motor2)
         
        # total volume = 40
        if SWEETNESS == 'No Sweet':
            DURATION1, DURATION2 = Mixing(0, 40)
            score = 5.57
        elif SWEETNESS == 'Quarter Sweet':
            DURATION1, DURATION2 = Mixing(8, 32)
            score = 5.91
        elif SWEETNESS == 'Half Sweet':
            DURATION1, DURATION2 = Mixing(16, 24)
            score = 6.04
        elif SWEETNESS == 'Less Sweet':
            DURATION1, DURATION2 = Mixing(20, 20)
            score = 6.23
        elif SWEETNESS == 'Normal Sweet':
            DURATION1, DURATION2 = Mixing(24, 16)
            score = 6.48
        elif SWEETNESS == 'Very Sweet':
            DURATION1, DURATION2 = Mixing(32, 8)
            score = 6.66
        elif SWEETNESS == 'Super Sweet':
            DURATION1, DURATION2 = Mixing(40, 0)
            score = 6.63

        # start mixing
        motor_run(motor1, 1, DURATION1, MOTOR1_STEPS)
        motor_run(motor2, 2, DURATION2, MOTOR2_STEPS)
        score_msg = "Evaluation score: %.2f" %score
        messagebox.showinfo('Burette Motor <info>', 'Mixing finish.')
        messagebox.showinfo('Burette Motor <info>', score_msg)
        # setting different ratio of the mix
        
        self.quit()
 
# adjust acidity window 
class Acid(Custom):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Burette Motor <Adjust Acidity>')
        self.window.geometry('350x70')
        # setting frame of the widget
        acid_div1 = tk.Frame(self.window, width=350, height=40, bg='blue')
        acid_div2 = tk.Frame(self.window, width=230, height=30, bg='green')
        acid_div3 = tk.Frame(self.window, width=120, height=30, bg='red')

        # setting widget position = (column, row)
        acid_div1.grid(column=0, row=0, columnspan=2, padx=5)
        acid_div2.grid(column=0, row=1, padx=10, pady=5)
        acid_div3.grid(column=1, row=1, padx=10, pady=5)
        
        self.define_layout(self.window, cols=2, rows=2)
        self.define_layout([acid_div1, acid_div2, acid_div3])
        
        lb1 = tk.Label(acid_div1, text='Adjust the acidity you want.', font=('Arial', 14))
        lb1.grid()
        
        # sweetness menu options (default as normal sweet)
        self.opt = ttk.Combobox(acid_div2, state='readonly')
        self.opt['values'] = ['Zero', 'Quarter', 'Half', 'Less', 'Normal', 'Very', 'Super']
        self.opt.current(4)
        self.opt.grid(sticky='e')

        bt_1 = tk.Button(acid_div3, text='Confirm', font=('Arial', 10), bg='gray', fg='white', command=self.set_acid)
        bt_1.grid(sticky='w')
        
        self.define_layout(self.window, cols=2, rows=2)
        self.define_layout([acid_div1, acid_div2, acid_div3])
        
        self.window.mainloop()

        # confirm sweet choose
    def set_acid(self):
        # Enable SWEETNESS_ENABLE and disable ACIDITY_ENABLE
        # Get custom parameters
        global SWEETNESS, SWEETNESS_ENABLE, ACIDITY, ACIDITY_ENABLE
        SWEETNESS_ENABLE = 'False'
        ACIDITY_ENABLE = 'True'
        print('set <ACIDITY_ENABLE> ', ACIDITY_ENABLE)
        ACIDITY = self.opt.get()
        print('set <ACIDITY> ', ACIDITY)

        messagebox.showinfo('Burette Motor <info>', "You choose the custom mode.\nPress OK to start mixing.")
        # initial motor1 and motor2
        MOTOR1_STEPS, MOTOR2_STEPS = motor_param()
        SEQUENCE1, SEQUENCE_COUNT1, PIN_COUNT1 = motor_init(motor1)
        SEQUENCE2, SEQUENCE_COUNT2, PIN_COUNT2 = motor_init(motor2)
         
        # total volume = 40
        if ACIDITY == 'No Sour':
            DURATION1, DURATION2 = Mixing(0, 40)
            score = 5.57
        elif ACIDITY == 'Quarter Sour':
            DURATION1, DURATION2 = Mixing(8, 32)
            score = 5.91
        elif ACIDITY == 'Half Sour':
            DURATION1, DURATION2 = Mixing(16, 24)
            score = 6.04
        elif ACIDITY == 'Less Sour':
            DURATION1, DURATION2 = Mixing(20, 20)
            score = 6.23
        elif ACIDITY == 'Normal Sour':
            DURATION1, DURATION2 = Mixing(24, 16)
            score = 6.48
        elif ACIDITY == 'Very Sour':
            DURATION1, DURATION2 = Mixing(32, 8)
            score = 6.66
        elif ACIDITY == 'Super Sour':
            DURATION1, DURATION2 = Mixing(40, 0)
            score = 6.63

        # start mixing
        motor_run(motor1, 1, DURATION1, MOTOR1_STEPS)
        motor_run(motor2, 2, DURATION2, MOTOR2_STEPS)
        score_msg = "Evaluation score: %.2f" %score
        messagebox.showinfo('Burette Motor <info>', 'Mixing finish.')
        messagebox.showinfo('Burette Motor <info>', score_msg)
        # setting different ratio of the mix
        
        self.quit()
