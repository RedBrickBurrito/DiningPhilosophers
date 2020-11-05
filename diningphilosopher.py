from tkinter import *
import threading
import time

import concurrent.futures
import random as rand


global numPhilosophers
numPhilosophers = 5
global fork
fork = [1, 2, 3, 4, 5]

for i in range(numPhilosophers):
    fork[i] = threading.Semaphore(1)


global room
room = threading.Semaphore(4)

root = Tk()
root.geometry("700x700") 

global eatingImg
eatingImg = PhotoImage(file="./img/eating.png")
eatingImg = eatingImg.subsample(2, 2)

global thinkingImg
thinkingImg = PhotoImage(file="./img/thinking.png")
thinkingImg = thinkingImg.subsample(4, 4)

global waitingImg
waitingImg = PhotoImage(file="./img/waiting.png")
waitingImg = waitingImg.subsample(4, 4)

isRunning = False

canvas = Canvas(root, bg="gray")

frame = Frame(root, bg="white")
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

ph1 = Label(frame, text="1")
ph1.place(relx=0.5, rely=0.1, anchor="center")
ph2 = Label(frame, text="2")
ph2.place(relx=0.7, rely=0.3, anchor="center")
ph3 = Label(frame, text="3")
ph3.place(relx=0.6, rely=0.6, anchor="center")
ph4 = Label(frame, text="4")
ph4.place(relx=0.4, rely=0.6, anchor="center")
ph5 = Label(frame, text="5")
ph5.place(relx=0.3, rely=0.3, anchor="center")

philosophers = []
philosophers.append(ph1)
philosophers.append(ph2)
philosophers.append(ph3)
philosophers.append(ph4)
philosophers.append(ph5)

def philosopher(id):

    maxThinkDelay = 10
    maxEatDelay = 10

    running = True

    wsem = threading.Semaphore(1)

    def think():
        newText = str(id) + ": thinking"
        philosophers[id].config(text=newText, image=thinkingImg)
        print("Thinking " + str(id))

        if keepRunning():
            time.sleep(rand.randint(0, maxThinkDelay))
            philosophers[id].config(image=waitingImg)

    def eat():
        newText = str(id) + ": eating"
        philosophers[id].config(text=newText, image=eatingImg)
        print("Eating " + str(id))
        if keepRunning():
            time.sleep(rand.randint(0, maxEatDelay))
            philosophers[id].config(text="finished", image='')

        

    def keepRunning():
        wsem.acquire()
        aux = running
        wsem.release()
        return aux

    while(keepRunning()):
        global isRunning
        if isRunning:
            think()
            room.acquire()
            fork[id].acquire()
            fork[(id + 1) % 5].acquire()
            eat()
            fork[(id + 1) % 5].release()
            fork[id].release()
            room.release()
        else:
            return 0

futures = []

def startSimulation():
    global isRunning
    isRunning = True
    for i in range(numPhilosophers):
        futures.append(threading.Thread(target=philosopher, args=(i, )))

        tempFutures = futures[i]
        tempFutures.start()

def stopSimulation():
    global isRunning
    isRunning = False

startButton = Button(text="Start Simulation", command=startSimulation)
startButton.place(relx=0.35, rely=0.9, anchor="center")
stopButton = Button(text="Stop Simulation", command=stopSimulation)
stopButton.place(relx=0.65, rely=0.9, anchor="center")

if __name__ == '__main__':
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = []

    #     for i in range(numPhilosophers):
    #         futures.append(executor.submit(philosopher, i))
        
    root.mainloop()