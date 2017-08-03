import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

def func(search_vector):
    return [
        search_vector[0]**2 + search_vector[1]**2
        ]
    '''
def func(search_vector):
    return [
    search_vector[0]*search_vector[1]
        ]
    '''
'''
def cal_feasible_area(feasible_search_vector_list):

    representative_feasible_serch_vector_list = [[0,0]]

    for feasible_search_vector in feasible_search_vector_list:

        print "feasible_search_vector : " + str(feasible_search_vector)
        print ""
        print "before representative_feasible_serch_vector_list : " + str(representative_feasible_serch_vector_list)
        print ""
        insert_flag = 0

        for representative_feasible_serch_vector in representative_feasible_serch_vector_list:
            print "representative_feasible_serch_vector: " + str(representative_feasible_serch_vector)
            print ""
            
            if feasible_search_vector[0] == representative_feasible_serch_vector[0] and feasible_search_vector[1] == representative_feasible_serch_vector[1]:
                print "1"
            elif feasible_search_vector[0] < representative_feasible_serch_vector[0] and feasible_search_vector[1] > representative_feasible_serch_vector[1]:
                if insert_flag == 0:
                    representative_feasible_serch_vector_list.append(feasible_search_vector)
                    insert_flag = 1
                print "2"

            elif feasible_search_vector[0] > representative_feasible_serch_vector[0] and feasible_search_vector[1] < representative_feasible_serch_vector[1]:
                if insert_flag == 0:
                    representative_feasible_serch_vector_list.append(feasible_search_vector)
                    insert_flag = 1
                
            elif feasible_search_vector[0] >= representative_feasible_serch_vector[0] and feasible_search_vector[1] >= representative_feasible_serch_vector[1] :
                if insert_flag == 0:
                    representative_feasible_serch_vector_list.append(feasible_search_vector)
                    insert_flag = 1
                representative_feasible_serch_vector_list.remove(representative_feasible_serch_vector)
                print "4"
                
        print "middle representative_feasible_serch_vector : " + str(representative_feasible_serch_vector_list)
        print ""

        for representative_feasible_serch_vector in representative_feasible_serch_vector_list:
            for representative_feasible_serch_vector2 in representative_feasible_serch_vector_list:
                print representative_feasible_serch_vector2
                if representative_feasible_serch_vector[0] == representative_feasible_serch_vector2[0] and representative_feasible_serch_vector[1] == representative_feasible_serch_vector2[1]:
                    continue
                if representative_feasible_serch_vector[0] <= representative_feasible_serch_vector2[0] and representative_feasible_serch_vector[1] <= representative_feasible_serch_vector2[1]:
                    representative_feasible_serch_vector_list.remove(representative_feasible_serch_vector)
                elif representative_feasible_serch_vector[0] >= representative_feasible_serch_vector2[0] and representative_feasible_serch_vector[1] >= representative_feasible_serch_vector2[1]:
                    representative_feasible_serch_vector_list.remove(representative_feasible_serch_vector2)

            print "after representative_feasible_serch_vector : " + str(representative_feasible_serch_vector_list)

            print ""
            print ""
            
            sorted_representative_feasible_serch_vector_list = sorted(representative_feasible_serch_vector_list,key=lambda x:x[1],reverse=False)
            print sorted_representative_feasible_serch_vector_list
'''
def cal_feasible_area(initial_search_vector,feasible_search_vector_list):

    representative_feasible_serch_vector_list = []
    
    for candidate_representatative_feasible_serch_vector in feasible_search_vector_list:
        cnt = 0
        for feasible_search_vector in feasible_search_vector_list:
            if candidate_representatative_feasible_serch_vector[0] <= feasible_search_vector[0] and candidate_representatative_feasible_serch_vector[1] <= feasible_search_vector[1]:
                cnt = cnt + 1
        if cnt == 1:
            representative_feasible_serch_vector_list.append(candidate_representatative_feasible_serch_vector)
    
    sorted_representative_feasible_serch_vector_list = sorted(representative_feasible_serch_vector_list,key=lambda x:x[1],reverse=False)
    
    area_sum = 0  
    for i in range(0,len(sorted_representative_feasible_serch_vector_list) - 1):
        x = sorted_representative_feasible_serch_vector_list[i + 1][0] - initial_search_vector[0]
        y = sorted_representative_feasible_serch_vector_list[i + 1][1] - sorted_representative_feasible_serch_vector_list[i][1]
        area_sum = area_sum + x * y
            
    print area_sum
        
    
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
    initial_search_vector = np.array([0.0,0.0])
    search_vector = np.array([0.0,0.0])
    resource_vector = np.array([0.0])
    resource_constraint_vector = np.array([10000.0])
    searched_search_vector_list = []
    feasible_search_vector_list = []
    representative_search_vector_list = []
    allowable_error = 0.00001
    delta_init = 10
    delta_amp_rate = 2

    search_sets = [Search_set(np.array([1.0,0]),initial_search_vector), Search_set(np.array([0,1.0]),initial_search_vector)]
    representative_search_vector_list.append(initial_search_vector.tolist())

    print "------------------search boundary------------"

    while True:
        insert_point = 2

        for search_set in search_sets:
            delta = delta_init

            #set start point
            print "------------------set search start point and search axis------------------"
            search_axis = search_set.get_search_axis()
            search_vector = search_set.get_search_start_point()

            resource_vector = func(search_vector)
            searched_search_vector_list.append(search_vector.tolist())
            if resource_vector[0] <= resource_constraint_vector[0]:
                feasible_search_vector_list.append(search_vector.tolist())

            if resource_vector[0] > resource_constraint_vector[0]:
                search_axis = - search_axis

            print "search start point : " + str(search_vector) + "," + "search axis : " + str(search_axis)

            while True:
                previous_search_vector = search_vector
                previous_resource_vector = resource_vector
                search_vector = search_vector + search_axis*delta
                resource_vector = func(search_vector)
                searched_search_vector_list.append(search_vector.tolist())
                print "variable : " + str(search_vector) + " , resource : " + str(resource_vector)

                if resource_vector[0] <= resource_constraint_vector[0]:
                    feasible_search_vector_list.append(search_vector.tolist())
                if (resource_vector[0] - resource_constraint_vector[0]) * (previous_resource_vector[0]  - resource_constraint_vector[0]) < 0 :
                    break

                delta = delta * delta_amp_rate

            if resource_vector[0] - resource_constraint_vector[0] < 0:
                upper_search_vector = previous_search_vector
                lower_search_vector = search_vector
            else:
                upper_search_vector = search_vector
                lower_search_vector = previous_search_vector

            while True:
                if abs(resource_vector[0] - resource_constraint_vector[0]) < allowable_error:
                    if len(representative_search_vector_list) < 2:
                        representative_search_vector_list.append(search_vector.tolist())
                    else:
                        representative_search_vector_list.insert(insert_point,search_vector.tolist())
                        insert_point = insert_point + 2
                    break

                else:
                    search_vector = (upper_search_vector + lower_search_vector)/2
                    resource_vector = func(search_vector)
                    searched_search_vector_list.append(search_vector.tolist())
                    print "variable : " + str(search_vector) + " , resource : " + str(resource_vector) 

                    if resource_vector[0] <= resource_constraint_vector[0]:
                        feasible_search_vector_list.append(search_vector.tolist())
                        lower_search_vector = search_vector
                    else:
                        upper_search_vector = search_vector

        print "search start point search axis"
        search_sets = []
        representative_points = np.array(representative_search_vector_list)

        for i in range(1,len(representative_points) - 1):
            endpoint_a = representative_points[i]
            endpoint_b = representative_points[i + 1]
            axis = endpoint_b - endpoint_a
            axis = axis / np.linalg.norm(axis) 
            normal_axis = np.array([axis[1],-axis[0]])
            normal_axis = normal_axis / np.linalg.norm(normal_axis)
            search_sets.append(Search_set(normal_axis,(endpoint_a + endpoint_b) / 2))

            print "cal_feasible_area"
            cal_feasible_area(initial_search_vector,feasible_search_vector_list)
        representative_points = np.array(representative_search_vector_list)
        searched_search_vector_points = np.array(searched_search_vector_list)
        feasible_search_vector_points = np.array(feasible_search_vector_list)
        plt.plot(feasible_search_vector_points [:,0], feasible_search_vector_points [:,1], 'v')
        plt.show()
'''
        plt.plot(representative_points[:,0], representative_points[:,1], 'o')
        plt.show()
        plt.plot(searched_search_vector_points[:,0], searched_search_vector_points[:,1], '^')
        plt.show()
'''