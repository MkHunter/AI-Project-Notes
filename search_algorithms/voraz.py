import numpy as np
import queue
import matplotlib.pyplot as plt

def getNAttacks(state):
    attacks = 0
    n = len(state)
    for i in range(0,n):
        X = state[i]
        for j in range(i+1,n):
            Y = state[j]
            if(X-Y == 0):
                attacks+=2
            if(abs(i-j) == abs(X-Y)):
                attacks+=2
    return attacks

#Receives a list that represents the state: [n1,n2,...] where n1 != n2!= ...
def goaltest(state,goal):
    attacks = getNAttacks(state)
    
    print("You got "+str(attacks)+" out of "+str(goal)+".\nYou "+("didn't ","")[attacks==goal]+"satisfy the goal.")
    return attacks == goal

def sortOffspring(offspring):
    state_attacks = [[x,getNAttacks(offspring[x])] for x in range(0,len(offspring))]
    sorted_by_attacks = sorted(state_attacks, key = lambda x: x[1])
    sorted_states = [offspring[sorted_by_attacks[x][0]] for x in range(0,len(sorted_by_attacks))]
    return sorted_states

#Expands the actual node, returns a list of states
def expand(state):
    expanded = []
    n = len(state)
    for i in range(0,n):
        temporal = [0]*n
        temporal[i] = 1
        expanded_value = list(np.add(temporal,state))
        #Validate that it can't overextend the range
        #And that it has unique values
        #if any(k > n for k in expanded_value) and not (len(set(expanded_value)) == n):
        #    continue
        expanded.append(expanded_value)
    return expanded

def addtoQueue(queue_,list_of_lists):
    for l in list_of_lists:
        queue_.put(l)

def printQueue(queue_,elem_limit):
    queue_= list(queue_.queue)
    if len(queue_)<elem_limit:
        print("frontier = "+str(queue_))

def printBoard(arr_solution):
    if arr_solution != []:
        size = len(arr_solution)

        chessboard = np.zeros((size,size))
        chessboard[1::2,0::2] = 1
        chessboard[0::2,1::2] = 1

        plt.imshow(chessboard, cmap='binary')
        #print(arr_solution)
        for i in range(0,len(arr_solution)):
            j = arr_solution[i]-1
            plt.text(j, i, '♕', fontsize=20, ha='center', va='center', color='black' if (i - j) % 2 == 0 else 'white')
        plt.show()

# MAIN ALGORITHM
cost=1
arr_solution = []

def VS(frontier,goal):
    global cost, arr_solution
    act_element = frontier.get()
    print("\n"+str(cost)+". ======== "+str(act_element)+" ========")
    if goaltest(act_element,goal):
        print("The BFS is "+str(act_element))
        arr_solution = act_element
        return
    
    offspring = expand(act_element)
    offspring = sortOffspring(offspring)
    
    addtoQueue(frontier,offspring)

    cost+=1
    VS(frontier,goal)

# The program itself
front = queue.Queue()
board = [1]*4
print(board)
front.put(board)
VS(front,0)
print(str(cost)+" iterations were done.")
cost = 0
front.queue.clear()