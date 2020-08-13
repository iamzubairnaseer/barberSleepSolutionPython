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
        cutHair()

def customer_thread():
    global chairs
    global customers
    global working
    
    mutex.acquire()
    if(customers - 1 < chairs):
        customers += 1
        if(customers == 1):
            print("first customer comes in, awaking barber")
            print("Total: {}\nWaiting: {}".format(customers,customers-1))
            mutex.release()
            sleep.release()
        else:
            print("\nnew customer entered, total customers are now: {}".format(customers))
            print("Total: {}\nWaiting: {}".format(customers,customers-1))
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
    mutex.acquire()
    customers -= 1
    print("\nCustomer{} exited barber room".format(working))
    print("Total/Waiting: {}".format(customers))
    mutex.release()

def customerEntry():
    for i in range(10):
        cutomerEntryThread = threading.Thread(target=customer_thread)        
        cutomerEntryThread.start()

EntryThread = threading.Thread(target=customerEntry)
EntryThread.start()
EntryThread.join()

barberWorkThread = threading.Thread(target=barber_thread)
barberWorkThread.start()

