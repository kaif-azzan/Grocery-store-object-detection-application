import cv2
from tkinter import *
from PIL import Image,ImageTk
#import matplotlib as pb
from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF

#==================================================

class App:
    def __init__(self,video_source="C:\\Users\\kaifm\\Downloads\\d.mp4"):
       
        self.window=Tk()
        self.window.iconbitmap("C:\\Users\\kaifm\\Downloads\\Graphicloads-Flat-Finance-Global.ico")
        self.window.title("Application active")
        self.window['bg']='black'
        self.window.geometry("1500x720")       
        self.window.resizable(0,0)

        self.video_source=video_source

        self.vid=MyVideoCapture(self.video_source)
        self.label=Label(self.window,text="Grocery store object detection application",font=15,bg='blue',fg='white',padx=900).pack()

        back=PhotoImage(file="C:\\Users\\kaifm\\Downloads\\pngegg (1).png")
        self.canvas= Canvas(self.window,height=600,width=self.vid.width)
        self.canvas.pack(side=TOP,fill=BOTH)
        self.canvas.create_image(0,0,image=back, anchor ="nw")


        self.update()
        self.b=Button(self.window,text="Exit",bg="maroon",padx=1080,pady=10,command=self.qt).pack()
        self.b1=Button(self.window,text="GO TO CHECKOUT PAGE",bg="dark green",padx=1080,pady=10,command=self.newwin).pack()
        
        self.window.mainloop()

    def newwin(self):
        global k
        file_name ="C:\\Users\\kaifm\\Desktop\\gre\\cost.txt"
        with open(file_name,'rt') as fpt:
            g = fpt.read().rstrip('\n').split('\n')

        for i in range(len(g)):
            g[i]=int(g[i])

        sum=0
        for i in range(len(k)):
           
            sum=sum+g[k[i]-1]
        sum=str(sum)

        
        self.w=Tk()
        self.w.iconbitmap("C:\\Users\\kaifm\\Downloads\\Custom-Icon-Design-Pretty-Office-11-Coin-us-dollar.ico")
        self.w.title("payment information")
        self.w.geometry('1920x1080')     
        labl1=Label(self.w,text="Enter the card number",fg='black',font=20)
        lab5=Label(self.w,text="--",font=20,fg='black')
        lab6=Label(self.w,text="--",font=20,fg='black')
        lab7=Label(self.w,text="--",font=20,fg='black')
        
        lab5.place(x=600,y=50)
        lab6.place(x=750,y=50)
        lab7.place(x=900,y=50)
        
        
        e1=Entry(self.w,width=10,font=20)
        e5=Entry(self.w,width=10,font=20)
        e6=Entry(self.w,width=10,font=20)
        e7=Entry(self.w,width=10,font=20)
        e5.place(x=630,y=50)
        e6.place(x=780,y=50)
        e7.place(x=930,y=50)
        labl1.place(x=650,y=0)
        e1.place(x=480,y=50)
        labl2=Label(self.w,text="Enter the security code",fg='black',font=20)
        e2=Entry(self.w,width=10,font=20)
        labl2.place(x=630,y=100)
        e2.place(x=670,y=150)
        labl3=Label(self.w,text="Enter the expiration date",fg='black',font=20)
        e3=Entry(self.w,width=10,font=20)
        e8=Entry(self.w,width=10,font=20)
        e8.place(x=740,y=250)
        lab8=Label(self.w,text="/",font=20,fg='black')
        lab8.place(x=710,y=250)
        labl3.place(x=620,y=200)
        e3.place(x=590,y=250)
        labl4=Label(self.w,text="Enter the card holders name",fg='black',font=20)
        e4=Entry(self.w,width=15,font=20)
        e9=Entry(self.w,width=15,font=20)
        labx=Label(self.w,text="|",font=20,fg='black')
        labx.place(x=610,y=350)
        laby=Entry(self.w,width=15,font=20)
        laby.place(x=620,y=350)
        labz=Label(self.w,text="|",font=20,fg='black')
        labz.place(x=790,y=350)
        labl4.place(x=600,y=300)
        e4.place(x=450,y=350)
        labv=Entry(self.w,font=20,width=15)
        labv.place(x=800,y=350)
        e1.get()#card number first field check done
        e2.get()#cvv code check done
        e3.get()#exp first field check done
        e4.get()#card name first field check done
        e5.get()#card number second field check done
        e6.get()#card number 3rd field check done
        e7.get()#card number lase field check done
        e8.get()#exp second field check done
        laby.get()#card holder name middle field check done
        labv.get()#card holder name last field check done

        if sum==0:
            labl5=Label(self.w,text="The amount to be paid is"+' $0',bg='blue',fg='white',font=20)
            labl5.place(x=600,y=450)
        else:
            labl5=Label(self.w,text="The amount to be paid is $"+sum,bg='blue',fg='white',font=20)
            labl5.place(x=600,y=450)

        def change():
            k=[]
            
        def check(a,b,c,d,e,f,g,h,i,j,sum):
             now=datetime.now()
             v=now.time()
             v=str(v)
             x=now.date()
             x=str(x)
             now=str(now)
             f=int(f)
             
             if(len(a)==4 and len(b)==4 and len(c)==4 and len(d)==4 and e.isdigit() and len(e)==3 and g.isdigit() and h.isalpha() and i.isalpha() and j.isalpha() and f<13 and f>0):
                    f=str(f)
                    
                    file=open('C:\\Users\\kaifm\\Desktop\\gre\\counter.txt','r')
                    n=file.read()
                    file.close()
                    
                    
                    file=open('C:\\Users\\kaifm\\Desktop\\gre\\detail.txt','a') 
                    a=str(a)
                    b=str(b)
                    c=str(c)
                    d=str(d)
                    e=str(e)
                    f=str(f)
                    g=str(g)
                    h=str(h)
                    i=str(i)
                    j=str(j)
                    file.write(a)
                    file.write(b)
                    file.write(c)
                    file.write(d)
                    e1.delete(0,END)
                    e5.delete(0,END)
                    e6.delete(0,END)
                    e7.delete(0,END)
                    file.write(' | ')
                    file.write(e)
                    e2.delete(0,END)
                    file.write(' | ')
                    file.write(f)
                    file.write('/')
                    file.write(g)
                    e3.delete(0,END)
                    e8.delete(0,END)
                    file.write(' | ')
                    file.write(h)
                    file.write(i)
                    file.write(j)
                    e4.delete(0,END)
                    laby.delete(0,END)
                    labv.delete(0,END)
                    file.write(' | ')
                    file.write('$')
                    file.write(sum)
                    file.write(' | ')
                    file.write(now)
                    file.write(' | ')
                    file.write(n)
                    file.write(' ')
                    file.write('\n')
                    file.close()
                    file=open('C:\\Users\\kaifm\\Desktop\\gre\\counter.txt','w')
                    t=str(n)
                    n=int(n)
                    n=n+1
                    n=str(n)
                    file.write(n)
                    file.close()
                    my_pdf=FPDF()
                    my_pdf.add_page()
                    my_pdf.set_font("Arial",size=29)
                    my_pdf.cell(0,5,txt="XYZ Super Market",ln=1,align='C')
                    my_pdf.set_font("Arial",size=12)
                    my_pdf.cell(10,10,txt="date",ln=2)
                    my_pdf.cell(0,0,txt=x,ln=2,align='R')
                    my_pdf.cell(0,5,txt="time",ln=3)
                    my_pdf.cell(0,5,txt=v,ln=3,align='R')
                    my_pdf.cell(0,5,txt="bill number",ln=4)
                    my_pdf.cell(0,5,txt=t,ln=4,align='R')
                    my_pdf.cell(0,5,txt="itmes",ln=5)
                    my_pdf.cell(0,5,txt=q,ln=5,align='R')

                    my_pdf.cell(0,5,txt="total cost",ln=8)
                    my_pdf.cell(0,5,txt=sum,ln=8,align='R')
                    my_pdf.cell(0,5,txt="payers name",ln=9)
                    my_pdf.cell(0,5,txt=d,ln=9,align='R')
                    my_pdf.output("okay.pdf")
            else:
                    messagebox.showinfo("Invalid","Please enter the right information")


        btn1=Button(self.w,text="PAY",bg='green',fg='white',padx=48,command=lambda:check(e1.get(),e5.get(),e6.get(),e7.get(),e2.get(),e3.get(),e8.get(),e4.get(),laby.get(),labv.get(),sum))
        btn1.place(x=600,y=500)

        btn2=Button(self.w,text="exit",bg='red',fg='white',padx=50,command=self.w.destroy)
        btn2.place(x=750,y=500)

        btnx=Button(self.w,text="Next order?",bg='white',fg='black',command=change)
        btnx.place(x=700,y=700)

    def qt(self):
        
        self.window.destroy()
    
    def update(self):
       isTrue,frame=self.vid.getFrame()

       font_scale=1
       font = cv2.FONT_HERSHEY_PLAIN

       ClassIndex, confidece, bbox = model.detect(frame,confThreshold=0.64)
       global k
       k=[]
       global q
       q=[]
       
       if (len(ClassIndex)!=0):
        for ClassInd,conf,boxes in zip(ClassIndex.flatten(),confidece.flatten(),bbox):
            if (ClassInd<=81):
              
                    k.append(ClassInd)
                    q.append(classLabels[ClassInd-1])
                    cv2.rectangle(frame,boxes,(255,0,0),1)
                    cv2.putText(frame,classLabels[ClassInd-1],(boxes[0]+10,boxes[1]+20), font,fontScale= font_scale,color=(255,255,255), thickness=1)
                
        k=set(k)
        k=list(k)
        q=str(q)
        
        
      
        if isTrue:
            self.photo= ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(750,300,image=self.photo,anchor=CENTER)

        
       self.window.after(1, self.update)
       

#==================================================

class MyVideoCapture:
    def __init__(self,video_source="C:\\Users\\kaifm\\Downloads\\d.mp4"):
        self.vid=cv2.VideoCapture(video_source)

        self.width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def getFrame(self):
        if self.vid.isOpened():
            isTrue,frame=self.vid.read()
            if isTrue:
                return(isTrue,cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)) 
            else:
                return(isTrue,None)
        else:
            return(isTrue,None)
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__=="__main__":
    
    config_file = 'C:\\Users\\kaifm\\Desktop\\new det\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    frozen_model = 'C:\\Users\\kaifm\\Desktop\\new det\\frozen_inference_graph.pb'
    model = cv2.dnn_DetectionModel(frozen_model,config_file)
    classLabels = []
    file_name ="C:\\Users\\kaifm\\Desktop\\new det\\coco_labels.txt"
    with open(file_name,'rt') as fpt:
        classLabels = fpt.read().rstrip('\n').split('\n')
    model.setInputSize(320,320)
    model.setInputScale(1.0/127.5) 
    model.setInputMean((127.5,127.5,127.5))
    model.setInputSwapRB(True)
    root=Tk()
   
    root["bg"]='black'
    
    root.title("WELCOME")
    root.iconbitmap("C:\\Users\\kaifm\\Downloads\\Martz90-Circle-Camera.ico")
    root.geometry("320x320")

    root.resizable(0,0)
    
    lab0=Label(root,text='',bg='black',height=3)
    lab0.pack()

    labl=Label(root,text="WELCOME",bg='black',fg='red')
    labl.pack()


    labl1=Label(root,text="Enter the User Id",bg='black',fg='white')
    e1=Entry(root,width=50,bg='black',fg='white')
    labl1.pack()
    e1.pack()

    labl2=Label(root,text="Enter the password",bg='black',fg='white')
    e2=Entry(root,width=50,bg='black',fg='white')
    labl2.pack()
    e2.pack()
    labl3=Label(root,text='',bg='black')
    labl3.pack()


    def check(a,b):
        if(a=='' and b==''):
            e1.delete(0,END)
            e2.delete(0,END)
            root.destroy()
            App()
        else:
            messagebox.showinfo("Warning","Please enter the right information")
  
    btn1=Button(root,text="Login",bg='green',fg='white',padx=132,height=2,command=lambda:check(e1.get(),e2.get()))
    btn1.pack()
   


root.mainloop()