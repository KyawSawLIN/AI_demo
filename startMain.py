from GUI import VideoStream, AI
import multiprocessing
from multiprocessing import Process,Queue
import tkinter
from tkinter import ttk
from keras.models import load_model
import numpy as np


def stream(q1,q2,q3):
 w = VideoStream(tkinter.Tk(), "ROCK-PAPER_SCISSOR", q1,q2,q3)
 
 w.mainloop()
   

def ai(q1,q2,q3):
     model = load_model('/home/pi/Desktop/ksl/model/keras_model.h5',compile=False)
     data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
     m = AI(q1,q2,q3,model,data)
     m.AIrun()

 
if __name__ == "__main__":
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
  
    mp = multiprocessing.Process(target=stream, args=(q1,q2,q3))
    mp1 = multiprocessing.Process(target = ai, args=(q1,q2,q3))

    mp.start()
    mp1.start()

    mp.join()
    mp1.join()
      
 

