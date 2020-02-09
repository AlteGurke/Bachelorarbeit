import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import ntpath

def get_Color(value):
    switcher = {
        "l": "red",
        "u": "green"
    }
    return switcher.get(value, "")

def add_To_Dictionary(lineValues, action, dict):
    values = lineValues[1][2:-1].split(',')
    key = values[0]
    dict.setdefault(key, []).append([ action, lineValues[0], values[1] ])

def read_Trace_File(traceFilename):
    file = open(traceFilename, 'r') 
    lines = file.readlines() 

    dict = {}
    for line in lines: 
        lineValues = line.strip().split(':')
        if lineValues[1][0] == "l":
            add_To_Dictionary(lineValues, "l", dict)
        elif lineValues[1][0] == "u":
            add_To_Dictionary(lineValues, "u", dict)
    return dict
    #print(dict)

def create_Graph(dict, title):
    threads  = set([])
    times = set([])
    x = []
    y = []
    c = []
    texts = []

    for key, value in dict.items():
        threads.add(key)
        for v in value:
            times.add(v[1])

    threads  = sorted(list(threads))
    times  = sorted(list(times))

    for key, value in dict.items():
        for v in value:
            xValue = int(v[1]) - int(times[0])
            offset = 0
            if xValue in x:
                offset = 0.1 * x.count(xValue)
            x.append(xValue)
            y.append(threads.index(key) + offset)
            c.append(get_Color(v[0]))
            texts.append(v[2])

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
dict = read_Trace_File(traceFilename)
plt = create_Graph(dict, "Trace for " + ntpath.basename(traceFilename))
plt.show()