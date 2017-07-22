import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

def func(variable_vector):
    return [
        variable_vector[0]**2 + variable_vector[1]**2
        ]

class Search_set:
    __search_axis = []
    __search_start_point = ""
    
    def __init__(self,search_axis,search_start_point):
        self.__search_axis = search_axis
        self.__search_start_point = search_start_point
    
    def get_search_axis(self):
        return self.__search_axis
    
    def get_search_start_point(self):
        return self.__search_start_point
    

if __name__ == '__main__':
    
    initial_variable_vector = np.array([0.0,0.0])
    variable_vector = np.array([0.0,0.0])
    resource_vector = np.array([0.0])
    resource_constraint_vector = np.array([10000.0])
    feasible_variable_vector_list = []
    allowable_error = 0.1
    initial_flag = 0
    delta = 10
    
    search_sets = [Search_set(np.array([1.0,0]),np.array([0,0])), Search_set(np.array([0,1.0]),np.array([0,0]))]
        
    print "search boundary"
    
    while True:
        for search_set in search_sets:
            
            #set start point
            search_axis = search_set.get_search_axis()
            variable_vector = search_set.get_search_start_point()
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
                    if np.dot(previous_variable_vector,search_axis) < np.dot(variable_vector,search_axis):
                        new_vector = variable_vector + search_axis*(resource_constraint_vector[0] - resource_vector[0]) * np.linalg.norm(variable_vector - previous_variable_vector)/(resource_vector[0] - previous_resource_vector[0])
                    else:
                        new_vector = variable_vector - search_axis*(resource_constraint_vector[0] - resource_vector[0]) * np.linalg.norm(variable_vector - previous_variable_vector)/(resource_vector[0] - previous_resource_vector[0])
                    previous_variable_vector = variable_vector
                    previous_resource_vector = resource_vector
                    variable_vector = new_vector
                    resource_vector = func(variable_vector)
                    print "variable : " + str(variable_vector) + " , resource : " + str(resource_vector) 
    
                    if resource_vector[0] < resource_constraint_vector[0]:
                        feasible_variable_vector_list.append(variable_vector.tolist())
        
        points = np.array(feasible_variable_vector_list)
        hull = ConvexHull(points)
        vertices = hull.vertices
        search_sets = []
        
        print "search start point search axis"
        for i in range(1,len(vertices) - 1):
            endpoint_a = points[vertices[i]]
            endpoint_b = points[vertices[i + 1]]
            axis = endpoint_b - endpoint_a
            axis = axis / np.linalg.norm(axis)
            
            previous_variable_vector = endpoint_a
            previous_resource_vector =  func(previous_variable_vector)
    
    
            variable_vector = endpoint_a + axis*delta
            resource_vector = func(variable_vector)
            print "variable : " + str(variable_vector) + " , resource : " + str(resource_vector) 
            if resource_vector[0] < resource_constraint_vector[0]:
                feasible_variable_vector_list.append(variable_vector.tolist())
            while True:
                if np.linalg.norm(resource_vector[0] - previous_resource_vector[0]) < allowable_error:
                    break
                else:
                    if np.dot(previous_variable_vector,axis) < np.dot(variable_vector,axis):
                        new_vector = variable_vector - axis * np.linalg.norm(variable_vector - previous_variable_vector)/(resource_vector[0] - previous_resource_vector[0])
                    else:
                        new_vector = variable_vector + axis * np.linalg.norm(variable_vector - previous_variable_vector)/(resource_vector[0] - previous_resource_vector[0])
                    previous_variable_vector = variable_vector
                    previous_resource_vector = resource_vector
                    variable_vector = new_vector
                    resource_vector = func(variable_vector)
                    print "variable : " + str(variable_vector) + " , resource : " + str(resource_vector)
                    if resource_vector[0] < resource_constraint_vector[0]:
                        feasible_variable_vector_list.append(variable_vector.tolist())
            print axis
            normal_axis = np.array([axis[1],-axis[0]])
            print normal_axis

            normal_axis = normal_axis / np.linalg.norm(normal_axis)
            print normal_axis
            print variable_vector                       
            search_sets.append(Search_set(normal_axis,variable_vector))
               
        points = np.array(feasible_variable_vector_list)
        hull = ConvexHull(points)
        vertices = hull.vertices
                    
        plt.plot(points[:,0], points[:,1], 'o')
        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
        plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
        plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
        plt.show()
