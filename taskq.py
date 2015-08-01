#!/usr/bin/env python2

from multiprocessing import Process, Queue, Pool
from time import sleep

workq = Queue()
doneq = Queue()
errq = Queue()

def f():
    retries=0
    q = workq
    done = doneq
    err = errq

    while True:
        ### get an item from the queue
        try:
            i = q.get_nowait()
        except Queue.Empty:
            slee(.1)
            retries+=1
        else:
            retries=0
            print 'got ',i,
            ### process it
            try:
                i = process(i)
                print ', putting', i
            except Exception as e:  ### This shouldn't be a pokemon exception
                err.put((i, e))
            ### put it back in the queue
            if i:
                q.put(i)
            ### Or mark it as done
            else:
                done.put(i)
        if retries==10:
            break

def process(i):
    sleep(2) ###simulate work
    return i+1

if __name__ == '__main__':
    ###Dummy data
    workq.put(-1)
    workq.put(120)
    workq.put(0)
    workq.put(-1)
    workq.put(1)

    pool = Pool(processes=4)
    pool.apply(f)
    pool.join()

    #p = Process(target=f, args=(workq, doneq, errq))
    #p.start()
    #print q.get()    # prints "[42, None, 'hello']"
    #p.join()
