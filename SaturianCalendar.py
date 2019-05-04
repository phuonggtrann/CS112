def saturianDay():
    return ["Titanday","Enceladusday","Hyperionday","Iapetusday","Mimasday","Rheaday", "Phoebeday","Janusday","Calypsoday","Kiviuqday","Atlasday","Ymirday"]
    
def takeInput():
    ansList=["yes","no"]
    startDay = (input("Enter start day:"))
    while startDay not in saturianDay(): 
        startDay = input("Sorry pls another start day:")
    isFiesta = input("Is is month Fiesta? yes/no:")
    while isFiesta not in ansList:
        isFiesta = input("Sorry pls indicate whether it's Fiesta month:")
    numDay = input("Please enter number of days: ")
    while True:
        try:
            numDay = int(numDay)
            while numDay<36 or numDay>78:
                numDay = int(input("Pls enter a whole number in range 36 to 78"))
            break
            
        except ValueError:
            numDay = int(input("Oops! Please enter a whole number: "))

    startDayIndex = saturianDay().index(startDay)
    makeCalendar(startDayIndex, numDay,isFiesta)
    
def makeCalendar(startDayIndex,numDay,isFiesta):
    Calendar = "Ti  "+"En  "+"Hy  "+"Ia  "+"Mi  "+"Rh  "+"Ph  "+"Ja  "+"Ca  "+"Ki  "+"At  "+"Ym  \n"
    day = saturianDay()
    fiestaDay=["En","Ia","Ca","At"]
    weekCount=1
    start=1
    while start!=(numDay+1):
        for x in range(len(day)):
            if numDay+1==start:
                break
            if startDayIndex>0:
                Calendar +="    "
                startDayIndex-=1
            else:
                if isFiesta == "yes" and day[x][0:2] in fiestaDay and (weekCount==2 or weekCount==4):
                    Calendar+="--  "
                else:
                    Calendar += "{:2}  ".format(start)
                start+=1
            if x==len(day)-1:
                weekCount+=1
                Calendar+="\n"
    print(Calendar)
    isContinue = input("Do you want to continue? yes/no")
    while isContinue!="yes" and isContinue!="no":
        isContinue=input("Sorry please try again:")
    if isContinue=="yes":
        takeInput()
    else:
        return None
        
takeInput()