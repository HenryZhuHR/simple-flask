from queue import Queue
FRAME_LIST=Queue(maxsize=10)

i=0
while i<=200:
    if FRAME_LIST.full():
        FRAME_LIST.get()
    FRAME_LIST.put(i)
    i+=1
    print(FRAME_LIST.queue)
