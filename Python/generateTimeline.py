import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import ntpath

import traceFileReader

def get_Color(value):
    switcher = {
        traceFileReader.LockActionType.LOCK: "red",
        traceFileReader.LockActionType.UNLOCK: "green"
    }
    return switcher.get(value, "")

def create_Graph(lockActions, title):
    threads  = set([])
    times = set([])
    x = []
    y = []
    c = []
    texts = []

    for lockAction in lockActions:
        threads.add(lockAction.threadName)
        times.add(lockAction.timeStamp)

    threads  = sorted(list(threads))
    times  = sorted(list(times))

    for lockAction in lockActions:
        xValue = int(lockAction.timeStamp) - int(times[0])
        offset = 0
        if xValue in x:
            offset = 0.1 * x.count(xValue)
        x.append(xValue)
        y.append(threads.index(lockAction.threadName) + offset)
        c.append(get_Color(lockAction.actionType))
        texts.append(lockAction.lockObjectName)

    plt.figure(figsize=(20, len(threads) + 2))
    plt.title(title)
    plt.scatter(x, y, c=c, alpha=0.85, s=100)
    plt.xlabel("Time in µs")

    red_patch = mpatches.Patch(color='red', label='Lock event')
    green_patch = mpatches.Patch(color='green', label='Unlock event')
    plt.legend(handles=[red_patch, green_patch], loc="upper left")

    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)

    # Ensure that the axis ticks only show up on the bottom and left of the plot. 
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.   
    ax.get_xaxis().tick_bottom()   
    ax.get_yaxis().tick_left()

    # Limit the range of the plot to only where the data is.    
    # Avoid unnecessary whitespace.    
    plt.ylim((-1,len(threads)))
    plt.xlim((-1, int(times[len(times) - 1]) - int(times[0]) + 1))

    # Make sure your axis ticks are large enough to be easily read.
    # You don't want your viewers squinting to read your plot.
    plt.yticks(range(len(threads)), threads, fontsize=14)
    plt.xticks(fontsize=14)

    for i, txt in enumerate(texts):
        plt.annotate(txt, (x[i], y[i] + 0.1))

    return plt

traceFilename = sys.argv[1]
lockActions = traceFileReader.read_Trace_File_Lines(traceFilename)
plt = create_Graph(lockActions, "Trace for " + ntpath.basename(traceFilename))
plt.show()