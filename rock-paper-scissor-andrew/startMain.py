from gui import VideoStream, AI, hand
import multiprocessing
from multiprocessing import Process,Queue
import tkinter
from tkinter import ttk
from keras.models import load_model
import numpy as np
import serial


def stream(q1,q2,q3):
 w = VideoStream(tkinter.Tk(), "ROCK-PAPER_SCISSOR", q1,q2,q3)
 
 w.mainloop()
   

def ai(q1,q2,q3,q4):
     model = load_model('/home/pi/Desktop/rock-paper-scissor-KYaw/model/keras_model.h5',compile=False)
     data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
     m = AI(q1,q2,q3,q4,model,data)
     m.AIrun()

def robot_hand(q4):
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
    
    h = hand(q4, arduino)
    h.run_hand()

 
if __name__ == "__main__":
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    q4 = Queue()
  
    mp = multiprocessing.Process(target=stream, args=(q1,q2,q3))
    mp1 = multiprocessing.Process(target = ai, args=(q1,q2,q3,q4))
    mp2 = multiprocessing.Process(target = robot_hand, args=(q4,))

    mp.start()
    mp1.start()
    mp2.start()

    mp.join()
    mp1.join()
    mp2.join()
      
 

