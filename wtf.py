import datetime

arr = [('how to win friends and influence people', 'dale carnegie', datetime.date(2022, 12, 16), 1, 0), ('fqlsdkfq', 'lsqdkjfq', datetime.date(2022, 12, 20), 1, 0), ('atomic habits', 'james clear', datetime.date(2022, 12, 18), 1, 0), ('12 rules for life', 'jordan peterson', datetime.date(2022, 12, 19), 4, 0), ('azerty', 'azerty', datetime.date(2022, 12, 19), 7, 0), ('qwerty', 'qwerty', datetime.date(2022, 12, 19), 4, 0)]
nr = []

for i in arr : 
    xr = []
    for j in range(len(i)) : 
        if(j == 2) : 
            xr.append(str(i[j]))
        else : 
            xr.append(i[j])
    nr.append(xr)
        

print(nr)