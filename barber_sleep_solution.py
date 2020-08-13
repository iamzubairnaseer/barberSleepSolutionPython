import threading
import time

chairs = 5

customers = 0
working = 0

mutex = threading.Semaphore(0)
sleep = threading.Semaphore(0)
barber = threading.Semaphore(0)
ready_for_haircut = threading.Semaphore(0)

def barber_thread(): 
    global customers
    
    while True:
        if(customers == 0):
            print("\nBarbar sleeping")
            mutex.release()
            sleep.acquire()
        barber.release()
        ready_for_haircut.acquire()
        time.sleep(1)
        cutHair()
        time.sleep(2)

def customer_thread():
    global chairs
    global customers
    global working
    
    mutex.acquire()
    if(customers - 1 < chairs):
        customers += 1
        if(customers == 1):
            print("first customer comes in, awaking barber\nTotal: {}\nWaiting: {}".format(customers,customers-1))
            mutex.release()
            sleep.release()
        else:
            print("\nnew customer entered, total customers are now: {}\nTotal: {}\nWaiting: {}".format(customers,customers,customers-1))
            mutex.release()
        barber.acquire()
        working+=1
        #getHairCut()
        print("\nget hair cut called by customer{}".format(working))
        ready_for_haircut.release()
    else:
        #balk()
        print("\nnew customer came but had to leave\nSHOP IS FULL!, Waiting customers are: {}".format(customers-1))
        mutex.release()
       
def cutHair():
    global working
    global customers
    
    print("\ncutting customer{} hair".format(working))
    time.sleep(2)
    mutex.acquire()
    customers -= 1
    print("\nCustomer{} exited barber room\nTotal/Waiting: {}".format(working,customers))
    mutex.release()

def customerEntry():
    for i in range(10):
        cutomerEntryThread = threading.Thread(target=customer_thread)        
        cutomerEntryThread.start()
        time.sleep(1)

barberWorkThread = threading.Thread(target=barber_thread)
barberWorkThread.start()

EntryThread = threading.Thread(target=customerEntry)
EntryThread.start()

