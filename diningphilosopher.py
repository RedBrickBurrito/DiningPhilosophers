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


def philosopher(id):

    maxThinkDelay = 10
    maxEatDelay = 10

    running = True

    wsem = threading.Semaphore(1)

    def think():
        print("Thinking " + str(id))

        if keepRunning():
            time.sleep(rand.randint(0, maxThinkDelay))

    def eat():
        print("Eating " + str(id))
        if keepRunning():
            time.sleep(rand.randint(0, maxEatDelay))

    def keepRunning():
        wsem.acquire()
        aux = running
        wsem.release()
        return aux

    while(keepRunning()):
        think()
        room.acquire()
        fork[id].acquire()
        fork[(id + 1) % 5].acquire()
        eat()
        fork[(id + 1) % 5].release()
        fork[id].release()
        room.release()


if __name__ == '__main__':

    #root = Tk()

    #a = Label(root, text="hello, world!!")
    # a.pack()

    # root.mainloop()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for i in range(numPhilosophers):
            futures.append(executor.submit(philosopher, i))
