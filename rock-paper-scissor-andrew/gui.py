import tkinter
from tkinter import ttk
import cv2
from PIL import ImageTk, Image, ImageOps, ImageFile
import PIL.Image, PIL.ImageTk
import time
global a
from keras.models import load_model
import numpy as np


global a
a= 'd' #[[0.0 ,0.0 ]]
global b
b = 1
global c
c = 1

class VideoStream:
      def __init__(self, window, window_title, q1, q2 ,q3, video_source=-1):
          
          self.q1= q1
          self.q2 = q2
          self.q3 = q3
          self.ans = 0
          
          self.pbar = [[0,0,0,0]]
          self.size = (224,224)
          self.window = window
          
          self.vframe = tkinter.Frame(window)
          self.vframe.grid(row=0, column =0)
          #self.vframe.configure(background='orange')
          self.window.title(window_title)
          self.video_source = video_source
          
#           self.bframe = tkinter.Frame(window)
#           self.bframe.grid(row=2, column=0)
          
          self.button = tkinter.Button(self.vframe, text= "start", font=("Calibre", 14),padx=350, pady=30, command=self.start)
          self.button.grid(row=10, column=0, columnspan=2)
          
          self.button1 = tkinter.Button(self.vframe, text= "stop", font=("Calibre", 14),padx=350, pady=30, command=self.stop)
          self.button1.grid(row=11, column=0, columnspan=2)
          
          self.exitbutton = tkinter.Button(self.vframe, text = "exit", font=("Calibre", 14),padx=350, pady=30, command=self.kill)
          self.exitbutton.grid(row=12, column=0, columnspan=2)
          
          self.label = tkinter.Label(self.vframe, text="(User Input)",font=("Calibre", 16),fg ="red", padx=50, pady=5)
          self.label.grid(row = 1, column=0)
          self.label1 = tkinter.Label(self.vframe, text="(AI Decision)",font=("Calibre", 16), fg ="red", padx=50, pady=5)
          self.label1.grid(row = 1, column=1)
          
          self.pb = ttk.Progressbar(self.vframe, orient='horizontal', mode='determinate', length=500)
          self.pb.grid(row = 2, column=0, padx=10, pady=20, columnspan=2)
          
          self.label_r = tkinter.Label(self.vframe, text="↑↑ Rock Confidence",font=("Calibre", 16), padx=50)
          self.label_r.grid(row = 3, column=0, columnspan=2)
          
          self.pb1 = ttk.Progressbar(self.vframe, orient='horizontal', mode='determinate', length=500)
          self.pb1.grid(row = 4, column=0, padx=10, pady=20, columnspan=2)
                 
          self.label_p = tkinter.Label(self.vframe, text="↑↑ paper Confidence",font=("Calibre", 16), padx=50)
          self.label_p.grid(row = 5, column=0, columnspan=2)
          
          self.pb2 = ttk.Progressbar(self.vframe, orient='horizontal', mode='determinate', length=500)
          self.pb2.grid(row = 6, column=0, padx=10, pady=20, columnspan=2)
                 
          self.label_s = tkinter.Label(self.vframe, text="↑↑ scissor Confidence",font=("Calibre", 16), padx=50)
          self.label_s.grid(row = 7, column=0, columnspan=2)
          
          self.pb3 = ttk.Progressbar(self.vframe, orient='horizontal', mode='determinate', length=500)
          self.pb3.grid(row = 8, column=0, padx=10, pady=20, columnspan=2)
                 
          self.label_d = tkinter.Label(self.vframe, text="↑↑ default Confidence",font=("Calibre", 16), padx=50)
          self.label_d.grid(row = 9, column=0, columnspan=2)
          
  
         # open video source
          self.vid = MyVideoCapture(self.video_source)
 
          self.dsize = (600,580)   
         # Create a canvas that can fit the above video source size
          self.canvas = tkinter.Canvas(self.vframe, width = self.vid.width, height = self.vid.height)
          self.canvas.grid(row=0, column=0)
          
          self.output_canvas = tkinter.Canvas(self.vframe, width = self.vid.width, height = self.vid.height)
          self.output_canvas.grid(row=0, column=1)
          
          self.delay = 1
          self.update()
        
 
          
      
      def start(self):
         
          self.q1.put(1)
      
          
      def stop(self):
        
          self.q1.put(0)
          
          
      def kill(self):
          self.quit1()
          self.quit2()
          

      def quit1(self):
        
          self.window.quit()
          

      def quit2(self):
        
          self.q1.put(5)
         
          
      def update(self):
         
         ret, frame = self.vid.get_frame()
         frame = cv2.flip(frame, flipCode=1)
 
         if ret:
             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
             self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
             cv2.imwrite('/home/pi/Desktop/ksl/testimage.jpg',cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
             self.window.update()
             self.window.update_idletasks()
    
    
         try:
                  self.ans = self.q2.get(block=False)
                  self.pbar = self.q3.get(block= False)
                  print("this is the pipe result")
                  print(type(self.pbar))
                  print(self.ans)
                  
                  
         except Exception as e:
                    pass
         if self.ans != 'k':     
          self.pb['value'] = self.pbar[0][0] * 100
          self.pb1['value'] = self.pbar[0][1] * 100
          self.pb2['value'] = self.pbar[0][2] * 100
          self.pb3['value'] = self.pbar[0][3] * 100
         else:
          self.pb['value'] = 0
          self.pb1['value'] = 0
          self.pb2['value'] = 0
          self.pb3['value'] = 0
# 
         self.label_r.config(text=f"↑↑ Rock Confidence : {round(self.pb['value'])}%")
         self.window.update()
         self.label_p.config(text=f"↑↑ paper Confidence : {round(self.pb1['value'])}%")
         self.window.update()
         self.label_s.config(text=f"↑↑ scissor Confidence : {round(self.pb2['value'])}%")
         self.window.update()
         self.label_d.config(text = f"↑↑ default Confidence : {round(self.pb3['value'])}%")
         self.window.update()
         
         if(self.ans == 'p'):
                 self.img = cv2.imread('/home/pi/Desktop/ksl/paper.png')
                 self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)
                 self.img = cv2.resize(self.img, self.dsize)
                 self.img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.img))
                 self.output_canvas.create_image(0,0,image=self.img, anchor=tkinter.NW)
                 self.window.update()
                
         elif (self.ans == 'r'):
                 self.img = cv2.imread('/home/pi/Desktop/ksl/rock.png')
                 self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)
                 self.img = cv2.resize(self.img, self.dsize)
                 self.img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.img))
                 self.output_canvas.create_image(0,0,image=self.img, anchor=tkinter.NW)
                 self.window.update()

         elif (self.ans == 's'):
                 self.img = cv2.imread('/home/pi/Desktop/ksl/scissor.png')
                 self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)
                 self.img = cv2.resize(self.img, self.dsize)
                 self.img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.img))
                 self.output_canvas.create_image(0,0,image=self.img, anchor=tkinter.NW)
                 self.window.update()

         elif (self.ans == 'd' or self.ans =='k'):
                 self.img = cv2.imread('/home/pi/Desktop/ksl/blank.png')
                 self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)
                 self.img = cv2.resize(self.img, self.dsize)
                 self.img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.img))
                 self.output_canvas.create_image(0,0,image=self.img, anchor=tkinter.NW)
                 self.window.update()
                 
         
         self.window.after(self.delay, self.update)
       
     
      def mainloop(self):
         return self.window.mainloop()  



class hand:
 
    
    def __init__(self, q4, com):
        self.q4 = q4
        self.com = com
        self.count = 0
        self.decide = 'p'
        self.previous = 'p'
        
        
        
    def run_hand(self):
      while 1: 
        try:
            self.decide = self.q4.get(block=False)
                          
        except Exception as e:
            pass
        
        global a
      
        
        if a != self.decide :   
        
         if (self.decide == 'r'):
             self.mess = "rock"
             print("this is rock")
             self.x = self.mess.replace("\r\n", "\n")
             self.com.write(bytes(self.x, 'utf-8'))
             self.count = -1
             time.sleep(1)
             a = 'r'
             
             
         elif (self.decide == 'p'):
             self.mess = "paper"
             print("this is paper")
             self.x = self.mess.replace("\r\n", "\n")
             self.com.write(bytes(self.x, 'utf-8'))
             self.count = -1
             time.sleep(1)
             a = 'p'
             
             
         elif (self.decide == 's'):
             self.mess = "scissors"
             print("this is scissor")
             self.x = self.mess.replace("\r\n", "\n")
             self.com.write(bytes(self.x, 'utf-8'))
             self.count = -1
             time.sleep(1)
             a = 's'
             
         elif (self.decide == 'd' or self.decide == 'k'):
             self.mess = "default"
             print("this is default")
             self.x = self.mess.replace("\r\n", "\n")
             self.com.write(bytes(self.x, 'utf-8'))
             self.count = -1
             time.sleep(1)
             a = 'd'          
        
         else:
            print('breaking')
            break  

     
     
class AI:
      def __init__(self,q1,q2,q3,q4, model, data):
          self.q1= q1
          self.q2 = q2
          self.q3 = q3
          self.q4 = q4
          self.model =  model
          self.data = data
          self.b = 1
          self.a = 1

           
      def AIrun(self):

        
        while 1: 
           try:
            self.a = self.q1.get(block=False)
      
           except Exception as e:
               pass
      
           
           print(self.a)
           if self.a == 1  :
                print("ai running")
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                   
                try:
                   self.image = Image.open('/home/pi/Desktop/ksl/testimage.jpg')
                   self.size = (224, 224)
                   self.image = ImageOps.fit(self.image, self.size, Image.LANCZOS)    
                   self.image_array = np.asarray(self.image)
                # Normalize the image
                   self.normalized_image_array = (self.image_array.astype(np.float32) / 127.0) - 1
                # Load the image into the array
                   self.data[0] = self.normalized_image_array

                # run the inference
                   self.prediction = self.model.predict(self.data)
                   print(self.prediction)
                   
                   
                   self.chooseImg = np.argsort(self.prediction)
                   self.result = self.chooseImg[0,3]
                   
                   global b
                   
                   if b != self.result:
                   
                       if self.result == 0:
                           self.q2.put('p', block = False)
                           self.q4.put('p', block = False)
                           self.q3.put(self.prediction, block = False)
                           b = 'p'
                       elif self.result == 1:
                           self.q2.put('s', block = False)
                           self.q4.put('s', block = False)
                           self.q3.put(self.prediction, block = False)
                           b = 's'
                       elif self.result == 2:
                           self.q2.put('r', block = False)
                           self.q4.put('r', block = False)
                           self.q3.put(self.prediction, block = False)
                           b = 'r'
                       elif self.result == 3:
                           self.q2.put('d', block = False)
                           self.q4.put('d', block = False)
                           self.q3.put(self.prediction, block = False)
                           b = 'd'
                
                   
                except:
                    print("error")
                   
           elif self.a == 0:
                   print("AI stop")
                   self.q2.put('k', block= False) # d for default
                   self.q4.put('k', block= False)
                   time.sleep(3)
                
           else :
               self.q2.put('q',block=False)
               self.q4.put('q',block=False)
               break
    


class animal():
    def __init__(self):
        self.animal = 'dog'
        self.type = 'cute'
    def print(self):
        while 1:
         print(self.animal)     
     
     
     
     
     
     
class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)
 
     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()
   





