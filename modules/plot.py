import matplotlib.pyplot as plt

'Plotar um gráfico em 2D'
def plot2D(point_cloud):
    ax1 = list()
    ax2 = list()
    for point in point_cloud:
        ax1.append(point['x'])
        ax2.append(point['z'])
    plt.plot(ax1, ax2, 'o')
    plt.show()


'Plotar um gráfico em 3D'
def plot3D(point_cloud):
    axis_x = list()
    axis_y = list()
    axis_z = list()
    axis_c = list()
    for point in point_cloud:    
        axis_x[-1].append(point['x'])
        axis_y[-1].append(point['y'])
        axis_z[-1].append(point['z'])
        axis_c[-1].append(point['value'])
    
    'Plotar em 3D'
    fig = plb.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(
        np.array(axis_x),
        np.array(axis_y),
        np.array(axis_z),
        c=np.array(axis_c),
        s=20,
        linewidths=0
    )
    #ax.set_xlim3d(-60, 60)
    #ax.set_ylim3d(-60, 60)
    #ax.set_zlim3d(-96, -50)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_zlabel("Eixo Z")
    plb.show()
