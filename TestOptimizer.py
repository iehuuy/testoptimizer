import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

def func(variable_vector):
    return [
        2*variable_vector[0]**2 + variable_vector[1]**2 + 3*variable_vector[0] + 2*variable_vector[1]
        ]


if __name__ == '__main__':
    points = np.random.rand(30, 2)
    print points
    
    initial_variable_vector = np.array([0.0,0.0])
    variable_vector = np.array([0.0,0.0])
    resource_vector = np.array([0.0])
    resource_constraint_vector = np.array([500.0])
    feasible_variable_vector_list = []
    allowable_error = 0.1
    initial_flag = 0
    delta = 1
        
    search_axes = [np.array([1.0,0]),np.array([0,1.0])]

     #serach
    for search_axis in search_axes:
        
        #set start point
        variable_vector = initial_variable_vector
        resource_vector = func(variable_vector)
        if func(variable_vector)[0] < resource_constraint_vector[0]:
            feasible_variable_vector_list.append(variable_vector.tolist())
        print "variable : " + str(variable_vector) + " , resource : " + str(resource_vector)
        
        #set 2nd point
        previous_variable_vector = variable_vector
        previous_resource_vector = resource_vector      
        variable_vector = variable_vector + search_axis*delta
        resource_vector = func(variable_vector)
        if func(variable_vector)[0] < resource_constraint_vector[0]:
            feasible_variable_vector_list.append(variable_vector.tolist())
        print "variable : " + str(variable_vector) + " , resource : " + str(resource_vector)
                    
        while True:
            if abs(resource_vector[0] - resource_constraint_vector[0]) < allowable_error:
                break
            else:
                variable_vector = variable_vector + search_axis*(resource_constraint_vector[0] - func(variable_vector)[0]) * np.linalg.norm(variable_vector - previous_variable_vector)/(func(variable_vector)[0] - func(previous_variable_vector)[0])
                resource_vector = func(variable_vector)
            if func(variable_vector)[0] < resource_constraint_vector[0]:
                feasible_variable_vector_list.append(variable_vector.tolist())
                print "variable : " + str(variable_vector) + " , resource : " + str(resource_vector)              
    
    print feasible_variable_vector_list

    points = np.array(feasible_variable_vector_list)
    print points  
    hull = ConvexHull(points)
    plt.plot(points[:,0], points[:,1], 'o')
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
    plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
    plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
    plt.show()