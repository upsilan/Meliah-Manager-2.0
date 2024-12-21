from tkinter import *
import datetime

root = Tk()
root.title("Meliah Manager")
root.geometry("320x270")

topicStartTime = datetime.datetime.now()
topicNum = 0

people = []

class Person:
    def __init__(self, topicStartTime):
        self.lastOut = topicStartTime
        self.secondsOutFromTopic = 0
        self.timeLimit = 330
        self.inside = False
        self.insideInitiated = False
        self.strikes = 0
        self.canvas = Canvas(root, width = 320, height = 270)
        self.rectangle = self.canvas.create_rectangle(10, 10, 10+300, 10+250, fill="#35447a", outline="#06123d")
        #creates the writable name textbox
        text_box = Text(self.canvas, height=1, width = 22, font=("Helvetica", 18))
        text_box.place(x=15, y=15)
        #creates the time out from topic text
        self.timeText = self.canvas.create_text(320/2, 270/2 - 50, text = "--:--", anchor='center', font=("Helvetica", 55))
        self.strikeText = self.canvas.create_text(320/2, 190, text = "strikes: 0", anchor='center', font=("Helvetica", 20))
        #enter button
        enter = Button(self.canvas, width=4, height=1, text="Enter", font=("Helvetica", 20), command=lambda: self.Enter())
        enter.place(x=40, y=120)
        #leave button
        leave = Button(self.canvas, width=4, height=1, text="Leave", font=("Helvetica", 20), command=lambda: self.Leave())
        leave.place(x=320 - 40 - leave.winfo_reqwidth(), y=120)
        #strikes button
        strike = Button(self.canvas, width=4, height=1, text="strike", font=("Helvetica", 13), command=lambda: self.Strike())
        strike.place(x=320/2 - strike.winfo_reqwidth() / 2, y=210)
        
        self.updateTimer()
        self.tick()
        
    def Leave(self):
        if not self.insideInitiated:
            self.insideInitiated = True
            self.inside = True
        if self.inside:
            self.inside = False
        
    def Enter(self):
        if not self.insideInitiated:
            self.insideInitiated = True
            self.inside = False
            self.secondsOutFromTopic += (datetime.datetime.now() - self.lastOut).total_seconds()
        if not self.inside:
            self.inside = True

    def Strike(self):
        self.strikes += 1
        self.canvas.itemconfig(self.strikeText, text=f"strikes: {self.strikes}")
    
    def updateTimer(self):
        if not self.insideInitiated:
            self.canvas.after(1, self.updateTimer)
            return

        self.canvas.itemconfig(self.timeText, text=('%02d:%02d' % (self.secondsOutFromTopic / 60, self.secondsOutFromTopic % 60)))
        self.canvas.after(1, self.updateTimer)

    def tick(self):
        if not self.insideInitiated:
            self.canvas.after(1000, self.tick)
            return
        if not self.inside:
            self.secondsOutFromTopic += 1
        self.canvas.after(1000, self.tick)
    
        
def placeCanvases():
    x = min(len(people) + 1, 4) * 320
    y = int((len(people) / 4) + 1) * 270
    root.geometry(f"{x}x{y}")
    
    for person in people:
        person.canvas.place(x=people.index(person) % 4 * 320, y=int(people.index(person) / 4) * 270)
    buttonCanvas.place(x=len(people) % 4 * 320, y=int(len(people) / 4) * 270)

def addPerson():
    people.append(Person(topicStartTime))
    placeCanvases()

def resetTopic():
    global topicStartTime
    topicStartTime = datetime.datetime.now()
    for person in people:
        person.lastOut = topicStartTime
        person.secondsOutFromTopic = 0

buttonCanvas = Canvas(root, width = 320, height = 270)
buttonCanvas.create_rectangle(10, 10, 10 + 300, 10 + 250, fill="#717891", outline="#06123d")
button = Button(buttonCanvas, width=3, height=1, text="+", font=("Helvetica", 20), command=lambda: addPerson())
button.place(x=(320/2) - button.winfo_reqwidth() / 2, y=(270/2) - button.winfo_reqheight() / 2)
reset = Button(buttonCanvas, width = 9, height=1, text="New Topic", font=("Helvetica", 12), command=lambda: resetTopic())
reset.place(x=(320/2) - reset.winfo_reqwidth() / 2, y=200)
placeCanvases()

root.mainloop()
