import random
temperatures = [random.randint(26,41),random.randint(26,41),random.randint(26,41),random.randint(26,41),random.randint(26,41),random.randint(26,41),random.randint(26,41)]
days_of_the_week=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

sum=0

good_days_count=0
for i in range(7):
    sum+=temperatures[i]
    if(temperatures[i]%2==0):
        good_days_count+=1
        
highest_temp=temperatures[0]
lowest_temp=temperatures[0]
highest_temp_day=days_of_the_week[0]
lowest_temp_day=days_of_the_week[0]
for i in range(7):
	if(highest_temp<temperatures[i]):
		highest_temp=temperatures[i]
		highest_temp_day=days_of_the_week[i]
	if(lowest_temp>temperatures[i]):
		lowest_temp=temperatures[i]
		lowest_temp_day=days_of_the_week[i]
            
avg=sum/7
aboveavg=[]
for i in range(7):
    if(temperatures[i]>avg):
        aboveavg.append(days_of_the_week[i])

for i in range(7):
    print(days_of_the_week[i],": ",temperatures[i])
print(good_days_count," good days")
print("Max: ", highest_temp,"on ", highest_temp_day)
print("Min: ", lowest_temp,"on ", lowest_temp_day)
print("avg: ",avg)
print("above avg: ",aboveavg)

sort=temperatures
for i in range(7):
	j = i
	while(j<7):
		if(sort[j]<sort[i]):
			temp=sort[i]
			sort[i]=sort[j]
			sort[j]=temp
		j+=1
print(sort)



            
	

