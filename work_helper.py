import time
from os import listdir, getcwd

# replace commas with this string so it doesn't affect split(",")
CODE = "!@#$%^&*()(*&^%$#@!"

def print_line():
    print("----------------------------------------------------------------")

def time_converter(t):
    '''
    Takes in time t in seconds, and returns a nicely formatted string.

    >>> time_converter(5)
    5 s
    >>> time_converter(65)
    1 m 5 s
    >>> time_converter(3665)
    1 h 1 m 5 s
    '''
    if t < 60:
        return str(int(t)) + " s"
    elif t < 3600:
        mins = t//60
        return str(int(mins)) + " m " + time_converter(t%60)
    else:
        hrs = t//3600
        return str(int(hrs)) + " h " + time_converter(t%3600)

def print_if_non_zero(text, n, to_time_convert=False):
    '''
    Prints text followed by n if n is non-zero. Converts n to a nice time string if to_time_convert

    >>>print_if_non_zero("Qns Completed:", 5)
    Qns Completed: 5
    >>>print_if_non_zero("Total Time:", 0)

    >>>print_if_non_zero("Ave Time:", 65)
    Ave Time: 1 m 5 s
    '''
    if n:
        if to_time_convert:
            n = time_converter(n)
        print(text, n)

def print_stats(completed, ave, totalTime=0, qnsLeft=0, timeLeft=0):
    print_if_non_zero("Qns Completed:", completed)
    print_if_non_zero("Qns Left:", qnsLeft)
    print_if_non_zero("Total Time:", totalTime, True)
    print_if_non_zero("Ave Time:", ave, True)
    print_if_non_zero("Time Left:", timeLeft, True)

def productivity_manager(qns, completed=0, totalTime=0):
    '''
    Tracks a user's time taken per question and churns out stats regarding their work.
    '''
    startTime = time.time()
    prevTime = 0
    if totalTime != 0:
        ave = totalTime/completed
    else:
        ave = 0
    
    for i in range(qns - completed, 0, -1):
        print_line()
        print_stats(completed, ave, qnsLeft=i, timeLeft=i*ave)

        if prevTime != 0: print("Prev Qn:", time_converter(prevTime))

        text = input("> ")
        if text == "done":
        	# saves current data in a txt file

            filename = input("File name: ") + ".txt"
            remarks = input("Remarks: ")
            global CODE
            remarks = remarks.replace(",", CODE)
            data = open(filename , 'w')
            data.write(str(qns) + "," + str(completed) + "," + str(totalTime) +"," + remarks)
            data.close()
            print_line()
            print("Data successfully saved in", filename)
            print_line()
            print_stats(completed, ave, totalTime=totalTime, qnsLeft=i)
            print_line()
            return
        elif text=="p" or text=="pause":
            pauseTime = time.time()
            print("Timer paused. Hit enter to resume.")
            input("> ")
            startTime = time.time() - pauseTime + startTime
            print("Break was", time_converter(time.time()-pauseTime), "long")
            print("Resumed")
            print_line()
        else:
            endTime = time.time()
            prevTime, startTime = endTime - startTime, endTime
            completed += 1
            totalTime += prevTime
            ave = totalTime / completed

    print_line()
    print("CONGRATS YOU ARE DONE!!!")
    print_stats(completed, ave, totalTime=totalTime)

def data_from_name(data_name=None):
    '''
    Loads data from a txt file with name data_name
    '''
    file_name_list = []
    for i in listdir(getcwd()):
    	if ".txt" in i:
    		file_name_list += [i]
    if data_name == None:
    	print_line()
    	print("All saved data:")
    	for i in file_name_list:
    		print(i)
    	print_line()
    	data_name = input("Data name: ")

    if not ".txt" in data_name:
    	data_name += ".txt"

    if data_name in file_name_list:
    	file = open(data_name, 'r')
    	data = file.read().split(',')
    	print("Remarks:")
    	global CODE
    	print(data[3].replace(CODE, ","))
    	print("Press Enter to begin")
    	input("> ")
    	productivity_manager(int(data[0]), int(data[1]), float(data[2]))
    else:
    	print_line()
    	print("That file name does not exist.")
    	data_from_name()

def start():
    '''
    Creates a command-line like interface for starting a new work or continuing an old one. Loops indefinitely until q is called.
    '''
    print_line()
    print("n - new work")
    print("c - continue from saved data (eg 'c test')")
    print("m - manually enter data from previous session")
    print("q - quit")
    print_line()

    command = input("Command me: ")

    if command[0] == "n" and len(command) == 1:
        productivity_manager(int(input("Total questions: ")))
    elif command[0] == "m" and len(command) == 1:
    	productivity_manager(int(input("Total questions: ")), int(input("Completed questions: ")), int(input("Time taken in sec: ")))
    elif command[0] == 'c':
    	if len(command) > 2:
    		data_from_name(command[2:])
    	else:
    		data_from_name()
    elif command[0] == 'q' and len(command) == 1:
    	print("Have a nice day!")
    	return
    else:
    	print("I'm sorry I don't quite understand.")

    # loops indefinitely
    start()

start()
