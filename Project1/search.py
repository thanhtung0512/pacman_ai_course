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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    explored = []
    path = []
    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return path
    # Add node, path
    frontier.push((initial_state, path))

    while not frontier.isEmpty():
        curr_node, path = frontier.pop()
        if curr_node not in explored:
            explored.append(curr_node)

            if problem.isGoalState(curr_node):
                return path
            
            for next_state, action, cost in problem.getSuccessors(curr_node):
                frontier.push((next_state, path + [action]))

    return None

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    explored = []
    path = []
    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return path
    # Add node, path
    frontier.push((initial_state, path))

    while not frontier.isEmpty():
        curr_node, path = frontier.pop()
        if curr_node not in explored:
            explored.append(curr_node)

            if problem.isGoalState(curr_node):
                return path
            for next_state, action, cost in problem.getSuccessors(curr_node):
                frontier.push((next_state, path + [action]))

    return None

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    start_node = problem.getStartState()
    frontier = util.PriorityQueue()
    explored = {}  
    path = []
    init_cost = 0
    frontier.push((init_cost, start_node, path), init_cost)

    while not frontier.isEmpty():
        curr_cost, curr_node, path = frontier.pop()

        if problem.isGoalState(curr_node):
            return path

        if curr_node in explored and curr_cost > explored[curr_node]:
            continue 

        explored[curr_node] = curr_cost

        for successor, action, cost in problem.getSuccessors(curr_node):
            new_cost = curr_cost + cost

            if successor not in explored or new_cost < explored[successor]:
                frontier.push((new_cost, successor, path + [action]), new_cost)

    return None

        


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueueWithFunction

    start_node = problem.getStartState()
    path = {start_node: (None, None, 0, 1)}  # (parent, action, cost, collected)
    frontier = PriorityQueueWithFunction(lambda x: path[x][2] + heuristic(x, problem))
    actions = []
    

    while not problem.isGoalState(start_node):
        for successor in problem.getSuccessors(start_node):
            next_node = successor[0]
            action = successor[1]
            cost = successor[2]

            if next_node not in path:
                path[next_node] = (start_node, action, path[start_node][2] + cost, 0)
                frontier.push(next_node)
            elif not path[next_node][3] and path[start_node][2] + cost < path[next_node][2]:
                path[next_node] = (start_node, action, path[start_node][2] + cost, 0)
                frontier.update(next_node, path[next_node][2] + heuristic(next_node, problem))

        start_node = frontier.pop()
        path[start_node] = (path[start_node][0], path[start_node][1], path[start_node][2], 1)

    while start_node != problem.getStartState():
        actions.insert(0, path[start_node][1])
        start_node = path[start_node][0]

    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
