
import bs4
import urllib.parse as ulp
import urllib.request as ulr
import urllib.error as ule
import http.cookiejar as hc
import itertools as it
import functools as ft

import collections
import keyring
import getpass
import png
import glob
import math
import random


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a, b)



# set to your own username to avoid the prompt
username = "fabianlischka"

baseURL = "http://projecteuler.net/"

def problemURL(N):
    return ulp.urljoin(baseURL,"problem=" + str(N))

def loginURL():
    return ulp.urljoin(baseURL,"login")


def getURL(someurl):
    req = ulr.Request(someurl)
    try:
        response = ulr.urlopen(req)
    except ule.URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    else:
        return response

def getUserPass():
    global username

    if username == None:
        username = input("Project Euler Username:\n")

    password = keyring.get_password('ProjectEulerAnswerer', username)

    if password == None:
        password = getpass.getpass("Project Euler Password:\n")
        # store the password
        keyring.set_password('ProjectEulerAnswerer', username, password)

    # the stuff that needs authorization here
    # note: the login = "Login" part seems required by Project Euler
    return dict(username = username, password = password, login = "Login")


#  r=png.Reader(file=urllib.urlopen('http://www.schaik.com/pngsuite/basn0g02.png'))
# d = dict(username="fabianlischka",password="eulerul8u")


def test1():
    cj = hc.CookieJar()
    for c in cj:
        print("before",c)
    opener = ulr.build_opener(ulr.HTTPCookieProcessor(cj))
    r = opener.open(problemURL(250))
    b0 = bs4.BeautifulSoup(r)
    for c in cj:
        print("mid",c)

    # acquire cookie & login
    request = ulr.Request(loginURL())
    r = opener.open(request)
    loginData = ulp.urlencode(getUserPass())
    loginData = loginData.encode('utf-8')
    request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
    r = opener.open(request,loginData)
    b1 = bs4.BeautifulSoup(r)

    for c in cj:
        print("after",c)


    r = opener.open(problemURL(250))
    b2 = bs4.BeautifulSoup(r)

    print("\n\n\n\n-------0:",b0)
    print("\n\n\n\n-------1:",b1)
    print("\n\n\n\n-------2:",b2)


## TO POST solution: data is: guess_301=987654321&confirm=12345
def writeModBWPng(path, suffix, pixels):
    testimageModPath = path+"-"+suffix+".png"
    with open(testimageModPath, 'wb') as f:
        w = png.Writer(len(pixels[0]), len(pixels), greyscale=True, bitdepth=1)
        w.write(f, pixels)

def findCuts(potential, N = 5):
    g = 200
    means = [i/N for i in range(1,N)] # [0.2,0.4,0.6,0.8]
    std = 0.3/N
    lowest = 999999999
    repellMin = sum((x-y)**(-2) for x,y in pairwise([0]+means+[1])) 
    for r in range(1000):
        particleXs = sorted([0.01,0.99]+[random.gauss(m,std) for m in means])[1:-1]
        coords = [math.floor(x*len(potential)) for x in particleXs]
        repell = sum((x-y)**(-2) for x,y in pairwise([0]+particleXs+[1])) - repellMin
        gravity = sum(1-potential[c] for c in coords) * g
        totalEnergy = repell + gravity
        if totalEnergy < lowest:
            lowest = totalEnergy
            best = coords
            # print(particleXs,totalEnergy,repell, gravity)
    return best

def levelPic(levels, M,N, cuts = None):
    mi, ma = min(levels), max(levels)+1
    lPic = [[1]*N for row in range(M)]
    for col in range(N):
        y = math.floor(M*(levels[col] - mi)/(ma-mi))
        lPic[y][col] = 0
        if cuts is not None:
            if col in cuts:
                for y in range(M):
                    lPic[y][col] = 0
    return lPic


def extractDigitsFromPath(testImagePath):
    return [int(c) for c in testImagePath[-9:-4]]

def truncateDigits(pixelsWB, cuts):
    cuts = [0]+cuts+[len(pixelsWB[0])]
    # print(cuts)
    pixT = list(zip(*pixelsWB)) # transpose
    digitPixs = [list(zip(*(pixT[l:r]))) for l,r in pairwise(cuts)] # note: probably have some overlap here...
    return digitPixs


def test2():
#    testimageFolder = "/Users/frl/Documents/Meins/Coding/HackerSchool/PEAnswer/captchaExamples"
    testImagePathPattern = "/Users/frl/Documents/Meins/Coding/HackerSchool/PEAnswer/captchaExamples/[0-9][0-9][0-9][0-9][0-9].png"
    digitCounter = collections.defaultdict(int)
    for testImagePath in glob.glob(testImagePathPattern):
        print(testImagePath)
        writeBW = ft.partial(writeModBWPng,testImagePath[:-4])

        i1 = png.Reader(testImagePath)
        pixels = i1.asFloat()[2]
        pixelsGray = [[(i+j+k)/3 for i,j,k in zip(*(it.islice(row,i,None,3) for i in range(3)))] for row in pixels]
        M = len(pixelsGray)
        N = len(pixelsGray[0])
        # turn pic to b/w by cutting off
        cutoff = 0.7
        pixelsBW = [[(1 if p > cutoff else 0) for p in row] for row in pixelsGray]

        colSum = [sum(col)/M for col in zip(*pixelsBW)]
        for i in range(N):
            if colSum[i] < 0.999:
                iLeft = i
                break
        for i in range(N-1,0,-1):
            if colSum[i] < 0.999:
                iRight = i+1
                break
        colSumTrunc = colSum[iLeft:iRight]


        cuts = [iLeft + c for c in findCuts(colSumTrunc)]

        digitPics = truncateDigits(pixelsBW,cuts)
        digits = extractDigitsFromPath(testImagePath)

        if True:
            for digit, digitPic in zip(digits, digitPics):
                digitPath = testImagePath[:-9]+"Digits/"+str(digit)
                suffix = "v{:0>3}".format(digitCounter[digit])
                digitCounter[digit] += 1
                # print(digit,digitPath+"-"+suffix)
                writeModBWPng(digitPath, suffix, digitPic)


        # and plot cuts
        for col in cuts:
            for y in range(M):
                pixelsBW[y][col] = 0
        writeBW("bw", pixelsBW)

        # compute average column darkness, from gray
        colSum = [sum(col) for col in zip(*pixelsGray)]
        colSumPic = levelPic(colSum,M,N,cuts)
        writeBW("cold",colSumPic)

        # compute average column darkness, from BW
        colSum = [sum(col) for col in zip(*pixelsBW)]
        colSumPic = levelPic(colSum,M,N,cuts)
        writeBW("colb",colSumPic)


        # # compute shifted copies (for gradient/energy computation)
        # su = pixelsGray[1:] + [pixelsGray[-1]]
        # sd = [pixelsGray[1]] + pixelsGray[:-1]
        # sl = [row[1:] + [row[-1]] for row in pixelsGray]
        # sr = [[row[1]] + row[:-1] for row in pixelsGray]
        # # energy
        # energy = [[ (p-u)**2 + (p-d)**2 + (p-l)**2 + (p-r)**2 for p,u,d,l,r in zip(rp,ru,rd,rl,rr)] for rp,ru,rd,rl,rr in zip(pixelsGray,su,sd,sl,sr)]
        # # determine cutoff point
        # flatEnergy = it.chain.from_iterable(energy)
        # cutoff = sorted(flatEnergy)[87*M*N//100]
        # # turn energy to b/w by cutting off
        # gradBW = [[(1 if p > cutoff else 0) for p in row] for row in energy]
        # writeBW("grad", gradBW)


def normalizeImages():
    pass
    # truncate l,r,t,b?
    # move to center of gravity
    # standard size


def moment(pixels,p,q):
    return sum( sum(x**p * y**p * pixel for y, pixel in row) for x,row in enumerate(pixels))

def cmoment(pixels,p,q,xbar,ybar):
    return sum( sum((x-xbar)**p * (y-ybar)**p * pixel for y, pixel in row) for x,row in enumerate(pixels))

def moments(pixels,p,q):
    # see http://en.wikipedia.org/wiki/Image_moment
    M00 = moment(pixels,0,0) # = µ00 (note: µ = asci 181, option-m on the Mac, not small greek letter mu)
    xbar = moment(pixels,1,0) / M00
    ybar = moment(pixels,0,1) / M00

    eta = [[0]*4 for p in range(4)]
    for p in range(4):
        for q in range(4):
            eta[p][q] = cmoment(pixesl,p,q,xbar,ybar) * M00**(-1-(i+j)/2)

    I1 = eta[2][0] + eta[0][2]
    I2 = (eta[2][0] - eta[0][2])**2 + 4*eta[1][1]**2
    I8 = eta[1][1]*( (eta[3][0]+eta[1][2])**2 - (eta[0][3]+eta[2][1])**2) - (eta[2][0]-eta[0][2])*(eta[3][0]-eta[1][2])*(eta[0][3]-eta[2][1])
    I4 = (eta[3][0]+eta[1][2])**2 + (eta[2][1]+eta[0][3])**2
    return (M00, I1,I2,I8,I4)


def featureExtraction():
    pass
    # intensity
    # symmetry
    # eigenvalues?



if __name__ == "__main__":
    # test1()
    test2()

