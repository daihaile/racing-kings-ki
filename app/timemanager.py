import threading, time, datetime

# Get the current unix time epoch in milliseconds
def time_ms():
	return int(time.time() * 1000)

# Set a function to be executed after a certain time
def setTimeout(ms, function,args):
	t = threading.Timer(ms / 1000, function ,args)
	t.start()
	return t


def havetime(timeout,timeBudget, time_hint):
    return True

def timeHandle(move):
    start_time = datetime.datetime.now()
    current_time = start_time
    print(start_time)
    while True:
        if (datetime.datetime.now() - current_time).seconds == 1:
            current_time = datetime.datetime.now()
            print(current_time)
            if(current_time - start_time).seconds == 5:
                print("5 seconds past")
                return "new move here" + move



def startTimer(duration):
    move = "random"
    timer = setTimeout(duration,timeHandle,["move"])

if __name__ == "__main__":
    print("starting timer")
    t = startTimer(1000)
    print(t.name)