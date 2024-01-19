'''!    @file main.py
        @brief                                  Initializes shares and then runs;
                                                    user_task.py
                                                    jam_task.py
                                                    aim_task.py
                                                    shoot_task.py
                                                
        @author                                 Hefter, David
        @author                                 OConnell, Joseph
                                                
        @date                                   October 25, 2022
'''

import user_task, cotask, task_share, gc, micropython, Jam_task, aim_task, shoot_task
#import print_task

columnNum = task_share.Share ('h', thread_protect = False, name = "columnNum")
columnNum.put(0)

rowNum = task_share.Share ('h', thread_protect = False, name = "rowNum")
rowNum.put(0)

jam = task_share.Share ('h', thread_protect = False, name = "jam")
jam.put(False)

FireSignal = task_share.Share ('h', thread_protect = False, name = "Fire Signal")
FireSignal.put(False)

LoadSignal = task_share.Share ('h', thread_protect = False, name = "Load Signal")
LoadSignal.put(False)

shoot = task_share.Share ('h', thread_protect = False, name = "Fire Signal")
shoot.put(False)

task1 = cotask.Task(user_task.taskUserFcn(columnNum, rowNum, jam, shoot, FireSignal), name = 'User Task', priority = 3, period = 5, profile = True, trace = False)
task2 = cotask.Task(Jam_task.JamTaskFcn(FireSignal, jam), name = 'Jam Task', priority = 3, period = 1, profile = True, trace = False)
task3 = cotask.Task(aim_task.AimTaskFcn(columnNum, rowNum, FireSignal, LoadSignal, shoot), name = 'Aim Task', priority = 4, period = 5, profile = True, trace = False)
task4 = cotask.Task(shoot_task.ShootTaskFcn(FireSignal, LoadSignal), name = 'Shoot Task', priority = 4, period = 5, profile = True, trace = False)

cotask.task_list.append (task1)
cotask.task_list.append (task2)
cotask.task_list.append (task3)
cotask.task_list.append (task4)

if __name__=='__main__':
    micropython.alloc_emergency_exception_buf(100)
    
    gc.collect ()
    
    while True:
    
        try:
            cotask.task_list.pri_sched ()
                
        except KeyboardInterrupt:
            break
    
    

    print("Program Terminating")