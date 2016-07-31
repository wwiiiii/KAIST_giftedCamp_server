from PIL import Image
from distort import *
from bisect import *
import Queue
import time
import numpy as np

black = (255,255,255)
maxdiff = 100
path = 'C:\Users\q\Desktop\ocrtemp\\'

def isSame(a,b,c,d,e,f,mydiff = maxdiff):
    diff = abs(a-d) + abs(b-e) + abs(c-f)
    return diff < mydiff

def isSameTuple(p1,p2):
    a,b,c = p1; d,e,f = p2
    return isSame(a,b,c,d,e,f)

def addColor(colorList,r,g,b):
    for i in range(len(colorList)):
        r1,g1,b1,cnt1 = colorList[i][0], colorList[i][1],colorList[i][2],colorList[i][3]
        if isSame(r1,g1,b1,r,g,b):
            colorList[i] = [r1,g1,b1,cnt1+1]
            return
    colorList.append([r,g,b,1])

def ft(a):
    return max(0,min(255,a))

GRAD = 5

def Extract(img, r0,g0,b0):
    newimg = Image.new('RGB',img.size,"white")
    width, height = img.size
    newpx = newimg.load()
    imgpx = img.load()
    for i in range(width):
        for j in range(height):
            r,g,b = imgpx[i,j]
            if isSame(r,g,b,r0,g0,b0):
                newpx[i,j] = imgpx[i,j]
    return newimg

#[[0,1,0],[1,-4,1],[0,1,0]]

def ImageFilter(img, filter, ratio):
    newimg = Image.new('RGB', img.size, "white")
    newpx = newimg.load(); imgpx = img.load()
    width, height = img.size
    for i in range(1,width-1):
        for j in range(1,height-1):
            r,g,b, = 0,0,0
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    rr,gg,bb = imgpx[i+dx,j+dy]
                    #print dx,dy,rr,gg,bb
                    r += rr*filter[dx+1][dy+1]; g += gg*filter[dx+1][dy+1];b += bb*filter[dx+1][dy+1];
            #print ft(r), ft(g), ft(b)
            newpx[i,j] = (ft(r/ratio),ft(g/ratio),ft(b/ratio))
    return newimg

def Binary(img):
    imgpx = img.load(); width,height = img.size
    newimg = Image.new('RGB', img.size, "white")
    newpx = newimg.load()
    for i in range(1,width-1):
        for j in range(1, height-1):
            r,g,b = imgpx[i,j]
            if r+g+b < 255+127: newpx[i,j] = (0,0,0)
    return newimg

THRES = 200

def Contrast(img, GRAD):
    imgpx = img.load(); width,height = img.size
    for i in range(1,width-1):
        for j in range(1,height-1):
            r,g,b = imgpx[i,j]; r1,g1,b1=r,g,b
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    r2,g2,b2 = imgpx[i+dx,j+dy]
                    if isSame(r,g,b,r2,g2,b2): continue
                    if r-r2 >= THRES and g-g2>=THRES and b-b2>=THRES:
                        imgpx[i+dx,j+dy] = (0,0,0)
                        r1,g1,b1 = 255,255,255
                    elif r2-r>= THRES and g2-g >=THRES and b2-b>=THRES:
                        imgpx[i+dx,j+dx] = (255,255,255)
                        r1,g1,b1=0,0,0
            imgpx[i,j]=(ft(r1),ft(g1),ft(b1))
    return img

def ImageRemoveBg(img, rt,gt,bt):
    imgpx = img.load();
    width, height = img.size
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            r, g, b = imgpx[i,j]
            if isSame(r,g,b,rt,gt,bt):
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        chk[i+dx][j+dy] += 1
    for i in range(1,width-1):
        for j in range(1,height-1):
            if chk[i][j] == 9:
                imgpx[i,j] = (255,255,255)

bfsdiff = 80


def bfs(img, i, j):
    imgpx = img.load(); q = Queue.Queue()
    width, height = img.size
    q.put([i,j])
    ddx = [1,-1,0,0]; ddy = [0,0,1,-1]
    while not q.empty():
        now = q.get(); 
        r,g,b = imgpx[now[0],now[1]];
        while r==255 and g==255 and b==255 and not q.empty():
            now = q.get(); r,g,b = imgpx[now[0],now[1]];
        if r==255 and g==255 and b==255: continue;
        for i in range(4):
            dx = ddx[i]; dy =ddy[i];
            if now[0]+dx <0 or now[0]+dx>=width or now[1]+dy<0 or now[1]+dy>=height: continue
            r1,g1,b1 = imgpx[now[0]+dx, now[1]+dy]
            if isSame(r,g,b,r1,g1,b1,bfsdiff):
                q.put([i+dx,j+dy])
        imgpx[now[0], now[1]] = (255,255,255)

def ImageRemoveBgBfs(img, rt,gt,bt):
    imgpx = img.load()
    width, height = img.size
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            r, g, b = imgpx[i,j]
            if isSame(r,g,b,rt,gt,bt,bfsdiff):
                t1 = time.time()
                bfs(img,i,j)
                #print 'bfs : ' + str(time.time()-t1)
    return img
    


def ImageReinforce(img):
    imgpx = img.load();
    width, height = img.size
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            r, g, b = imgpx[i,j]
            if isSame(r,g,b,0,0,0):
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        chk[i+dx][j+dy] += 1
    i = 1;
    while i < width-1:
        j = 1;
        while j < height-1:
            if chk[i][j] >= 4:
                imgpx[i,j] = (0,0,0)
            j+=1
        i+=1

def ImageRemoveBgMedian(img,colorList):
    imgpx = img.load(); width, height = img.size
    list = [];
    for r,g,b,c in colorList:
        list.append(r+g+b)
    list.sort()
    if len(list) > 2: threshold = (list[1] + list[2])/2;
    else: threshold = (list[0] + list[1])/2;
    for i in range(width):
        for j in range(height):
            r,g,b = imgpx[i,j];
            if r+g+b > threshold: imgpx[i,j] = (255,255,255)
            elif r+g+b < threshold: imgpx[i,j]=(0,0,0)
    return img

def ImageReinforceGray(img):
    imgpx = img.load();
    width, height = img.size
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            a = imgpx[i,j]
            if a == 0:
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        chk[i+dx][j+dy] += 1
    i = 1;
    while i < width-1:
        j = 1;
        while j < height-1:
            if chk[i][j] >= 4:
                imgpx[i,j] = 0
            j+=1
        i+=1
def MedianFilter(img):
    newimg = Image.new('RGB', img.size, "white")
    newpx = newimg.load(); imgpx = img.load()
    width, height = img.size
    for i in range(1,width-1):
        for j in range(1,height-1):
            pixlist = []
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    r,g,b = imgpx[i,j];
                    pixlist.append([(r,g,b),r+g+b])
            sorted(pixlist, key=lambda a:a[1])
            newpx[i,j] = pixlist[3][0]
    return newimg

def MedianFilterGray(img):
    newimg = Image.new('L', img.size, 255)
    newpx = newimg.load(); imgpx = img.load()
    width, height = img.size
    for i in range(1,width-1):
        for j in range(1,height-1):
            pixlist = []
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    pixlist.append(imgpx[i+dx,j+dy])
            pixlist.sort()
            newpx[i,j] = pixlist[4]
    return newimg

def ImagePreprocessing2(img):
    imgpx = img.load();
    width, height = img.size
    colorList = []
    t1=time.time()
    for i in range(width):
        for j in range(height):
            r, g, b = imgpx[i,j]
            addColor(colorList, r, g, b)
    colorList = sorted(colorList, key=lambda arg1:arg1[3],reverse=True)
    cnt = 0
    for i in colorList:
        cnt+=1
        r,g,b=i[0],i[1],i[2]
        timg = Image.new('RGB',(100,100),(r,g,b))
        timg.save(path+'color'+str(cnt)+'.bmp')
    print colorList
    print 'list', time.time() - t1;t1 = time.time()
    # first route : bgmedian => blur => binary => reinforce
    # second route : bgbfs => binary => reinforce
    FAST = False
    if FAST == True:
        img = ImageRemoveBgMedian(img,colorList); 
        print 'median', time.time() - t1; t1 = time.time()
        img = MedianFilter(img); 
        print 'filter', time.time() - t1;t1 = time.time()
    else:
        img = ImageRemoveBgBfs(img, colorList[0][0], colorList[0][1], colorList[0][2]); 
        print 'bgbfs', time.time() - t1;t1 = time.time()
    #img = Contrast(img, 20); 
    print 'contra', time.time() - t1; t1 = time.time()
    #img = Extract(img,0,0,0); #onlyB filter
    img = Binary(img); #B/W filter
    print 'binary', time.time() - t1;t1 = time.time()
    if FAST == True:
        for i in range(5):
            ImageReinforce(img);#
    else:
        for i in range(1):
            ImageReinforce(img);#
    print 'reinf', time.time() - t1;t1 = time.time()
    
    #img = ImageFilter(img, [[0,-2,0],[-2,+11,-2],[0,-2,0]], 3); #sharpen 1
    #img = ImageFilter(img, [[0,-1,0],[-1,+5,-1],[0,-1,0]], 1); #sharpen 2
    findBoundary(img)
    return img


def ImagePreprocessing(img):
    img = img.convert('L')
    width, height = img.size; imgpx = img.load()
    #Contrast Stretching
    maxpx = 0; minpx = 255; pixlist = range(width * (height+1)); pixcnt = 0;
    for i in range(width):
        for j in range(height):
            a = imgpx[i,j]
            if maxpx < a: maxpx = a
            if minpx > a: minpx = a
    for i in range(width):
        for j in range(height):
            a = imgpx[i,j]
            a = int((255.0/(maxpx-minpx)) * (a - minpx))
            pixlist[pixcnt] = a; pixcnt += 1;
            imgpx[i,j] = a
    pixlist = pixlist[:pixcnt]; pixlist.sort();
    print pixlist[len(pixlist)-1]
    sumpix = range(len(pixlist)); sumpix[0] = pixlist[0]; 
    for i in range(1,len(pixlist)): sumpix[i] = sumpix[i-1] + pixlist[i];
    prevmean = 0; nowmean = 0; pivot = len(pixlist)/2;
    for i in range(100000):#while True:
        print nowmean
        smallmean = sumpix[pivot] / pivot;
        bigmean = sumpix[len(pixlist)-1] - sumpix[pivot]
        bigmean /= len(pixlist)-1 - pivot
        nowmean = (smallmean + bigmean) / 2.0
        print smallmean, bigmean, nowmean
        if nowmean == prevmean: break
        prevmean = nowmean;
        pivot = bisect_left(pixlist, nowmean)
    #nowmean += 20
    for i in range(width):
        for j in range(height):
            a = imgpx[i,j]
            if a < nowmean: imgpx[i,j] = 0
            else : imgpx[i,j] = 255
    
    '''for i in range(10):
        img = MedianFilterGray(img); 
    
    for i in range(3):
            ImageReinforceGray(img);#
    '''
    #findBoundary(img.convert('RGB'))
    return img
#http://bimage.interpark.com/milti/renewPark/evtboard/20110623131612851.jpg