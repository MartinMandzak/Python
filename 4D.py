import math, tkinter, random, time, sys
from tkinter import *

# Canvas CFG

main = Tk()
main.title('4D/3D projection')

bgcolor = "#%02x%02x%02x" % (10 ,10 ,10)
whitecolor = "#%02x%02x%02x" % (255 ,255 ,255)
tesseractcolor = whitecolor


width = 550
height = width
main.attributes('-fullscreen', True)


cx = width/2
cy = height/2

add = width/2+50

cnv = tkinter.Canvas(main, width=width+add, height=height+height/6)
cnv.configure(background=bgcolor)
cnv.pack()

sliderr = 10
sliderpos = width-100

def draw():
    global whitecolor, sliderr, sliderpos, bgcolor
    global q, qXY, qYZ, qXZ, qWX, qWY, qWZ, sXY, sYZ, sXZ, sWX, sWY, sWZ
    cnv.configure(background=bgcolor)
    cnv.delete("draw")
    cnv.create_line(width,0,width,height,fill=whitecolor, tags="draw")
    cnv.create_line(width+add*(1/2),0,width+add*(1/2),height,fill=whitecolor, tags="draw")
    cnv.create_line(0,height,width+add,height,fill=whitecolor, tags="draw")
    cnv.create_line(width,height,width,height+height/6,fill=whitecolor, tags="draw")
    cnv.create_line(width/2,height,width/2,height+height/6,fill=whitecolor, tags="draw")

    cnv.create_line(100,50,width-100,50,fill=whitecolor, tags="draw")
    cnv.create_line(100,40,100,60,fill=whitecolor, tags="draw")
    cnv.create_line(height-100,40,height-100,60,fill=whitecolor, tags="draw")

    for i in range(1,6):
        cnv.create_line(width,i*(height/6),width+add,i*(height/6),fill=whitecolor, tags="draw")

    cnv.create_text(width+add/4,height*(1/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "XY", tags="draw")
    cnv.create_text(width+add/4,height*(3/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "YZ", tags="draw")
    cnv.create_text(width+add/4,height*(5/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "XZ", tags="draw")
    cnv.create_text(width+add/4,height*(7/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "WX", tags="draw")
    cnv.create_text(width+add/4,height*(9/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "WY", tags="draw")
    cnv.create_text(width+add/4,height*(11/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "WZ", tags="draw")
    cnv.create_text((width)/4,height*(13/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "START / STOP", tags="draw")
    cnv.create_text(3*(width/4),height*(13/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "3D / 4D", tags="draw")
    cnv.create_text(width+add/2,height*(13/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "RESTART", tags="draw")

    cnv.create_oval(sliderpos-sliderr,50-sliderr,sliderpos+sliderr,50+sliderr,fill=whitecolor,tags=("sli","draw"))

    qXY = 0
    qYZ = 0
    qXZ = 0
    qWX = 0
    qWY = 0
    qWZ = 0

    sXY = 0
    sYZ = 0
    sXZ = 0
    sWX = 0
    sWY = 0
    sWZ = 0


draw()

main.bind("<F1>",exit)

q = 0.03

anglexy = 0
angleyz = 0
anglexz = 0
anglexw = 0
angleyw = 0
anglezw = 0

anglex = -(math.pi)/2
angley = 0 
anglez = 0

# Matrix Multiplication

def MatMultVec(a,b):
    colsA = len(a[0])
    rowsA = len(a)
    colsB = 1
    rowsB = len(b)

    if (colsA != rowsB):
        print("colsA =/= rowsB")
        return None

    m = rowsA
    result = [0]*m
    for i in range(0,rowsA):
        s = 0
        for k in range(0,colsA):
            s += (a[i][k] * b[k])
        result[i] = s
    return result

def VecMultMat(a,b):
    colsA = 1
    rowsA = len(a)
    colsB = len(b)
    rowsB = 1


    n = colsB
    m = rowsA
    result = []
    for i in range(0,n):
        result.append([0]*m)
    for i in range(0,rowsA):
        for j in range(0,colsB):
            s = 0
            s += (a[i] * b[j])
            result[i][j] = s
    return result

def matrixMult(a,b):

    try:
        colsA = len(a[0])
    except TypeError:
        return VecMultMat(a,b)
        
    rowsA = len(a)

    try:
        colsB = len(b[0])
    except TypeError:
        return MatMultVec(a,b)
        

    rowsB = len(b)

    if (colsA != rowsB):
        print("colsA =/= rowsB")
        return None

    n = colsB
    m = rowsA
    result = []
    for i in range(0,n):
        result.append([0]*m)
    for i in range(0,rowsA):
        for j in range(0,colsB):
            s = 0
            for k in range(0,colsA):
                s += (a[i][k] * b[k][j])
            result[i][j] = s
    return result

# Tesseract obj

points = [0]*16
points[0]  = ( -1,  -1, -1,  1)
points[1]  = (  1,  -1, -1,  1)
points[2]  = (  1,   1, -1,  1)
points[3]  = ( -1,   1, -1,  1)
points[4]  = ( -1,  -1,  1,  1)
points[5]  = (  1,  -1,  1,  1)
points[6]  = (  1,   1,  1,  1)
points[7]  = ( -1,   1,  1,  1)
points[8]  = ( -1,  -1, -1, -1)
points[9]  = (  1,  -1, -1, -1)
points[10] = (  1,   1, -1, -1)
points[11] = ( -1,   1, -1, -1)
points[12] = ( -1,  -1,  1, -1)
points[13] = (  1,  -1,  1, -1)
points[14] = (  1,   1,  1, -1)
points[15] = ( -1,   1,  1, -1)

projection    = [0]*2
projection[0] = (1,0,0)
projection[1] = (0,1,0)

radius = width/140
r = radius

e = len(points)

def create_offsets():
    global menux, menuy, whitecolor
    cnv.create_rectangle(menux+200,menuy-350,menux+500,menuy+350,outline=whitecolor,tags=("offsets","menu"))
    for i in range(-1,5):
        cnv.create_line(menux+200,menuy-150+i*100,menux+500,menuy-150+i*100,fill=whitecolor,tags=("offsets","menu"))
    cnv.create_text(menux+350,menuy-300,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "DEFAULT", tags=("offsets","menu"))
    cnv.create_text(menux+250,menuy-200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "X", tags=("offsets","menu"))
    cnv.create_text(menux+250,menuy,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "Y", tags=("offsets","menu"))
    cnv.create_text(menux+250,menuy+200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "Z", tags=("offsets","menu"))
    for i in range(0,3):
        cnv.create_line(menux+220,menuy-100+200*i,menux+480,menuy-100+200*i,fill=whitecolor,tags=("offsets","menu"))
        cnv.create_line(menux+220,menuy-100+200*i-10,menux+220,menuy-100+200*i+10,fill=whitecolor,tags=("offsets","menu"))
        cnv.create_line(menux+480,menuy-100+200*i-10,menux+480,menuy-100+200*i+10,fill=whitecolor,tags=("offsets","menu"))
        cnv.create_text(menux+300,menuy-200+200*i,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "=", tags=("offsets","menu"))

    cnv.create_oval(sliderposX-sliderr,menuy-100-sliderr,sliderposX+sliderr,menuy-100+sliderr,fill=whitecolor,tags=("sliX","offsets","menu"))
    cnv.create_oval(sliderposY-sliderr,menuy+100-sliderr,sliderposY+sliderr,menuy+100+sliderr,fill=whitecolor,tags=("sliY","menu","offsets"))
    cnv.create_oval(sliderposZ-sliderr,menuy+300-sliderr,sliderposZ+sliderr,menuy+300+sliderr,fill=whitecolor,tags=("sliZ","menu","offsets"))

    anglex = ((sliderposX-(menux+350))/130)*(math.pi/2)
    if anglex > 1.5:
        anglex = math.pi/2
    if anglex < -1.5:
        anglex = -math.pi/2
    if -0.1 < anglex < 0.1:
        anglex = 0
    roundanglex = round(anglex*1000)/1000

    angley = ((sliderposY-(menux+350))/130)*(math.pi/2)
    if angley > 1.5:
        angley = math.pi/2
    if angley < -1.5:
        angley = -math.pi/2
    if -0.1 < angley < 0.1:
        angley = 0
    roundangley = round(angley*1000)/1000

    anglez = ((sliderposZ-(menux+350))/130)*(math.pi/2)
    if anglez > 1.5:
        anglez = math.pi/2
    if anglez < -1.5:
        anglez = -math.pi/2
    if -0.1 < anglez < 0.1:
        anglez = 0
    roundanglez = round(anglez*1000)/1000
    
    cnv.create_text(menux+400,menuy-200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundanglex), tags=("offsets","menu","sliX"))
    cnv.create_text(menux+400,menuy,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundangley), tags=("offsets","menu","sliY"))
    cnv.create_text(menux+400,menuy+200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundanglez), tags=("offsets","menu","sliZ"))

def create_colormode():
    global menux, menuy, whitecolor
    cnv.create_rectangle(menux+200,menuy-250,menux+500,menuy+150,outline=whitecolor,tags=("colormode","menu"))
    cnv.create_line(menux+200,menuy-150,menux+500,menuy-150,fill=whitecolor,tags=("colormode","menu"))
    cnv.create_line(menux+200,menuy-50,menux+500,menuy-50,fill=whitecolor,tags=("colormode","menu"))
    cnv.create_line(menux+200,menuy+50,menux+500,menuy+50,fill=whitecolor,tags=("colormode","menu"))
    cnv.create_text(menux+350,menuy-200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "BLACK / WHITE", tags=("colormode","menu"))
    cnv.create_text(menux+350,menuy-100,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "WHITE / BLACK", tags=("colormode","menu"))
    cnv.create_text(menux+350,menuy,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "BLACK / GREEN", tags=("colormode","menu"))
    cnv.create_text(menux+350,menuy+100,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "CUSTOM", tags=("colormode","menu"))

def create_cmodecustom():
    global menux, menuy, whitecolor, bgcolor
    cnv.create_rectangle(menux-200,menuy-400,menux-500,menuy+400,outline=whitecolor,tags=("colormode","menu","cmodecustom"))
    for i in range(0,7):
        cnv.create_line(menux-200,menuy-300+100*i,menux-500,menuy-300+100*i,fill=whitecolor,tags=("colormode","menu","cmodecustom"))
    cnv.create_text(menux-400,menuy-350,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "BG COLOR", tags=("colormode","menu","cmodecustom"))
    cnv.create_text(menux-400,menuy+50,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "2nd COLOR", tags=("colormode","menu","cmodecustom"))
    cnv.create_line(menux-300,menuy-300,menux-300,menuy-400,fill=whitecolor,tags=("colormode","menu","cmodecustom"))
    cnv.create_line(menux-300,menuy,menux-300,menuy+100,fill=whitecolor,tags=("colormode","menu","cmodecustom"))

    cnv.create_rectangle(menux-290,menuy-390,menux-210,menuy-310,fill=bgcolor,width=0,tags=("colormode","menu","cmodecustom","bgcolormode"))
    cnv.create_rectangle(menux-290,menuy+10,menux-210,menuy+90,fill=whitecolor,width=0,tags=("colormode","menu","cmodecustom","wcolormode"))
    
    for i in range(0,3):
        cnv.create_line(menux-220,menuy-250+100*i,menux-480,menuy-250+100*i,fill=whitecolor,tags=("colormode","menu","cmodecustom"))
        cnv.create_line(menux-220,menuy-250+100*i-10,menux-220,menuy-250+100*i+10,fill=whitecolor,tags=("colormode","menu","cmodecustom"))
        cnv.create_line(menux-480,menuy-250+100*i-10,menux-480,menuy-250+100*i+10,fill=whitecolor,tags=("colormode","menu","cmodecustom"))
    for i in range(0,3):
        cnv.create_line(menux-220,menuy+150+100*i,menux-480,menuy+150+100*i,fill=whitecolor,tags=("colormode","menu","cmodecustom"))
        cnv.create_line(menux-220,menuy+150+100*i-10,menux-220,menuy+150+100*i+10,fill=whitecolor,tags=("colormode","menu","cmodecustom"))
        cnv.create_line(menux-480,menuy+150+100*i-10,menux-480,menuy+150+100*i+10,fill=whitecolor,tags=("colormode","menu","cmodecustom"))

    global bg1, bg2, bg3
    global sliderposR1, sliderposG1, sliderposB1

    global w1, w2, w3
    global sliderposR2, sliderposG2, sliderposB2

    global tesseractcolor
    
    cnv.delete("sliR1")
    cnv.create_oval(sliderposR1-sliderr,menuy-250-sliderr,sliderposR1+sliderr,menuy-250+sliderr,fill=whitecolor,tags=("sliR1","colormode","menu","cmodecustom"))
    bg1 = int(((((sliderposR1-menux+350)/130)*255)+255)/2)
    cnv.delete("bgcolormode")
    bgcolor = "#%02x%02x%02x" % (bg1 ,bg2 ,bg3)
    cnv.create_rectangle(menux-290,menuy-390,menux-210,menuy-310,fill=bgcolor,width=0,tags=("colormode","menu","cmodecustom","bgcolormode"))
            
    cnv.delete("sliG1")
    cnv.create_oval(sliderposG1-sliderr,menuy-150-sliderr,sliderposG1+sliderr,menuy-150+sliderr,fill=whitecolor,tags=("sliG1","colormode","menu","cmodecustom"))
    bg2 = int(((((sliderposG1-menux+350)/130)*255)+255)/2)
    cnv.delete("bgcolormode")
    bgcolor = "#%02x%02x%02x" % (bg1 ,bg2 ,bg3)
    cnv.create_rectangle(menux-290,menuy-390,menux-210,menuy-310,fill=bgcolor,width=0,tags=("colormode","menu","cmodecustom","bgcolormode"))
            
    cnv.delete("sliB1")
    cnv.create_oval(sliderposB1-sliderr,menuy-50-sliderr,sliderposB1+sliderr,menuy-50+sliderr,fill=whitecolor,tags=("sliB1","colormode","menu","cmodecustom"))
    bg3 = int(((((sliderposB1-menux+350)/130)*255)+255)/2)
    cnv.delete("bgcolormode")
    bgcolor = "#%02x%02x%02x" % (bg1 ,bg2 ,bg3)
    cnv.create_rectangle(menux-290,menuy-390,menux-210,menuy-310,fill=bgcolor,width=0,tags=("colormode","menu","cmodecustom","bgcolormode"))

    #
    cnv.delete("sliR2")
    cnv.create_oval(sliderposR2-sliderr,menuy+150-sliderr,sliderposR2+sliderr,menuy+150+sliderr,fill=whitecolor,tags=("sliR2","colormode","menu","cmodecustom"))
    w1 = int(((((sliderposR2-menux+350)/130)*255)+255)/2)
    cnv.delete("wcolormode")
    whitecolor = "#%02x%02x%02x" % (w1 ,w2 ,w3)
    tesseractcolor = whitecolor
    cnv.create_rectangle(menux-290,menuy+10,menux-210,menuy+90,fill=whitecolor,width=0,tags=("colormode","menu","cmodecustom","wcolormode"))
            
    cnv.delete("sliG2")
    cnv.create_oval(sliderposG2-sliderr,menuy+250-sliderr,sliderposG2+sliderr,menuy+250+sliderr,fill=whitecolor,tags=("sliG2","colormode","menu","cmodecustom"))
    w2 = int(((((sliderposG2-menux+350)/130)*255)+255)/2)
    cnv.delete("wcolormode")
    whitecolor = "#%02x%02x%02x" % (w1 ,w2 ,w3)
    tesseractcolor = whitecolor
    cnv.create_rectangle(menux-290,menuy+10,menux-210,menuy+90,fill=whitecolor,width=0,tags=("colormode","menu","cmodecustom","wcolormode"))
            
    cnv.delete("sliB2")
    cnv.create_oval(sliderposB2-sliderr,menuy+350-sliderr,sliderposB2+sliderr,menuy+350+sliderr,fill=whitecolor,tags=("sliB2","colormode","menu","cmodecustom"))
    w3 = int(((((sliderposB2-menux+350)/130)*255)+255)/2)
    cnv.delete("wcolormode")
    whitecolor = "#%02x%02x%02x" % (w1 ,w2 ,w3)
    tesseractcolor = whitecolor
    cnv.create_rectangle(menux-290,menuy+10,menux-210,menuy+90,fill=whitecolor,width=0,tags=("colormode","menu","cmodecustom","wcolormode"))        

def create_lines():
    global menux, menuy, whitecolor, sliderSIZE1, linesize
    global t1, t2, t3, sliderposR3, sliderposG3, sliderposB3, tesseractcolor
    cnv.create_rectangle(menux+200,menuy-250,menux+500,menuy+350,outline=whitecolor,tags=("lines","menu"))
    for i in range(0,5):
        cnv.create_line(menux+200,menuy-150+100*i,menux+500,menuy-150+100*i,fill=whitecolor,tags=("lines","menu"))
    cnv.create_text(menux+350,menuy-200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "SIZE", tags=("lines","menu"))
    cnv.create_text(menux+300,menuy,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "3rd COLOR", tags=("lines","menu"))
    cnv.create_line(menux+400,menuy-50,menux+400,menuy+50,fill=whitecolor,tags=("lines","menu"))

    cnv.create_line(menux+220,menuy-100,menux+480,menuy-100,fill=whitecolor,tags=("lines","menu"))
    cnv.create_line(menux+220,menuy-100-10,menux+220,menuy-100+10,fill=whitecolor,tags=("lines","menu"))
    cnv.create_line(menux+480,menuy-100-10,menux+480,menuy-100+10,fill=whitecolor,tags=("lines","menu"))

    for i in range(0,3):
        cnv.create_line(menux+220,menuy+100+100*i,menux+480,menuy+100+100*i,fill=whitecolor,tags=("lines","menu"))
        cnv.create_line(menux+220,menuy+100-10+100*i,menux+220,menuy+100+10+100*i,fill=whitecolor,tags=("lines","menu"))
        cnv.create_line(menux+480,menuy+100-10+100*i,menux+480,menuy+100+10+100*i,fill=whitecolor,tags=("lines","menu"))

    cnv.delete("sliS1")
    cnv.create_oval(sliderSIZE1-sliderr,menuy-100-sliderr,sliderSIZE1+sliderr,menuy-100+sliderr,fill=whitecolor,tags=("sliS1","colormode","menu","lines"))
    linesize = (((sliderSIZE1-(menux+350))/130)*5)+5

    cnv.delete("sliR3")
    cnv.create_oval(sliderposR3-sliderr,menuy+100-sliderr,sliderposR3+sliderr,menuy+100+sliderr,fill=whitecolor,tags=("sliR3","colormode","menu","cmodecustom"))
    t1 = int(((((sliderposR3-(menux+350))/130)*255)+255)/2)
    cnv.delete("tcolormode")
    tesseractcolor = "#%02x%02x%02x" % (t1 ,t2 ,t3)
    cnv.create_rectangle(menux+410,menuy+40,menux+490,menuy-40,fill=tesseractcolor,width=0,tags=("menu","lines","tcolormode"))

    cnv.delete("sliG3")
    cnv.create_oval(sliderposG3-sliderr,menuy+200-sliderr,sliderposG3+sliderr,menuy+200+sliderr,fill=whitecolor,tags=("sliG3","colormode","menu","cmodecustom"))
    t2 = int(((((sliderposG3-(menux+350))/130)*255)+255)/2)
    cnv.delete("tcolormode")
    tesseractcolor = "#%02x%02x%02x" % (t1 ,t2 ,t3)
    cnv.create_rectangle(menux+410,menuy+40,menux+490,menuy-40,fill=tesseractcolor,width=0,tags=("menu","lines","tcolormode"))

    cnv.delete("sliB3")
    cnv.create_oval(sliderposB3-sliderr,menuy+300-sliderr,sliderposB3+sliderr,menuy+300+sliderr,fill=whitecolor,tags=("sliB3","colormode","menu","cmodecustom"))
    t3 = int(((((sliderposB3-(menux+350))/130)*255)+255)/2)
    cnv.delete("tcolormode")
    tesseractcolor = "#%02x%02x%02x" % (t1 ,t2 ,t3)
    cnv.create_rectangle(menux+410,menuy+40,menux+490,menuy-40,fill=tesseractcolor,width=0,tags=("menu","lines","tcolormode"))


    
def motion(event):
    global q, qXY, qYZ, qXZ, qWX, qWY, qWZ, sXY, sYZ, sXZ, sWX, sWY, sWZ, u, whitecolor
    global anglexy, angleyz, anglexz, anglexw, angleyw, anglezw, sliderpos

    mx, my = event.x, event.y

    if h == 1:
        if   (width+add/2 < mx) and (height*(0/6) < my < height*(1/6)):
            if sXY == 0:
                sXY = 1
                qXY = q
                cnv.create_text(width+add*(3/4),height*(1/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "ON", tags=("xy","draw"))
            else:
                sXY = 0
                qXY = 0
                cnv.delete("xy")
                
        elif (width+add/2 < mx) and (height*(1/6) < my < height*(2/6)):
            if sYZ == 0:
                sYZ = 1
                qYZ = q
                cnv.create_text(width+add*(3/4),height*(3/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "ON", tags=("yz","draw"))
            else:
                sYZ = 0
                qYZ = 0
                cnv.delete("yz")
                
        elif (width+add/2 < mx) and (height*(2/6) < my < height*(3/6)):
            if sXZ == 0:
                sXZ = 1
                qXZ = q
                cnv.create_text(width+add*(3/4),height*(5/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "ON", tags=("xz","draw"))
            else:
                sXZ = 0
                qXZ = 0
                cnv.delete("xz")
                
        elif (width+add/2 < mx) and (height*(3/6) < my < height*(4/6)):
            if sWX == 0:
                sWX = 1
                qWX = q
                cnv.create_text(width+add*(3/4),height*(7/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "ON", tags=("wx","draw"))
            else:
                sWX = 0
                qWX = 0
                cnv.delete("wx")
                
        elif (width+add/2 < mx) and (height*(4/6) < my < height*(5/6)):
            if sWY == 0:
                sWY = 1
                qWY = q
                cnv.create_text(width+add*(3/4),height*(9/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "ON", tags=("wy","draw"))
            else:
                sWY = 0
                qWY = 0
                cnv.delete("wy")
                
        elif (width+add/2 < mx) and (height*(5/6) < my < height*(6/6)):
            if sWZ == 0:
                sWZ = 1
                qWZ = q
                cnv.create_text(width+add*(3/4),height*(11/12),fill=whitecolor,font=("Times","20", "italic", "bold"), text = "ON", tags=("wz","draw"))
            else:
                sWZ = 0
                qWZ = 0
                cnv.delete("wz")
                
        elif (mx < width/2) and (height*(6/6) < my < height*(7/6)):
            if u == 0:
                u = 1
            else:
                u = 0
                
        elif (width < mx) and (height*(6/6) < my < height*(7/6)):
            anglexy = 0
            angleyz = 0
            anglexz = 0
            anglexw = 0
            angleyw = 0
            anglezw = 0

        elif (width > mx > width/2) and (height*(6/6) < my < height*(7/6)):
            global e, points, anglex, angley, anglez
            if e == 16:
                points = [0]*8
                points[0]  = ( -1,  -1, -1)
                points[1]  = (  1,  -1, -1)
                points[2]  = (  1,   1, -1)
                points[3]  = ( -1,   1, -1)
                points[4]  = ( -1,  -1,  1)
                points[5]  = (  1,  -1,  1)
                points[6]  = (  1,   1,  1)
                points[7]  = ( -1,   1,  1)
                e = 8
            else:
                points = [0]*16
                points[0]  = ( -1,  -1, -1,  1)
                points[1]  = (  1,  -1, -1,  1)
                points[2]  = (  1,   1, -1,  1)
                points[3]  = ( -1,   1, -1,  1)
                points[4]  = ( -1,  -1,  1,  1)
                points[5]  = (  1,  -1,  1,  1)
                points[6]  = (  1,   1,  1,  1)
                points[7]  = ( -1,   1,  1,  1)
                points[8]  = ( -1,  -1, -1, -1)
                points[9]  = (  1,  -1, -1, -1)
                points[10] = (  1,   1, -1, -1)
                points[11] = ( -1,   1, -1, -1)
                points[12] = ( -1,  -1,  1, -1)
                points[13] = (  1,  -1,  1, -1)
                points[14] = (  1,   1,  1, -1)
                points[15] = ( -1,   1,  1, -1)
                e = 16   
                anglex = -(math.pi)/2
                angley = 0
                anglez = 0
    else:
        global menuy, menux, offH, quitv, colH, bgcolor, cmodecustom, linH, tesseractcolor

        if (menux - 150 < mx < menux + 150) and (menuy - 250 < my < menuy - 150):
            if offH == 1:
                cnv.delete("colormode","lines")
                create_offsets()
                offH = 0
                colH = 1
                cmodecustom = 1
                linH = 1
            else:
                offH = 1
                linH = 1
                cnv.delete("offsets")

        elif (offH == 0) and (menux + 200 < mx < menux + 500) and (menuy - 350 < my < menuy - 250):
            ######

            global sliderposX, sliderposY, sliderposZ

            cnv.delete("sliX","sliZ","sliY")

            sliderposX = (width+add)/2+220
            sliderposY = (width+add)/2+350
            sliderposZ = (width+add)/2+350
            
            cnv.create_oval(sliderposX-sliderr,menuy-100-sliderr,sliderposX+sliderr,menuy-100+sliderr,fill=whitecolor,tags=("sliX","offsets","menu"))
            cnv.create_oval(sliderposY-sliderr,menuy+100-sliderr,sliderposY+sliderr,menuy+100+sliderr,fill=whitecolor,tags=("sliY","menu","offsets"))
            cnv.create_oval(sliderposZ-sliderr,menuy+300-sliderr,sliderposZ+sliderr,menuy+300+sliderr,fill=whitecolor,tags=("sliZ","menu","offsets"))

            anglex = ((sliderposX-(menux+350))/130)*(math.pi/2)
            if anglex > 1.5:
                anglex = math.pi/2
            if anglex < -1.5:
                anglex = -math.pi/2
            if -0.1 < anglex < 0.1:
                anglex = 0
            roundanglex = round(anglex*1000)/1000

            angley = ((sliderposY-(menux+350))/130)*(math.pi/2)
            if angley > 1.5:
                angley = math.pi/2
            if angley < -1.5:
                angley = -math.pi/2
            if -0.1 < angley < 0.1:
                angley = 0
            roundangley = round(angley*1000)/1000

            anglez = ((sliderposZ-(menux+350))/130)*(math.pi/2)
            if anglez > 1.5:
                anglez = math.pi/2
            if anglez < -1.5:
                anglez = -math.pi/2
            if -0.1 < anglez < 0.1:
                anglez = 0
            roundanglez = round(anglez*1000)/1000

            cnv.create_text(menux+400,menuy-200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundanglex), tags=("offsets","menu","sliX"))
            cnv.create_text(menux+400,menuy,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundangley), tags=("offsets","menu","sliY"))
            cnv.create_text(menux+400,menuy+200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundanglez), tags=("offsets","menu","sliZ"))
                
        elif (menux - 150 < mx < menux + 150) and (menuy - 150 < my < menuy - 50):
            if colH == 1:
                cnv.delete("offsets","lines")
                create_colormode()
                colH = 0
                offH = 1
                linH = 1
            else:
                colH = 1
                cmodecustom = 1
                linH = 1
                cnv.delete("colormode")

        elif (menux + 200 < mx < menux + 500) and (menuy - 250 < my < menuy - 150):
            if colH == 0:
                bgcolor = "#%02x%02x%02x" % (10 ,10 ,10)
                whitecolor = "#%02x%02x%02x" % (255 ,255 ,255)
                tesseractcolor = whitecolor

        elif (menux + 200 < mx < menux + 500) and (menuy - 150 < my < menuy - 50):
            if colH == 0:
                bgcolor = "#%02x%02x%02x" % (255 ,255 ,255)
                whitecolor = "#%02x%02x%02x" % (10 ,10 ,10)
                tesseractcolor = whitecolor
                
        elif (menux + 200 < mx < menux + 500) and (menuy - 50 < my < menuy + 50):
            if colH == 0:
                bgcolor = "#%02x%02x%02x" % (10 ,10 ,10)
                whitecolor = "#%02x%02x%02x" % (0 ,255 ,0)
                tesseractcolor = whitecolor

        elif (menux + 200 < mx < menux + 500) and (menuy + 50 < my < menuy + 150):
            if colH == 0:
                if cmodecustom == 1:
                    create_cmodecustom()
                    cmodecustom = 0
                    linH = 1
                else:
                    cnv.delete("cmodecustom")
                    cmodecustom = 1
                    linH = 1

        elif (menux - 150 < mx < menux + 150) and (menuy - 50 < my < menuy + 50):
            if linH == 1:
                cnv.delete("offsets","cmodecustom","colormode")
                create_lines()
                linH = 0
                colH = 1
                offH = 1
                cmodecustom = 1
            else:
                linH = 1
                cnv.delete("lines")
                
        elif (menux - 150 < mx < menux + 150) and (menuy + 50 < my < menuy + 150):
            menu(0)

        elif (menux - 150 < mx < menux + 150) and (menuy + 150 < my < menuy + 250):
            quitv = 1


cmodecustom = 1            
offH = 1
colH = 1
linH = 1
size = width/6

def slider(event):
    global sliderpos, size, r, h, offH, sliderposX, sliderposY, sliderposZ, sliderr, whitecolor, cmodecustom, menuy, menux, bgcolor
    mx, my = event.x, event.y
    if h == 1:
        if (100 <= mx <= width-100) and (0 < my < 65):
            sliderpos = mx
            cnv.delete("sli")
            cnv.create_oval(sliderpos-sliderr,50-sliderr,sliderpos+sliderr,50+sliderr,fill=whitecolor,tags=("sli","draw"))
            size = (sliderpos+100)/6
            r = ((sliderpos+100)/(width/5))
    elif offH == 0:
        global anglex, angley, anglez
        
        if (menux+220 <= mx <= menux+480) and (menuy-150 < my < menuy-50):
            sliderposX = mx
            cnv.delete("sliX")
            cnv.create_oval(sliderposX-sliderr,menuy-100-sliderr,sliderposX+sliderr,menuy-100+sliderr,fill=whitecolor,tags=("sliX","menu","offsets"))
            anglex = ((sliderposX-(menux+350))/130)*(math.pi/2)
            if anglex > 1.5:
                anglex = math.pi/2
            if anglex < -1.5:
                anglex = -math.pi/2
            if -0.1 < anglex < 0.1:
                anglex = 0
            roundanglex = round(anglex*1000)/1000
            cnv.create_text(menux+400,menuy-200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundanglex), tags=("offsets","menu","sliX"))

        if (menux+220 <= mx <= menux+480) and (menuy+50 < my < menuy+150):
            sliderposY = mx
            cnv.delete("sliY")
            cnv.create_oval(sliderposY-sliderr,menuy+100-sliderr,sliderposY+sliderr,menuy+100+sliderr,fill=whitecolor,tags=("sliY","menu","offsets"))
            angley = ((sliderposY-(menux+350))/130)*(math.pi/2)
            if angley > 1.5:
                angley = math.pi/2
            if angley < -1.5:
                angley = -math.pi/2
            if -0.1 < angley < 0.1:
                angley = 0
            roundangley = round(angley*1000)/1000
            cnv.create_text(menux+400,menuy,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundangley), tags=("offsets","menu","sliY"))

        if (menux+220 <= mx <= menux+480) and (menuy+250 < my < menuy+350):
            sliderposZ = mx
            cnv.delete("sliZ")
            cnv.create_oval(sliderposZ-sliderr,menuy+300-sliderr,sliderposZ+sliderr,menuy+300+sliderr,fill=whitecolor,tags=("sliZ","menu","offsets"))
            anglez = ((sliderposZ-(menux+350))/130)*(math.pi/2)
            if anglez > 1.5:
                anglez = math.pi/2
            if anglez < -1.5:
                anglez = -math.pi/2
            if -0.1 < anglez < 0.1:
                anglez = 0
            roundanglez = round(anglez*1000)/1000
            cnv.create_text(menux+400,menuy+200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = str(roundanglez), tags=("offsets","menu","sliZ"))

    elif cmodecustom == 0:
        global bg1, bg2, bg3
        global sliderposR1, sliderposG1, sliderposB1
        global w1, w2, w3
        global sliderposR2, sliderposG2, sliderposB2
        global tesseractcolor
        
        if (menux-480 <= mx <= menux-220) and (menuy-300 < my < menuy-200):
            sliderposR1 = mx
            cnv.delete("sliR1")
            cnv.create_oval(sliderposR1-sliderr,menuy-250-sliderr,sliderposR1+sliderr,menuy-250+sliderr,fill=whitecolor,tags=("sliR1","colormode","menu","cmodecustom"))
            bg1 = int(((((sliderposR1-menux+350)/130)*255)+255)/2)
            cnv.delete("bgcolormode")
            bgcolor = "#%02x%02x%02x" % (bg1 ,bg2 ,bg3)
            cnv.create_rectangle(menux-290,menuy-390,menux-210,menuy-310,fill=bgcolor,width=0,tags=("colormode","menu","cmodecustom","bgcolormode"))
            
        elif (menux-480 <= mx <= menux-220) and (menuy-200 < my < menuy-100):
            sliderposG1 = mx
            cnv.delete("sliG1")
            cnv.create_oval(sliderposG1-sliderr,menuy-150-sliderr,sliderposG1+sliderr,menuy-150+sliderr,fill=whitecolor,tags=("sliG1","colormode","menu","cmodecustom"))
            bg2 = int(((((sliderposG1-menux+350)/130)*255)+255)/2)
            cnv.delete("bgcolormode")
            bgcolor = "#%02x%02x%02x" % (bg1 ,bg2 ,bg3)
            cnv.create_rectangle(menux-290,menuy-390,menux-210,menuy-310,fill=bgcolor,width=0,tags=("colormode","menu","cmodecustom","bgcolormode"))
            
        elif (menux-480 <= mx <= menux-220) and (menuy-100 < my < menuy):
            sliderposB1 = mx
            cnv.delete("sliB1")
            cnv.create_oval(sliderposB1-sliderr,menuy-50-sliderr,sliderposB1+sliderr,menuy-50+sliderr,fill=whitecolor,tags=("sliB1","colormode","menu","cmodecustom"))
            bg3 = int(((((sliderposB1-menux+350)/130)*255)+255)/2)
            cnv.delete("bgcolormode")
            bgcolor = "#%02x%02x%02x" % (bg1 ,bg2 ,bg3)
            cnv.create_rectangle(menux-290,menuy-390,menux-210,menuy-310,fill=bgcolor,width=0,tags=("colormode","menu","cmodecustom","bgcolormode"))

        #
        elif (menux-480 <= mx <= menux-220) and (menuy+100 < my < menuy+200):
            sliderposR2 = mx
            cnv.delete("sliR2")
            cnv.create_oval(sliderposR2-sliderr,menuy+150-sliderr,sliderposR2+sliderr,menuy+150+sliderr,fill=whitecolor,tags=("sliR2","colormode","menu","cmodecustom"))
            w1 = int(((((sliderposR2-menux+350)/130)*255)+255)/2)
            cnv.delete("wcolormode")
            whitecolor = "#%02x%02x%02x" % (w1 ,w2 ,w3)
            tesseractcolor = whitecolor
            cnv.create_rectangle(menux-290,menuy+10,menux-210,menuy+90,fill=whitecolor,width=0,tags=("colormode","menu","cmodecustom","wcolormode"))
            
        elif (menux-480 <= mx <= menux-220) and (menuy+200 < my < menuy+300):
            sliderposG2 = mx
            cnv.delete("sliG2")
            cnv.create_oval(sliderposG2-sliderr,menuy+250-sliderr,sliderposG2+sliderr,menuy+250+sliderr,fill=whitecolor,tags=("sliG2","colormode","menu","cmodecustom"))
            w2 = int(((((sliderposG2-menux+350)/130)*255)+255)/2)
            cnv.delete("wcolormode")
            whitecolor = "#%02x%02x%02x" % (w1 ,w2 ,w3)
            tesseractcolor = whitecolor
            cnv.create_rectangle(menux-290,menuy+10,menux-210,menuy+90,fill=whitecolor,width=0,tags=("colormode","menu","cmodecustom","wcolormode"))
            
        elif (menux-480 <= mx <= menux-220) and (menuy+300 < my < menuy+400):
            sliderposB2 = mx
            cnv.delete("sliB2")
            cnv.create_oval(sliderposB2-sliderr,menuy+350-sliderr,sliderposB2+sliderr,menuy+350+sliderr,fill=whitecolor,tags=("sliB2","colormode","menu","cmodecustom"))
            w3 = int(((((sliderposB2-menux+350)/130)*255)+255)/2)
            cnv.delete("wcolormode")
            whitecolor = "#%02x%02x%02x" % (w1 ,w2 ,w3)
            tesseractcolor = whitecolor
            cnv.create_rectangle(menux-290,menuy+10,menux-210,menuy+90,fill=whitecolor,width=0,tags=("colormode","menu","cmodecustom","wcolormode"))

    elif linH == 0:
        global sliderSIZE1, linesize
        global sliderposR3, sliderposG3, sliderposB3
        global t1, t2, t3
        
        if (menux+220 <= mx <= menux+480) and (menuy-150 < my < menuy-50):
            sliderSIZE1 = mx
            cnv.delete("sliS1")
            cnv.create_oval(sliderSIZE1-sliderr,menuy-100-sliderr,sliderSIZE1+sliderr,menuy-100+sliderr,fill=whitecolor,tags=("sliS1","menu","lines"))
            linesize = (((sliderSIZE1-(menux+350))/130)*5)+5
            
        elif (menux+220 <= mx <= menux+480) and (menuy+50 < my < menuy+150):
            sliderposR3 = mx
            cnv.delete("sliR3")
            cnv.create_oval(sliderposR3-sliderr,menuy+100-sliderr,sliderposR3+sliderr,menuy+100+sliderr,fill=whitecolor,tags=("sliR3","colormode","menu","cmodecustom"))
            t1 = int(((((sliderposR3-(menux+350))/130)*255)+255)/2)
            cnv.delete("tcolormode")
            tesseractcolor = "#%02x%02x%02x" % (t1 ,t2 ,t3)
            cnv.create_rectangle(menux+410,menuy+40,menux+490,menuy-40,fill=tesseractcolor,width=0,tags=("menu","lines","tcolormode"))

        elif (menux+220 <= mx <= menux+480) and (menuy+150 < my < menuy+250):
            sliderposG3 = mx
            cnv.delete("sliG3")
            cnv.create_oval(sliderposG3-sliderr,menuy+200-sliderr,sliderposG3+sliderr,menuy+200+sliderr,fill=whitecolor,tags=("sliG3","colormode","menu","cmodecustom"))
            t2 = int(((((sliderposG3-(menux+350))/130)*255)+255)/2)
            cnv.delete("tcolormode")
            tesseractcolor = "#%02x%02x%02x" % (t1 ,t2 ,t3)
            cnv.create_rectangle(menux+410,menuy+40,menux+490,menuy-40,fill=tesseractcolor,width=0,tags=("menu","lines","tcolormode"))

        elif (menux+220 <= mx <= menux+480) and (menuy+250 < my < menuy+350):
            sliderposB3 = mx
            cnv.delete("sliB3")
            cnv.create_oval(sliderposB3-sliderr,menuy+300-sliderr,sliderposB3+sliderr,menuy+300+sliderr,fill=whitecolor,tags=("sliB3","colormode","menu","cmodecustom"))
            t3 = int(((((sliderposB3-(menux+350))/130)*255)+255)/2)
            cnv.delete("tcolormode")
            tesseractcolor = "#%02x%02x%02x" % (t1 ,t2 ,t3)
            cnv.create_rectangle(menux+410,menuy+40,menux+490,menuy-40,fill=tesseractcolor,width=0,tags=("menu","lines","tcolormode"))


sliderSIZE1 = (width+add)/2+220
            
sliderposX = (width+add)/2+220
sliderposY = (width+add)/2+350
sliderposZ = (width+add)/2+350

sliderposR1 = (width+add)/2-480
sliderposG1 = (width+add)/2-480
sliderposB1 = (width+add)/2-480

sliderposR2 = (width+add)/2-220
sliderposG2 = (width+add)/2-220
sliderposB2 = (width+add)/2-220

sliderposR3 = (width+add)/2+480
sliderposG3 = (width+add)/2+480
sliderposB3 = (width+add)/2+480

bg1 = 10
bg2 = 10
bg3 = 10

w1 = 255
w2 = 255
w3 = 255

t1 = 255
t2 = 255
t3 = 255
        
def createmenu():
    global menux, menuy, width, height, whitecolor
    cnv.create_line(menux-150,menuy-150,menux+150,menuy-150,fill=whitecolor,tags="menu")
    cnv.create_line(menux-150,menuy+150,menux+150,menuy+150,fill=whitecolor,tags="menu")
    cnv.create_line(menux-150,menuy-50,menux+150,menuy-50,fill=whitecolor,tags="menu")
    cnv.create_line(menux-150,menuy+50,menux+150,menuy+50,fill=whitecolor,tags="menu")
    cnv.create_text(menux,menuy-200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "OFFSETS", tags="menu")
    cnv.create_text(menux,menuy-100,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "COLOR MODE", tags="menu")
    cnv.create_text(menux,menuy,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "LINES", tags="menu")
    cnv.create_text(menux,menuy+100,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "RESUME", tags="menu")
    cnv.create_text(menux,menuy+200,fill=whitecolor,font=("Times","20", "italic", "bold"), text = "QUIT", tags="menu")
    
def menu(event):
    global h, menux, menuy, whitecolor, offH, colH, cmodecustom, linH
    menux = (width+add)/2
    menuy = ((7/6)*height)/2
    if h == 1:
        cnv.create_rectangle(0,0,width+add-1,(7/6)*height,fill=bgcolor,tags="menu")
        cnv.create_rectangle(menux-150,menuy-250,menux+150,menuy+250,outline=whitecolor,tags="menu")
        h = 0
        createmenu()
    else:
        h = 1
        offH = 1
        colH = 1
        cmodecustom = 1
        linH = 1
        draw()
        cnv.delete("menu")
            
main.bind("<1>", motion)
main.bind("<B1-Motion>", slider)
main.bind('<Escape>', menu)

linesize = 0
quitv = 0
u = 0
h = 1
while True:
    if quitv == 1:
        break
        
    if h == 1:
        if e == 16:
            rotationXY = [( math.cos(anglexy), -math.sin(anglexy), 0, 0),
                         (  math.sin(anglexy),  math.cos(anglexy), 0, 0),
                         (                  0,                  0, 1, 0),
                         (                  0,                  0, 0, 1)]

            rotationYZ = [( 1,                0,                   0, 0),
                         (  0, math.cos(angleyz), -math.sin(angleyz), 0),
                         (  0, math.sin(angleyz),  math.cos(angleyz), 0),
                         (  0,                0,                   0, 1)]

            rotationXZ = [( math.cos(anglexz), 0, -math.sin(anglexz), 0),
                         (                  0, 1,                  0, 0),
                         (  math.sin(anglexz), 0,  math.cos(anglexz), 0),
                         (                  0, 0,                  0, 1)]

            rotationXW = [( math.cos(anglexw), 0, 0, -math.sin(anglexw)),
                         (                  0, 1, 0,                  0),
                         (                  0, 0, 1,                  0),
                         (  math.sin(anglexw), 0, 0,  math.cos(anglexw))]

            rotationYW = [( 1,                 0, 0,                  0),
                         (  0, math.cos(angleyw), 0, -math.sin(angleyw)),
                         (  0,                 0, 1,                  0),
                         (  0, math.sin(angleyw), 0,  math.cos(angleyw))]

            rotationZW = [( 1, 0,                 0,                  0),
                         (  0, 1,                 0,                  0),
                         (  0, 0, math.cos(anglezw), -math.sin(anglezw)),
                         (  0, 0, math.sin(anglezw),  math.cos(anglezw))]

        rotationZ = [( math.cos(anglez), -math.sin(anglez), 0),
                     ( math.sin(anglez),  math.cos(anglez), 0),
                     (                0,                 0, 1)]

        rotationX = [( 1,                0,                 0),
                     ( 0, math.cos(anglex), -math.sin(anglex)),
                     ( 0, math.sin(anglex),  math.cos(anglex))]

        rotationY = [(  math.cos(angley), 0, math.sin(angley)),
                     (                 0, 1,                0),
                     ( -math.sin(angley), 0, math.cos(angley))]
        ax = []
        ay = []
        
        for x in range(0,e):

            if e == 16:
                dist = 2
                projected2d = matrixMult(rotationXY ,points[x]  )
                projected2d = matrixMult(rotationYZ ,projected2d)
                projected2d = matrixMult(rotationXZ ,projected2d)
                projected2d = matrixMult(rotationXW ,projected2d)
                projected2d = matrixMult(rotationYW ,projected2d)
                projected2d = matrixMult(rotationZW ,projected2d)

                w = 1 / (dist - projected2d[3])
                
                projection2    = [0]*3
                projection2[0] = (w,0,0,0)
                projection2[1] = (0,w,0,0)
                projection2[2] = (0,0,w,0)

                projected2d = matrixMult(projection2,projected2d)

                projected2d = matrixMult(rotationX  ,projected2d)
            
            elif e == 8:
                projected2d = matrixMult(rotationX  ,points[x])
                
            projected2d = matrixMult(rotationY  ,projected2d)
            projected2d = matrixMult(rotationZ  ,projected2d)
            projected2d = matrixMult(projection ,projected2d)
            
            cnv.create_oval(projected2d[0]*size-r+cx,projected2d[1]*size-r+cy,
                            projected2d[0]*size+r+cx,projected2d[1]*size+r+cy,
                            fill=tesseractcolor,width=0,tags="p")

            ax.append(projected2d[0]*size+cx)
            ay.append(projected2d[1]*size+cy)

        for i in range(0,4):
            cnv.create_line(ax[i+4] ,ay[i+4] ,ax[(i+1)%4+4] ,ay[(i+1)%4+4] ,fill=tesseractcolor ,width = linesize , tags="l")
            cnv.create_line(ax[i]   ,ay[i]   ,ax[(i+1)%4]   ,ay[(i+1)%4]   ,fill=tesseractcolor ,width = linesize ,tags="l")
            cnv.create_line(ax[i]   ,ay[i]   ,ax[i+4]       ,ay[i+4]       ,fill=tesseractcolor ,width = linesize ,tags="l")

            if e == 16:
                cnv.create_line(ax[i+12],ay[i+12],ax[(i+1)%4+12],ay[(i+1)%4+12],fill=tesseractcolor ,width = linesize ,tags="l")
                cnv.create_line(ax[i+8] ,ay[i+8] ,ax[(i+1)%4+8] ,ay[(i+1)%4+8] ,fill=tesseractcolor ,width = linesize ,tags="l")
                cnv.create_line(ax[i+8] ,ay[i+8] ,ax[i+12]      ,ay[i+12]      ,fill=tesseractcolor ,width = linesize ,tags="l")
                cnv.create_line(ax[i]   ,ay[i]   ,ax[i+8]       ,ay[i+8]       ,fill=tesseractcolor ,width = linesize ,tags="l")
                cnv.create_line(ax[i+4] ,ay[i+4] ,ax[i+12]      ,ay[i+12]      ,fill=tesseractcolor ,width = linesize ,tags="l")

        if (u == 1) and (e == 16):    
            anglexy += qXY
            angleyz += qYZ
            anglexz += qXZ
            anglexw += qWX
            angleyw += qWY
            anglezw += qWZ

        if (u == 1) and (e == 8):
            anglex += q
            angley += q
            anglez += q

    cnv.update()
    cnv.delete("p","l")
    time.sleep(0.05)

main.destroy()
exit()

