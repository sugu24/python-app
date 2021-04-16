import tkinter as tk
from tkinter import messagebox
import pyautogui as pa
import csv
import random

# 問題数
l = 5

class App(tk.Tk): 
    def __init__(self):
        # ウィンドウの初期化
        self.master = tk.Tk()
        self.master.title('英単語勉強タイピング')
        self.master.geometry("600x400")
        self.__init2__()

    
    def __init2__(self):
        # 変数
        self.get_problems = self.get_problems_from_csv()
        self.problem_english = ""
        self.problem_japanese = ""
        self.continue_wrose = ""
        self.all_num_problems = str(len(self.get_problems)//2)
        self.stay_problems_text = "残り" + self.all_num_problems + "問"

        # 入力欄を作成
        self.input_typing = tk.Entry(width=28,font=20)
        self.input_typing.place(x=150, y=200,height=30)
        self.input_typing.bind("<Return>",lambda _:self.answer_by_enter())
    
        # 指定単語表示ラベルを作成
        self.english = tk.Label(width=25,text="英語　  ： ", font=20)
        self.english.place(x=30, y=100)
        self.output_target_word = tk.Label(width=25,text='英語が表示されるよ', anchor="w", font=20)
        self.output_target_word.place(x=220, y=100)
        
        
        # 指定単語の意味を表示するラベルを作成
        self.japanese = tk.Label(width=25,text="日本語 ： ", font=20)
        self.japanese.place(x=30, y=150)
        self.output_target_japanese = tk.Label(width=25,text="日本語訳が表示されるよ", anchor="w", font=40)
        self.output_target_japanese.place(x=220,y=150)
        
        # 残り問題数表示ラベルを作成
        self.stay_problems = tk.Label(width=25,text=self.stay_problems_text, font=40)
        self.stay_problems.place(x=150, y=40)
        
        # 正誤表示
        self.ok_or_wrose_label = tk.Label(width=25,text="タイピング結果表示欄", font=20)
        self.ok_or_wrose_label.place(x=150,y=250)
        
        # スタートボタン作成
        self.start_button = tk.Button(width=20, text="start!", font=10, command=self.click_start)
        self.start_button.place(x=180, y=300)
        self.start_button.configure(bg='gray')
        self.flag = True
    
    
    def get_problems_from_csv(self):
        temp = []
        re = []
        numbers = set()
        global l
        
        with open("english_word.csv",encoding="utf-8-sig") as f:
            r = csv.reader(f)
            for i in r:
                temp.append(i)
    
        while len(numbers) < l: numbers.add(int(random.random()*len(temp)))
    
        for ind in numbers:
            re.append(temp[ind][0])
            re.append(temp[ind][1])                
            
        return re


    def answer_by_enter(self):
        s = self.input_typing.get()
        if self.problem_english == s or self.problem_japanese == s:
            pa.press("kanji")
            self.typing_result(True)
            self.input_typing.delete(0, tk.END) # テキストボックスを空欄にする
            if len(self.get_problems)==0:
                self.next_procedure()
            else: 
                #問題取得↓
                self.get_and_display_problem()
        else:
            self.typing_result(False)
    
    
    def next_procedure(self):
        self.flag = True
        self.stay_problems_updata()
        res = messagebox.askyesno("終了", "続ける？")
        if res:
            pa.press("kanji")
            self.__init2__()
            self.click_start()
        else:
            exit()
    
    
    def click_start(self):
        if not self.flag: return
        self.flag = False
        self.input_typing.focus_set()
        def countdown(s):
            if s == 0:
                self.ok_or_wrose_label["text"]=""
                self.get_and_display_problem()
            else:
                self.stay_problems["text"]=str(s)
                self.master.after(1000,countdown,s-1)
        countdown(3)


    def english_updata(self, string):
        self.output_target_word["text"]=string
    
    
    def japanese_updata(self, string):
        self.output_target_japanese["text"]=string


    def get_and_display_problem(self):
        if len(self.get_problems)%2==0:
            self.stay_problems_updata()
            self.problem_english = self.get_problems.pop(0)
            self.english_updata(self.problem_english)
            self.japanese_updata("")
        else:
            self.problem_english = False
            self.problem_japanese = self.get_problems.pop(0)
            self.japanese_updata(self.problem_japanese)
    
    
    def typing_result(self,result):
        if result: 
            self.ok_or_wrose_label["text"]="○"
            self.continue_wrose=""
        else: 
            self.continue_wrose+="×"
            self.ok_or_wrose_label["text"]=self.continue_wrose
            
    
    def stay_problems_updata(self):
        self.stay_problems_text = "残り" + str(len(self.get_problems)//2) + "問"
        self.stay_problems["text"]=self.stay_problems_text
    
    
    def mainloop(self):
        self.master.mainloop()
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
    