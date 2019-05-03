def saturianDay():
    return ["Ti","En","Hy","Ia","Mi","Rh", "Ph","Ja","Ca","Ki","At","Ym"]
    
def takeInput():
    ansList=["yes","no"]
    startDay = (input("Enter start day: "))[0:2]
    isFiesta = input("Is is month Fiesta? yes/no: ")
    numDay = int(input("Enter number of day: "))
    while startDay[0:3] not in saturianDay() or isFiesta not in ansList or numDay<36 or numDay>78:
        startDay = input("Sorry pls try again: ")
        isFiesta = input("Sorry pls try again: ")
        numDay = input("Pls enter a number in range 36-78 ")
    startDayIndex = saturianDay().index(startDay)
    makeCalendar(startDay,startDayIndex, numDay,isFiesta)
    
def makeCalendar(startDay,startDayIndex,numDay,isFiesta):
    Calendar = "Ti\t"+"En\t"+"Hy\t"+"Ia\t"+"Mi\t"+"Rh\t"+"Ph\t"+"Ja\t"+"Ca\t"+"Ki\t"+"At\t"+"Ym\t\n"
    day = saturianDay()
    fiestaDay=["En","Ia","Ca","At"]
    weekCount=1
    start=1
    while start!=(numDay+1):
        for x in range(len(day)):
            if startDayIndex>0:
                Calendar +="  \t"
                startDayIndex-=1
            else:
                if (numDay+1)!=start:
                    if isFiesta == "yes" and day[x] in fiestaDay and (weekCount==2 or weekCount==4):
                        Calendar+="--\t"
                    else:
                        if len(str(start))<2:
                            Calendar=Calendar+" "+str(start)+"\t"
                        else:
                            Calendar += str(start)+"\t"
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