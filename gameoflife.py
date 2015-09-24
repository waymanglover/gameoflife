import random
import argparse


class Cell:

    def __init__(self, x, y, alive=-1):
        if alive == -1:
            self.alive = random.choice([True, False])
        else:
            self.alive = alive
        self.x = x
        self.y = y

    def __str__(self):
        if self.alive:
            return '*'
        else:
            return ' '

    def position(self):
        return (self.x, self.y)

    def kill(self):
        self.alive = False

    def birth(self):
        self.alive = True


class World:

    def __init__(self, size, *seeds):
        if seeds:
            # Seed the world with predefined spots
            self.world = [[Cell(x, y, False) for y in range(size)] for x in range(size)]
            for seed in seeds:
                self.world[seed[1]][seed[0]].alive = True
        else:
            # Generate a random world
            self.world = [[Cell(x, y) for y in range(size)] for x in range(size)]
        self.generation = 1

    def __str__(self):
        # Used when printing the world state
        output = 'Generation ' + str(self.generation)
        for x in range(len(self.world)):
            output += '\n'
            for y in range(len(self.world)):
                output += str(self.world[x][y])
        output += '\n'
        return output

    def getCell(self, x, y):
        # This is where we do the wrap-around magic
        if x < 0 or x >= len(self.world):
            return Cell(x, y, False)
        elif y < 0 or y >= len(self.world):
            return Cell(x, y, False)
        else:
            return self.world[x][y]

    def countAliveNeighbors(self, cell):
        count = 0
        # Python ranges are exclusive, have to add one to the second parameter
        # for the range to be inclusive.
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                if xOffset != 0 or yOffset != 0:
                    # Only looking at cells that are not the current cell
                    x = cell.x + xOffset
                    y = cell.y + yOffset
                    if self.getCell(x, y).alive:
                        count += 1
        return count

    def simulateGeneration(self):
        killList = []
        birthList = []
        for row in self.world:
            for cell in row:
                cellLives = False
                neighbors = self.countAliveNeighbors(cell)  # number of neighbors
                if cell.alive:
                    # If cell is alive and neighbors < 2 -> cell dies
                    # If cell is alive and neighbors == 2 or 3 -> cell lives
                    # If cell is alive and neighbors > 3 -> cell dies
                    if neighbors < 2:
                        killList.append(cell)
                    elif neighbors > 3:
                        killList.append(cell)
                else:
                    # If cell is dead and neighbors == 3 -> cell lives
                    if neighbors == 3:
                        birthList.append(cell)
        for cell in killList:
            cell.kill()
        for cell in birthList:
            cell.birth()
        self.generation += 1


def main():
    generations = 3
    world = World(3, (0, 1), (1, 1), (0, 2), (1, 2))
    for x in range(generations):
        print(world)
        world.simulateGeneration()

    world = World(3, (0, 1), (1, 1), (2, 1))
    for x in range(generations):
        print(world)
        world.simulateGeneration()


if __name__ == "__main__":
    # Execute only if run as a script
    main()
