import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import datetime
import sys

if len(sys.argv) < 2:
    mydate = datetime.datetime.now()
    date = mydate.strftime("%G_%B")
else:
    date = sys.argv[1]


def full_zh_gen(df_dict: dict, current=True) -> str:
    print(df_dict)
    love = df_dict['love']
    money = df_dict['money']
    hobby = df_dict['hobby']
    friends = df_dict['friends']
    health = df_dict['health']
    job = df_dict['job']
    df = pd.DataFrame({
        'group': ['A'],
        'Л': [int(love)],
        'Б': [int(money)],
        'Х': [int(hobby)],
        'Д': [int(friends)],
        'З': [int(health)],
        'Р': [int(job)]
    })

    # ------- PART 1: Create background

    # number of variable
    categories = list(df)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], color="grey", size=7)
    plt.ylim(0, 10)

    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

    # Ind1
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    print(date)
    print(angles)
    print(values)
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=date[5:])
    ax.fill(angles, values, 'b', alpha=0.1)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    name = date + '_polnaya_zh.png'
    fig.savefig(name)
    return name
