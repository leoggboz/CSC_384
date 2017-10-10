# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    "create a queue S for frontier, path Path storing the path"
    successors_stack = util.Stack()

    #the starting state
    current_state = problem.getStartState()
    next_frontier = problem.getSuccessors(current_state)
    if problem.isGoalState(current_state):
        return []
    elif next_frontier == []:
        print "no such solution"
        return []
    else:
        for i in next_frontier:
            successors_stack.push([[current_state], i])

    #from the first state we build up the frontier
    while not successors_stack.isEmpty():
        current_state = successors_stack.pop()
        #goal checking current_state is the goal state jump out of the loop
        if problem.isGoalState(current_state[-1][0]):
            break

        #path checking next_frontier
        next_frontier = problem.getSuccessors(current_state[-1][0])
        for i in next_frontier:
            path_flag = 0
            for j in current_state:
                if i[0] == j[0]:
                    path_flag = 1
            if path_flag == 0:
                successors_stack.push(current_state+[i])

    #compute the path
    path = []
    for i in current_state[1:]:
        path.append(i[1])
    return path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    successors_queue = util.Queue()
    current_state = problem.getStartState()
    #keep a visited nodes list
    visited_nodes = [current_state]

    if problem.isGoalState(current_state):
        return []
    else:
        successors_queue.push( ((current_state,"",0),) )

    # from the first state we build up the frontier
    while not successors_queue.isEmpty():
        current_state = successors_queue.pop()
        # goal checking current_state is the goal state jump out of the loop
        if problem.isGoalState(current_state[-1][0]):
            break

        # CYCLE checking next_frontier
        next_frontier = problem.getSuccessors(current_state[-1][0])
        for i in next_frontier:
            if i[0] not in visited_nodes:
                successors_queue.push(current_state + (i,))
                visited_nodes.append(i[0])
    # compute the path
    path = []
    for i in current_state[1:]:
        path.append(i[1])
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    def sumCost(state):
        sum = 0
        for i in state:
            sum += i[2]
        return sum

    def returnPath(current_state):
        path = []
        for i in current_state[1:]:
            path.append(i[1])
        return path

    #create a priority queue
    successors_p_queue = util.PriorityQueue()
    current_state = problem.getStartState()
    # keep a visited nodes list
    visited_nodes = [current_state]
    if problem.isGoalState(current_state):
        return []
    else:
        #successors_p_queue.push(tuple([[current_state,"",0]]),sumCost([[current_state,"",0]]))
        next_frontier = problem.getSuccessors(current_state)
        for i in next_frontier:
            successors_p_queue.push(([current_state, "", 0], i), sumCost( [[current_state, "", 0], i] ))
            if not problem.isGoalState(i[0]):
                visited_nodes.append(i[0])


    # from the first state we build up the frontier
    while not successors_p_queue.isEmpty():
        current_state = successors_p_queue.pop()
        # goal checking current_state is the goal state jump out of the loop
        if problem.isGoalState(current_state[-1][0]):
            break

        # CYCLE checking next_frontier
        next_frontier = problem.getSuccessors(current_state[-1][0])
        for i in next_frontier:
            path_flag = 0

            for j in visited_nodes:
                if i[0] == j:
                    path_flag = 1

            if path_flag == 0:
                successors_p_queue.push(tuple(current_state + tuple([i])), sumCost(tuple(current_state + tuple([i]))))
                if not problem.isGoalState(i[0]):
                    visited_nodes.append(i[0])

    return returnPath(current_state)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def sumCost(state):
        sum = 0
        for i in state:
            sum += i[2]
        sum += heuristic(state[-1][0], problem)
        return sum

    def returnPath(current_state):
        path = []
        for i in current_state[1:]:
            path.append(i[1])
        return path

    #create a priority queue
    successors_p_queue = util.PriorityQueue()
    current_state = problem.getStartState()
    # keep a visited nodes list
    visited_nodes = [current_state]
    if problem.isGoalState(current_state):
        return []
    else:
        successors_p_queue.push(tuple([[current_state, "", 0]]), 0)

    while not successors_p_queue.isEmpty():
        current_state = successors_p_queue.pop()
        # goal checking current_state is the goal state jump out of the loop
        if problem.isGoalState(current_state[-1][0]):
            break

        # CYCLE checking next_frontier
        next_frontier = problem.getSuccessors(current_state[-1][0])
        for i in next_frontier:
            if not i[0] in visited_nodes:
                successors_p_queue.push(tuple(current_state + tuple([i])), sumCost(tuple(current_state + tuple([i]))))
                if not problem.isGoalState(i[0]):
                    visited_nodes.append(i[0])

    return returnPath(current_state)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
