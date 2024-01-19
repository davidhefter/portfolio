### THIS CODE WAS ONLY USED FOR PLOTTING PID RESPONSE DATA TO TUNE CONTROLLER, THIS FILE ISN'T USED IN THE MAIN CODE ###
import serial 
from matplotlib import pyplot as plt

t=[]
p=[]
p_t = []
p_target = 5000 # for plotting step response, change this target to match
# p_rate = 60   # for plotting first order response, change this rate to match

with open('asdfad.csv', 'r') as file:
    for line in file:
        rownum = line.strip().split(',')
        if len(rownum)==2:
            try:
                try_t = int(rownum[0].strip())
                try_p = int(rownum[1].strip())
                p_target = p_rate*try_t
                t.append(try_t)
                p.append(try_p)
                p_t.append(p_target)
                
            except ValueError:
                pass

max_position = max(p)
rise_time = t[p.index(max_position)]
for i in range(p.index(max_position), len(p)):
    if abs((p[i]-p_target)/p_target)<.02:
        settle_index = i
        break

# for plotting step response
sett_position = p[settle_index]
sett_time = t[settle_index]
print(rise_time)
print(sett_time)
print("% overshoot:", (max_position-p_target)/p_target*100)
print("rise time (ms):", rise_time)
plt.plot(t,p)
plt.plot(t,p_t)
plt.text(rise_time,max_position-300,"<--  Peak time: %dms\n     %% Overshoot: %.2f%%" % (rise_time, (max_position-p_target)/p_target*100))
plt.text(sett_time,sett_position,"<--  Settling time: %dms" % (sett_time))
plt.ylabel('Position (Ticks)')
plt.xlabel('Time (ms)')
plt.title('First Order Step Response')
plt.show()

# for plotting first order response
# plt.plot(t,p)
# plt.plot(t,p_t)
# plt.ylabel('Position (Ticks)')
# plt.xlabel('Time (ms)')
# plt.title('First Order Step Response')
# plt.show()
