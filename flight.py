import datetime
file = open('days you entered not the same with flight.txt', 'r')
lines = file.readlines()
heuristics = {}
# class will represent the graph which i will make from cites to connect them
class Graph:
    wate_in_dirction_flight = 0.0
    waiting = 0.0
    test = 0
    # use them for find number of flight for one trip
    temp = {}
    temp2 =[]
    # use them for find number of flight for multi trips
    stemp = {}
    stemp2 = {}
    # use this variable for another loop on file
    lines_len = 0
    # init like constructor
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed

    #create connection betwwen 2 cites with distance which equall in our case time
    def connect(self, A, B, time=1):
        self.graph_dict.setdefault(A, {})[B] = time


    # Get neighbor of city
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        #put keys and values withowt repeat in a list it's name nodes
        nodes = s1.union(s2)
        return list(nodes)


# class for city
class City:

    # it's like constructor and initialize function
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.g = 0  # time from city to other g
        self.h  = 0  # time from city to end heuristic g
        self.f = 0  # Total time f

    # operator overloading to compare nodes like (==)
    def __eq__(self, other):
        return self.name == other.name

    # operator overloading to sort nodes like (>)
    def __lt__(self, other):
        return self.f < other.f

    # for return node
    def __repr__(self):
        return ('({0},{1})'.format(self.position , self.f ))


# A* search
def travel(start, end, list):
    # days check by it if entered day valid or not and if not i'm chose on before and one after
    dayes = ['sat','sun','mon','tue','wed','thr','fri']
    graph = Graph()
    # files
    for line in lines:
        data = line.strip().split("|")
        # time of each trip
        deprture = datetime.datetime.strptime(data[2], "%H:%M")
        arrival = datetime.datetime.strptime(data[3], "%H:%M")
        newTime = arrival - deprture
        # direct flight
        if ((data[0] == start and data[1] == end)):
            heuristics[data[0]] = (newTime.seconds / 3600)
            heuristics[data[1]] = 0
        # not direct flight
        elif((data[0] == start or data[1] == start) and (data[0] != start and data[1] != end)):
            heuristics[data[0]] = (newTime.seconds / 3600 )*2
            heuristics[data[1]] = (newTime.seconds / 3600 )*2
        # target city should have heuristic = 0
        elif(data[0] == end or data[1] == end):
            heuristics[data[0]] = 0
            heuristics[data[1]] = 0
        else:
            heuristics[data[0]] = (newTime.seconds / 3600)
            heuristics[data[1]] = (newTime.seconds / 3600)
        graph.connect(data[0], data[1], (newTime.seconds / 3600))
    # _____________

    open = []
    closed = []
    start_node = City(start, None)
    goal_node = City(end, None)

    # append the start node to opn list
    open.append(start_node)

    # while loop even length of open list == 0
    while len(open) > 0:

        # we need the node which have lower cost so we sort open list to get it
        open.sort()

        # we save our lower cost node in current node and pop it from list
        current_node = open.pop(0)

        # append the current node to closed list
        closed.append(current_node)

        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ':> IN: ' + str(current_node.g) + ' H')
                # change current to hold another node
                current_node = current_node.parent
                Graph.lines_len = len(lines)
                while(Graph.lines_len > 0):
                    for line2 in lines:
                        Graph.lines_len = Graph.lines_len - 1
                        data2 = line2.strip().split("|")
                        Departuret = data2[2].split(":")
                        Arrivalt = data2[3].split(":")
                        dayesoftravel = data2[5]
                        dayesoftravellist = dayesoftravel.split(",")
                        a_set = set(list)
                        b_set = set(dayesoftravellist)
                        if(start_node.name == data2[0] and current_node.name == data2[1]):
                            if((a_set & b_set)):
                                warrival = datetime.datetime.strptime(data2[3], "%H:%M")
                                print("Use Flight: " + data2[4] + " From: " + data2[0] +
                                      " To: " + data2[1]
                                      + ". Departure Time Is: " + data2[2] + " And Arrival Time Is: " + data2[3])
                                Graph.test = Graph.test + 1
                                #________________________________________________
                                x = float(float(Arrivalt[0])+float(Arrivalt[1])/100)
                                Graph.stemp.update({data2[4]:x})
                                #__________________________________________________

                            else:
                                list.insert(len(list), dayes[(dayes.index((list[len(list) - 1]))) + 1])
                                list.insert(0, dayes[(dayes.index((list[0]))) - 1])

                        if (current_node.name == data2[0] and goal_node.name == data2[1]):
                            if((a_set & b_set)):
                                if(start_node.name == data2[0] and Graph.test == 0):
                                    print("Use Flight: " + data2[4] + " From: " + data2[0] +
                                          " To: " + data2[1]
                                          + ". Departure Time Is: " + data2[2] + " And Arrival Time Is: " + data2[3])

                                    Graph.waiting = 0.0
                                    #__________________________________________________________
                                    ft = datetime.datetime.strptime(data2[3], "%H:%M")
                                    st = datetime.datetime.strptime(data2[2], "%H:%M")
                                    nt = ft - st
                                    nt = nt.seconds/3600
                                    Graph.temp.update({data2[4]:nt})
                                    Graph.temp2.append(nt)
                                    Graph.temp2.sort()
                                    #____________________________________________________________

                                if (start_node.name == data2[0]):
                                    arrival_in_dirction_flight = datetime.datetime.strptime(data2[3], "%H:%M")
                                    departure_in_dirction_flight = datetime.datetime.strptime(data2[2], "%H:%M")
                                    Graph.wate_in_dirction_flight = arrival_in_dirction_flight - departure_in_dirction_flight
                                    Graph.wate_in_dirction_flight = (Graph.wate_in_dirction_flight.seconds / 3600)
                                    #print(Graph.wate_in_dirction_flight)

                                elif(start_node.name != data2[0]):
                                    print("Use Flight: " + data2[4] + " From: " + data2[0] +
                                          " To: " + data2[1]
                                          + ". Departure Time Is: " + data2[2] + " And Arrival Time Is: " + data2[3])

                                    #____________________________________________________________
                                    y = float(float(Departuret[0])+float(Departuret[1])/100)
                                    Graph.stemp2.update({data2[4]:y})
                                    #_____________________________________________________________
                                    wdeprture = datetime.datetime.strptime(data2[2], "%H:%M")
                                    Graph.waiting = warrival -wdeprture
                                    Graph.waiting = (Graph.waiting.seconds/3600)
                                if((Graph.waiting+current_node.g) > Graph.wate_in_dirction_flight and Graph.wate_in_dirction_flight != 0 and start_node.name == data2[0]):
                                    print("Use Flight: " + data2[4] + " From: " + data2[0] +
                                          " To: " + data2[1]
                                          + ". Departure Time Is: " + data2[2] + " And Arrival Time Is: " + data2[3])

                                    Graph.waiting = 0.0
                                    # __________________________________________________________
                                    ft = datetime.datetime.strptime(data2[3], "%H:%M")
                                    st = datetime.datetime.strptime(data2[2], "%H:%M")
                                    nt = ft - st
                                    nt = nt.seconds / 3600
                                    Graph.temp.update({data2[4]: nt})
                                    Graph.temp2.append(nt)
                                    Graph.temp2.sort()
                                    # ____________________________________________________________

                            else:
                                list.insert(len(list), dayes[(dayes.index((list[len(list) - 1]))) + 1])
                                list.insert(0, dayes[(dayes.index((list[0]))) - 1])
                                if(Graph.lines_len == 0 and (a_set&b_set)):
                                    Graph.lines_len = Graph.lines_len + 1

            path.append(start_node.name + ':> IN: ' + str(current_node.g) + ' H')
            # print and return our path
            # bring every thing from start to end as list
            return path[::-1]

        # bring nodes which is neighbors to current nod
        neighbors = graph.get(current_node.name)

        # Loop on key and value
        for key, value in neighbors.items():
            # Create a neighbor node
            neighbor = City(key, current_node)
            if (neighbor in closed):
                continue
            # full path time
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # add neighbor to open list if have lower value
            if (add_to_open(open, neighbor) == True):
                open.append(neighbor)


    # if there isn't any path founded
    print("there is no flights from this source to this destination")
    return None


def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True

#to get value
def get_key1(val):
    for key, value in Graph.temp.items():
        if val == value:
            return key

    return "key doesn't exist"

# The main entry point for this module
def runmethod():
    templist = [1000]
    flightn1 = ' '
    flightn2 = ' '

    # input data here ____________________________________________________
    print(" You Have This Flights According To The Days You Entered :> ")
    print_soulution = travel('Alexandria', 'Aswan', ['sun','mon','tue','wed'])
    # _____________________________________________________________________


    if(len(Graph.temp2) > 0 and Graph.waiting == 0):
        list = [0]
        value = [Graph.temp2[i] for i in list]
        print(" Use Flights It's Numbers Is  : >> {}".format(get_key1(value[0])))
    if (len(Graph.stemp2) > 0 and Graph.waiting > 0):
        for i in Graph.stemp:
            for j in Graph.stemp2:
                for x in range (len(templist)):
                    templist.append(Graph.stemp[i]-Graph.stemp2[j])
                    templist.sort()
                    if(Graph.stemp[i]-Graph.stemp2[j] == templist[0]):
                        flightn1 = i
                        flightn2 = j
        print(" Use Flights It's Numbers Is : >> {} {} ".format(flightn1 , flightn2))
    print("  Were This Is Optimal Path According To Time Of Flights Not Consider Waite Time : >> {}".format(print_soulution))

    print()
    if(templist[0] == 1000):
        print("Waiting Time = {} Hour(s)".format(0))
    else:
        print("Waiting Time = {} Hour(s)".format(Graph.waiting))

if __name__ == "__main__": runmethod()