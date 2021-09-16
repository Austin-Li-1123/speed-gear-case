import matplotlib.pyplot as plt
import math
from matplotlib.patches import Patch
import job_definition

colors = ["blue", "red", "orange", "olive", "green", "gray", "pink", "purple"]



def creat_vis(endpoint_times, makespan):
    x_range = makespan * 1.3

    machine_count = len(endpoint_times)
    yi = [(math.floor(i*(100/machine_count)+5), 9) for i in range(machine_count)]

    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    
    # Setting Y-axis limits
    gnt.set_ylim(0, 110)
    
    # Setting X-axis limits
    gnt.set_xlim(0, x_range)
    
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('hours since start')
    gnt.set_ylabel('Processor')
    
    # Setting ticks on y-axis
    gnt.set_yticks([y[0]+5 for y in yi])
    # Labelling tickes of y-axis
    gnt.set_yticklabels([str(i) for i in range(machine_count)])
    
    # Setting graph attribute
    gnt.grid(True)
    
    # Declaring a bar in schedule
    # gnt.broken_barh([(40, 50)], (30, 9), facecolors =('tab:'+colors[0]))
    
    # # Declaring multiple bars in at same level and same width
    # gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
    #                         facecolors ='tab:'+colors[1])
    
    # gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
    #                                 facecolors =('tab:'+colors[2]))
    
    c_dict = {}

    for i in range(machine_count):
        for task in endpoint_times[i]:
            gnt.broken_barh([task[1:]], yi[i],
                                    facecolors =(colors[task[0]]))
            c_dict[job_definition.all_jobs[task[0]]] = colors[task[0]]

    # c_dict = {'MKT':'blue', 'FIN':'red', 'ENG':'orange',
    #         'PROD':'#34D0C3', 'IT':'#3475D0'}
    legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
    plt.legend(handles=legend_elements)



    plt.savefig("gantt1.png")
    plt.show()
