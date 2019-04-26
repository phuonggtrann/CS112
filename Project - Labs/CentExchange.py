def ChangeMaker(price, payment):
    # Write your code here
    totalPayment=0
    for i in payment:
        totalPayment+=i
    change = totalPayment-price
    coinChange=change-int(change)
    def helper(remain, result):
        temp=0
        if remain>=25:
            temp=25*int(remain//25)
            result[3]+=remain//25
            remain-=temp
        if remain>=10:
            temp=10*int(remain//10)
            result[2]+=int(remain//10)
            remain-=temp
        if remain>=5:
            temp=5*int(remain//5)
            result[1]+=int(remain//5)
            remain-=temp
        if remain>=1:
            temp=(remain)
            temp=int(remain)
            result[0]+=int(remain)
            remain-=temp
        else:
            return result
        
    return helper(int(coinChange*100)+1, [0,0,0,0])