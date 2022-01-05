# search.py
# Christopher Stasiowski, CMPSC 165A

import numpy
import time
import random

def NextMove(grid, step):

  MoveCode = 4
  bestScore = 0
  
  for i in range(4):
    score = calculateScore(grid, i)
    if score > bestScore:
      bestScore = score
      MoveCode = i
  
  if MoveCode == 4 and emptyTiles(grid) > 0:
    return random.randint(0,3)
  return MoveCode

# directional functions used to simulate possible moves given a grid
def moveLeft(grid):
  newGrid = compress(grid)
  newGrid = merge(newGrid)
  newGrid = compress(newGrid)
  return newGrid

def moveRight(grid):
  newGrid = reverse(grid)
  newGrid = moveLeft(newGrid)
  newGrid = reverse(newGrid)
  return newGrid

def moveUp(grid):
  newGrid = transpose(grid)
  newGrid = moveLeft(newGrid)
  newGrid = transpose(newGrid)
  return newGrid

def moveDown(grid):
  newGrid = transpose(grid)
  newGrid = moveRight(newGrid)
  newGrid = transpose(newGrid)
  return newGrid

# helper function: transposes a given grid
def transpose(grid):
  transGrid = []
  for i in range(4):
    transGrid.append([])
    for j in range(4):
      transGrid[i].append(grid[j][i])
  return transGrid

# helper function: reverses a given grid
def reverse(grid):
  reversedGrid = []
  for i in range(4):
    reversedGrid.append([])
    for j in range(4):
      reversedGrid[i].append(grid[i][3-j])
  return reversedGrid

# simulates a directional move for a given grid
def simulateMove(grid, dir):
  if dir == 0:
    return moveUp(grid)
  elif dir == 1:
    return moveDown(grid)
  elif dir == 2:
    return moveLeft(grid)
  elif dir == 3:
    return moveRight(grid)
  return grid

# helper compress/merge functions used in directional moves
def compress(grid):
  changed = False

  compressedGrid = []

  for i in range(4):
    compressedGrid.append([0]*4)
  
  for i in range(4):
    pos = 0
    for j in range(4):
      if grid[i][j] != 0:
        compressedGrid[i][pos] = grid[i][j]
        if j != pos:
          changed = True
        pos += 1
  
  return compressedGrid

def merge(grid):
  changed = False

  for i in range(4):
    for j in range(3):
      if (grid[i][j] == grid[i][j+1] and grid[i][j] != 0):
        grid[i][j] = grid[i][j]*2
        grid[i][j+1] = 0
        changed = True
  
  return grid

def calculateScore(grid, i):
  newGrid = simulateMove(grid, i)
  zeros = 0
  if newGrid == grid:
    return 0
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if grid[i][j] == 0:
        zeros += 1
  if zeros < 3:
    return generateScore(newGrid, 0, 3)
  return generateScore(newGrid, 0, 2)

def generateScore(grid, currentDepth, depthLimit):
  if currentDepth >= depthLimit:
    return calculateFinalScore(grid)
  totalScore = 0
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if grid[i][j] == 0:
        newGrid2 = grid
        newGrid2[i][j] = 2
        moveScore2 = calculateMoveScore(newGrid2, currentDepth, depthLimit)
        totalScore += (0.9*moveScore2)

        newGrid4 = grid
        newGrid4[i][j] = 4
        moveScore4 = calculateMoveScore(newGrid4, currentDepth, depthLimit)
        totalScore += (0.1*moveScore4)

  return totalScore

def calculateMoveScore(grid, currentDepth, depthLimit):
  bestScore = 0
  for i in range(4):
    newGrid = simulateMove(grid, i)
    if newGrid != grid:
      score = generateScore(newGrid, currentDepth+1, depthLimit)
      bestScore = max(score, bestScore)
  
  return bestScore

def emptyTiles(grid):
  zeros = 0
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if grid[i][j] == 0:
        zeros += 1
  return zeros

def smoothness(grid):
  smooth = 0
  row, col = len(grid), len(grid[0]) if len(grid) > 0 else 0
  for r in grid:
    for i in range(col-1):
      smooth += abs(r[i] - r[i+1])
      pass
  for j in range(row):
    for k in range(col-1):
      smooth += abs(grid[k][j] - grid[k+1][j])

  return smooth

def monotonicity(grid):
  mono= 0
  row, col = len(grid), len(grid[0]) if len(grid) > 0 else 0
  for r in grid:
    diff = r[0]-r[1]
    for i in range(col-1):
      if (r[i] - r[i+1]) * diff <= 0:
        mono += 1
      diff = r[i] - r[i+1]

  for j in range(row):
    diff = grid[0][j] - grid[1][j]
    for k in range(col - 1):
      if (grid[k][j] - grid[k+1][j]) * diff <= 0:
        mono += 1
      diff = grid[k][j] - grid[k+1][j]
  
  return mono

WEIGHT_MATRIX = [[2048, 1024, 64, 32],[512, 128, 16, 2],[256, 8, 2, 1],[4, 2, 1, 1]]

def weightedGrid(grid):
  result = 0
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      result += grid[i][j] * WEIGHT_MATRIX[i][j]
  return result

def calculateFinalScore(grid):
  score = []
  score.append(emptyTiles(grid))
  score.append(weightedGrid(grid))
  score.append(smoothness(grid))
  score.append(monotonicity(grid))
  return sum(score)

# TESTING FUNCTIONS

def generateRandom():
  grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
  values = [0,2,4,8,16,32,64,128,256]
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      num = random.randint(0,8)
      grid[i][j] = values[num]
  
  return grid

def timeTest():
  start = time.time()
  for i in range(10):
    grid = generateRandom()
    printGrid(grid)
    print(NextMove(grid, random.randint(0,20)))
  print("RUNTIME: ", time.time()-start)

def playGame():
  grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
  spawn = [2,2,2,2,2,2,2,2,2,4]
  grid[random.randint(0,3)][random.randint(0,3)] = spawn[random.randint(0,9)]
  while True:
    grid2x = random.randint(0,3)
    grid2y = random.randint(0,3)
    if grid[grid2x][grid2y] == 0:
      grid[grid2x][grid2y] = spawn[random.randint(0,9)]
      break
  
  while True:
    direction = NextMove(grid, 0)
    if direction == 4:
      print("GAME OVER")
      print(grid)
    grid = simulateMove(grid, direction)
    zeros = []
    for i in range(len(grid)):
      for j in range(len(grid[i])):
        if grid[i][j] == 0:
          zeros.append([i,j])
    
    insertAt = zeros[random.randint(0,len(zeros)-1)]
    insert = spawn[random.randint(0,9)]
    grid[insertAt[0]][insertAt[1]] = insert
    print(grid)

playGame()