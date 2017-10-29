# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if successorGameState.isLose():
            return -999999
        score = successorGameState.getScore()
        ghost_list = [ghostState.getPosition() for ghostState in newGhostStates]
        ghost_distance = []
        for i in ghost_list:
            ghost_distance.append(manhattanDistance(newPos,i))
            if manhattanDistance(newPos, i) == 0:
                return -99999

        food_list = newFood.asList()
        food_distance = []
        for i in food_list:
            food_distance.append(manhattanDistance(newPos,i))

        #go to the nearest food
        if ghost_distance and min(ghost_distance) > 0:
            score -= 10.0/min(ghost_distance)
        if food_distance and min(food_distance) > 0:
            score += 10.0/min(food_distance)
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState,depth,agent_ind):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)

            #ghost turn
            if agent_ind < gameState.getNumAgents():
                ghost_mvoe = gameState.getLegalActions(agent_ind)
                min_value = []
                for move in ghost_mvoe:
                    min_value.append(minimax(gameState.generateSuccessor(agent_ind, move),depth , agent_ind+1))
                return min(min_value)

            #pacman turn
            if agent_ind == gameState.getNumAgents():
                if depth+1 == self.depth or gameState.isLose() or gameState.isWin():
                    return self.evaluationFunction(gameState)
                pacman_move = gameState.getLegalActions(0)
                max_value = []
                for move in pacman_move:
                    max_value.append(minimax(gameState.generateSuccessor(0,move ),depth + 1,1))
                return max(max_value)

        max_move = ["",-999999]
        for i in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(0,i)
            temp_max = minimax(next_state,0,1)
            if max_move[1] < temp_max:
                max_move = i,temp_max
        return max_move[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -999999
        beta = 999999
        def minimax(gameState,depth,agent_ind, alpha, beta):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                value = self.evaluationFunction(gameState)
                return [value,alpha,beta]

            #ghost turn
            if agent_ind < gameState.getNumAgents():
                ghost_mvoe = gameState.getLegalActions(agent_ind)
                min_value = []
                for move in ghost_mvoe:
                    temp_value = minimax(gameState.generateSuccessor(agent_ind,move),depth,agent_ind+1,alpha,beta)
                    if beta > temp_value[0]:
                        beta = temp_value[0]
                    if beta <= alpha:
                        return [beta,alpha,beta]
                    min_value.append(temp_value)
                return  [beta,alpha,beta]

            #pacman turn
            if agent_ind == gameState.getNumAgents():
                if depth+1 == self.depth or gameState.isLose() or gameState.isWin():
                    value = self.evaluationFunction(gameState)
                    return [value,alpha,beta]

                pacman_move = gameState.getLegalActions(0)
                max_value = []
                for move in pacman_move:
                    temp_value = minimax(gameState.generateSuccessor(0,move),depth + 1,1,alpha,beta)
                    if alpha < temp_value[0]:
                        alpha = temp_value[0]
                    if beta <= alpha:
                        return [beta,alpha,beta]
                    max_value.append(temp_value)
                return  [alpha,alpha,beta]

        max_move = ["",-999999]
        for i in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(0,i)
            temp_max = minimax(next_state,0,1,alpha,beta)
            if alpha < temp_max[0]:
                alpha = temp_max[0]
            if beta <= alpha:
                break
            if max_move[1] < temp_max[0]:
                max_move = [i,temp_max[0]]
        return max_move[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState,depth,agent_ind):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)

            #ghost turn
            if agent_ind < gameState.getNumAgents():
                ghost_mvoe = gameState.getLegalActions(agent_ind)
                min_value = []
                for move in ghost_mvoe:
                    min_value.append(minimax(gameState.generateSuccessor(agent_ind, move),depth , agent_ind+1))
                return sum(min_value)/len(min_value)

            #pacman turn
            if agent_ind == gameState.getNumAgents():
                if depth+1 == self.depth or gameState.isLose() or gameState.isWin():
                    return self.evaluationFunction(gameState)
                pacman_move = gameState.getLegalActions(0)
                max_value = []
                for move in pacman_move:
                    max_value.append(minimax(gameState.generateSuccessor(0,move ),depth + 1,1))
                return max(max_value)

        max_move = ["",-999999]
        for i in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(0,i)
            temp_max = minimax(next_state,0,1)
            if max_move[1] < temp_max:
                max_move = i,temp_max
        return max_move[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacman_pos = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    ghost_state = currentGameState.getGhostStates()
    scared_time = [ghostState.scaredTimer for ghostState in ghost_state]
    ghost_pos = [ghostState.getPosition() for ghostState in ghost_state]

    value = currentGameState.getScore()

    pac_ghost_distance = [manhattanDistance(pacman_pos,i) for i in ghost_pos]
    pac_food_distance = [manhattanDistance(pacman_pos,i) for i in food_list]

    pac_food_distance.sort()
    pac_ghost_distance.sort()

    if min(pac_ghost_distance) <= 1:
        return -99

    for i in range(len(food_list)):
        value += (10.0/manhattanDistance(food_list[i],pacman_pos))*((len(food_list)-i)/len(food_list))

    for i in range(len(scared_time)):
        if scared_time[i] > 0:
            if len(pac_food_distance) != 0:
                value += 10/min(pac_food_distance)
        else:
            value -= 4/manhattanDistance(ghost_pos[i],pacman_pos)

    return value

# Abbreviation
better = betterEvaluationFunction
