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
        return successorGameState.getScore()

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
        self.pacmanIndex=0
        self.ghostIndex=1
        self.numGhosts = 0

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
        currentDepth = 0
        self.numGhosts = gameState.getNumAgents()-1
        return self.maxvalue(gameState, currentDepth)
    
    def maxvalue(self, gameState, currentDepth):
        #methods isWin() and isLose() from the class GameState in file pacman.py
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()
        pacmanActions = gameState.getLegalActions(self.pacmanIndex)
        maxUtilityvalue = currentScore = float("-inf")
        currentScore = maxUtilityvalue
        bestAction = pacmanActions[0] #instanciate the bestAction
        for action in pacmanActions:
            currentScore = self.minvalue(gameState.generateSuccessor(self.pacmanIndex, action), currentDepth, self.ghostIndex)
            if currentScore > maxUtilityvalue:
                maxUtilityvalue = currentScore
                bestAction = action
        #print "currentDepth : ", currentDepth
        if currentDepth == 0: #the root node the best action is returned to the method getAction
            return bestAction
        return maxUtilityvalue #otherwise we return the max utility value when it's the pacman turn to play

    def minvalue(self, gameState, currentDepth, ghost):
        #methods isWin() and isLose() from the class GameState in file pacman.py
        if gameState.isLose() or gameState.isWin():
            return gameState.getScore()
        nextAgent = ghost + 1
        if ghost == self.numGhosts : nextAgent = self.pacmanIndex
        ghostActions = gameState.getLegalActions(ghost)
        minUtilityvalue = float("inf")
        for action in ghostActions:
            if nextAgent > self.pacmanIndex:
                minUtilityvalue = min(minUtilityvalue, self.minvalue(gameState.generateSuccessor(ghost, action), currentDepth, nextAgent))
            else:
                if currentDepth == self.depth - 1:
                    minUtilityvalue = min(minUtilityvalue,self.evaluationFunction(gameState.generateSuccessor(ghost, action)))
                else:
                    minUtilityvalue = min(minUtilityvalue, self.maxvalue(gameState.generateSuccessor(ghost, action), currentDepth + 1))
        return minUtilityvalue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        currentDepth = 0
        self.numGhosts = gameState.getNumAgents()-1
        return self.maxvalue(gameState, currentDepth, float("-inf"), float("inf"))
    
    def maxvalue(self, gameState, currentDepth, alpha, beta):
        #methods isWin() and isLose() from the class GameState in file pacman.py
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()
        pacmanActions = gameState.getLegalActions(self.pacmanIndex)
        maxUtilityvalue = currentScore = float("-inf")
        #currentScore = maxUtilityvalue
        bestAction = pacmanActions[0] #instanciate the bestAction
        for action in pacmanActions:
            currentScore = self.minvalue(gameState.generateSuccessor(self.pacmanIndex, action), currentDepth, self.ghostIndex, alpha, beta)
            if currentScore > maxUtilityvalue:
                maxUtilityvalue = currentScore
                bestAction = action
            if maxUtilityvalue > beta:
                return maxUtilityvalue
            alpha = max(alpha, maxUtilityvalue)
        #print "currentDepth : ", currentDepth
        if currentDepth == 0: #the root node the best action is returned to the method getAction
            return bestAction
        return maxUtilityvalue #otherwise we return the max utility value when it's the pacman turn to play

    def minvalue(self, gameState, currentDepth, ghost, alpha, beta):
        #methods isWin() and isLose() from the class GameState in file pacman.py
        if gameState.isLose() or gameState.isWin():
            return gameState.getScore()
        nextAgent = ghost + 1
        if ghost == self.numGhosts : nextAgent = self.pacmanIndex
        ghostActions = gameState.getLegalActions(ghost)
        minUtilityvalue = float("inf")
        for action in ghostActions:
            if nextAgent > self.pacmanIndex:
                minUtilityvalue = min(minUtilityvalue, self.minvalue(gameState.generateSuccessor(ghost, action), currentDepth, nextAgent, alpha, beta))
            else:
                if currentDepth == self.depth - 1:
                    minUtilityvalue = min(minUtilityvalue,self.evaluationFunction(gameState.generateSuccessor(ghost, action)))
                else:
                    minUtilityvalue = min(minUtilityvalue, self.maxvalue(gameState.generateSuccessor(ghost, action), currentDepth + 1, alpha, beta))
            if minUtilityvalue < alpha:
               return minUtilityvalue
            beta = min(beta, minUtilityvalue)
        return minUtilityvalue

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

