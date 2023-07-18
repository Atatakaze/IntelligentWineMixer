#!usr/bin/python3
# Program:
#	Provide GUI_main.py with GUI window class and functions.
# Author:
# 	bobo
# History:
# 	2023/07/17	@bobo 


from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import math
from joblib import load

from motor_function import motor_init, motor_run, motor_param, Mixing

# ====== <parameters> ====== #
motor1 = [17, 18, 27, 22]
motor2 = [10, 9, 11, 8]

MODEL = './model/RF_model_32bit.joblib'
# ======</parameters> ====== #

# root window
class Tkwindow():
    # create root window
    def __init__(self):
        # initialize window name, size
        self.window = tk.Tk()
        self.window.title('Intelligent wine mixer')
        self.window.geometry('450x240')

        # setting frame of the widget
        div1 = tk.Frame(self.window, width=450, height=140)
        div2 = tk.Frame(self.window, width=180, height=50)
        div3 = tk.Frame(self.window, width=180, height=50)
        # setting widget position = (column, row)
        div1.grid(column=0, row=0, padx=10)
        div2.grid(column=0, row=1, padx=10, pady=5)
        div3.grid(column=0, row=2, padx=10, pady=5)

        self.define_layout(self.window, cols=1, rows=3)
        self.define_layout([div1, div2, div3])
        
        lb1 = tk.Label(div1, text="Welcome to intelligent wine mixer", font=('Arial', 20))
        lb1.grid(sticky=E+W+S+N, pady=40)

        bt1 = tk.Button(div2, text='wine1', font=('Arial', 16), bg='steel blue', fg='white', command=self.wine1, width=15)
        bt1.grid(column=0, row=0, padx=10)
        bt2 = tk.Button(div2, text='wine2', font=('Arial', 16), bg='steel blue', fg='white', command=self.wine2, width=15)
        bt2.grid(column=1, row=0, padx=10)
        bt3 = tk.Button(div3, text='start', font=('Arial', 16), bg='DarkOrange1', fg='white', command=self.start, width=15)
        bt3.grid(column=0, row=0, padx=10)
        bt4 = tk.Button(div3, text='leave', font=('Arial', 16), bg='DarkOrange1', fg='white', command=self.quit, width=15)
        bt4.grid(column=1, row=0, padx=10)

        self.define_layout(self.window, cols=1, rows=3)
        self.define_layout([div1, div2, div3])

        self.wine1_attributes = {'fixed acidity': 4.5, 
                                 'volatile acidity': 0.6, 
                                 'citric acid': 0.0, 
                                 'residual sugar': 2.0, 
                                 'chlorides': 0.0, 
                                 'total sulfur dioxide': 57, 
                                 'density': 0.9554, 
                                 'pH': 3.5, 
                                 'alcohol': 13.5}
        
        self.wine2_attributes = {'fixed acidity': 6.255, 
                                 'volatile acidity': 0.12, 
                                 'citric acid': 0.0, 
                                 'residual sugar': 1.51, 
                                 'chlorides': 0.0, 
                                 'total sulfur dioxide': 47, 
                                 'density': 0.9642, 
                                 'pH': 3.77, 
                                 'alcohol': 10.15}

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

    def wine1(self):
        MakeForm(self.wine1_attributes)

    def wine2(self):
        MakeForm(self.wine2_attributes)

    def start(self):
        messagebox.showinfo('INFO', "Start mixing ...")

        # load model
        model = load(MODEL)
        # calculating different blending ratio
        for ratio in range(0, 100, 5):
            w1 = np.array(ratio / 100)
            w2 = np.array((100 - ratio) / 100)
            mix1 = [4.5, 0.6, 0.0, 2.0, 0.0, 57, 0.9554, 3.5, 13.5]
            mix2 = [6.255, 0.12, 0.0, 1.51, 0.0, 47, 0.9642, 3.77, 10.15]
            ##### PH ######
            list1 = mix1.copy()
            list2 = mix2.copy()
            H2_1 = 10 ** -list1[7]
            H2_2 = 10 ** -list2[7]
            list1.remove(list1[7])
            list2.remove(list2[7])
            H2_mix=(w1 * H2_1 + w2 * H2_2) / 1
            PH_mix = -math.log(H2_mix, 10)
            wine_mix=(w1 * list1 + w2 * list2)
            wine_mix1 = wine_mix.tolist()
            wine_mix2 = wine_mix1.copy()
            wine_mix2.insert(7,PH_mix)

            if w1 == 0:
                best_quality = model.predict([mix1])
                blend_ratio = np.array([w1, w2])
            elif w2 == 0:
                prediction = model.predict([mix2])
                if prediction > best_quality:
                    blend_ratio = np.array([w1, w2])
                    best_quality = prediction
            else:
                prediction = model.predict([wine_mix2])
                if prediction > best_quality:
                    blend_ratio = np.array([w1, w2])
                    best_quality = prediction

        # initial motor1 and motor2
        MOTOR1_STEPS, MOTOR2_STEPS = motor_param()
        SEQUENCE1, SEQUENCE_COUNT1, PIN_COUNT1 = motor_init(motor1)
        SEQUENCE2, SEQUENCE_COUNT2, PIN_COUNT2 = motor_init(motor2)

        # total volume = 40
        DURATION1, DURATION2 = Mixing(40 * blend_ratio[0], blend_ratio[1])

        # start mixing
        #motor_run(motor1, 1, DURATION1, MOTOR1_STEPS)
        #motor_run(motor2, 2, DURATION2, MOTOR2_STEPS)

        FinishMessage(blend_ratio=blend_ratio, quality=best_quality)


# form window
class MakeForm(Tkwindow):
    # custom mode window
    def __init__(self, wine_attibutes):
        self.form = tk.Tk()
        self.form.title('Wine attributes entry')
        self.form.geometry('400x280')

        self.wine_attributes = wine_attibutes

        # setting frame of the widget
        form_div1 = tk.Frame(self.form, width=400, height=230)
        form_div2 = tk.Frame(self.form, width=100, height=50)

        form_div1.grid(column=0, row=0, padx=5, pady=5)
        form_div2.grid(column=0, row=1, padx=20)

        self.define_layout(self.form, cols=1, rows=2)
        self.define_layout([form_div1, form_div2])

        # make form
        lb1 = tk.Label(form_div1, text='Fixed acidity: ', anchor='w')
        lb1.grid(column=0, row=0, padx=10)
        self.en1 = tk.Entry(form_div1)
        self.en1.grid(column=1, row=0, padx=10)
        lb2 = tk.Label(form_div1, text='Volatile acidity: ', anchor='w')
        lb2.grid(column=0, row=1, padx=10)
        self.en2 = tk.Entry(form_div1)
        self.en2.grid(column=1, row=1, padx=10)
        lb3 = tk.Label(form_div1, text='Citric acid: ', anchor='w')
        lb3.grid(column=0, row=2, padx=10)
        self.en3 = tk.Entry(form_div1)
        self.en3.grid(column=1, row=2, padx=10)
        lb4 = tk.Label(form_div1, text='Residual sugar: ', anchor='w')
        lb4.grid(column=0, row=3, padx=10)
        self.en4 = tk.Entry(form_div1)
        self.en4.grid(column=1, row=3, padx=10)
        lb5 = tk.Label(form_div1, text='Chlorides: ', anchor='w')
        lb5.grid(column=0, row=4, padx=10)
        self.en5 = tk.Entry(form_div1)
        self.en5.grid(column=1, row=4, padx=10)
        lb6 = tk.Label(form_div1, text='Total sulfur dioxide: ', anchor='w')
        lb6.grid(column=0, row=5, padx=10)
        self.en6 = tk.Entry(form_div1)
        self.en6.grid(column=1, row=5, padx=10)
        lb7 = tk.Label(form_div1, text='Density: ', anchor='w')
        lb7.grid(column=0, row=6, padx=10)
        self.en7 = tk.Entry(form_div1)
        self.en7.grid(column=1, row=6, padx=10)
        lb8 = tk.Label(form_div1, text='pH: ', anchor='w')
        lb8.grid(column=0, row=7, padx=10)
        self.en8 = tk.Entry(form_div1)
        self.en8.grid(column=1, row=7, padx=10)
        lb9 = tk.Label(form_div1, text='Alcohol: ', anchor='w')
        lb9.grid(column=0, row=8, padx=10)
        self.en9 = tk.Entry(form_div1)
        self.en9.grid(column=1, row=8, padx=10)

        bt_1 = tk.Button(form_div2, text='save', font=('Arial', 16), bg='gray', fg='white', command=self.save, width=100)
        bt_1.grid(padx=80)

        self.define_layout(self.form, cols=1, rows=2)
        self.define_layout([form_div1, form_div2])
        
        self.form.mainloop()

    # save entries
    def save(self):
        self.wine_attributes['fixed acidity']  = float(self.en1.get())
        self.wine_attributes['volatile acidity']  = float(self.en2.get())
        self.wine_attributes['citric acid']  = float(self.en3.get())
        self.wine_attributes['residual sugar']  = float(self.en4.get())
        self.wine_attributes['chlorides']  = float(self.en5.get())
        self.wine_attributes['total sulfur dioxide']  = float(self.en6.get())
        self.wine_attributes['density']  = float(self.en7.get())
        self.wine_attributes['pH']  = float(self.en8.get())
        self.wine_attributes['alcohol']  = float(self.en9.get())

        self.form.destroy()


# finish window
class FinishMessage(Tkwindow):
    # custom mode window
    def __init__(self, blend_ratio, quality):
        self.msg_page = tk.Tk()
        self.msg_page.title('Blending results')
        self.msg_page.geometry('300x150')

        # setting frame of the widget
        msg_div1 = tk.Frame(self.msg_page, width=300, height=80)
        msg_div2 = tk.Frame(self.msg_page, width=300, height=40)
        msg_div3 = tk.Frame(self.msg_page, width=300, height=30)

        msg_div1.grid(column=0, row=0, padx=5, pady=5)
        msg_div2.grid(column=0, row=1, padx=20)
        msg_div3.grid(column=0, row=2, padx=30)

        self.define_layout(self.msg_page, cols=1, rows=3)
        self.define_layout([msg_div1, msg_div2, msg_div3])

        lb1 = tk.Label(msg_div1, text='Quality : {}'.format(np.round(quality, 2)), anchor='w', font=('Arial', 20))
        lb1.grid(column=0, row=0, padx=10)
        lb2 = tk.Label(msg_div2, text='(wine1) {}:{} (wine2)'.format(np.round(blend_ratio[0], 2), np.round(blend_ratio[1], 2)), anchor='w', font=('Arial', 14))
        lb2.grid(column=0, row=1, padx=10)

        bt_1 = tk.Button(msg_div3, text='OK', font=('Arial', 16), bg='gray', fg='white', command=self.confirm, width=100)
        bt_1.grid(padx=80)

        self.define_layout(self.msg_page, cols=1, rows=3)
        self.define_layout([msg_div1, msg_div2, msg_div3])
        
        self.msg_page.mainloop()

    # confirm
    def confirm(self):
        self.msg_page.destroy()