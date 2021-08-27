import copy
import time


class Puzzle:
    def __init__(self, puzzle: list):
        self.dimension = len(puzzle)

        cells = []
        not_assigned = []
        assigned = []
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] == '-':
                    temp = Cell([i, j])
                    not_assigned.append(temp)
                else:
                    temp = Cell([i, j], [int(puzzle[i][j])], int(puzzle[i][j]))
                    assigned.append(temp)
                cells.append(temp)

        for cell in range(len(cells)):
            if (cell + 1) % self.dimension:
                cells[cell].right = cells[cell+1]
            if cell % self.dimension:
                cells[cell].left = cells[cell-1]
            if int(cell/self.dimension):
                cells[cell].up = cells[cell-self.dimension]
            if int(cell/self.dimension) < self.dimension - 1:
                cells[cell].down = cells[cell+self.dimension]
        self.cells = cells
        self.assigned = assigned
        self.not_assigned = not_assigned
        forward_checking(self)


class Cell:
    def __init__(self, index: list, domain: list = None, value: int = -1):
        if domain:
            self.domain = domain
        else:
            self.domain = [0, 1]
        self.index = index
        self.value = value
        self.left = None
        self.right = None
        self.up = None
        self.down = None


def forward_checking(puzzle: Puzzle):
    for cell in puzzle.not_assigned:
        for value in cell.domain:
            # more than 2 0s or 1s adjacency check
            if cell.left and cell.left.left and cell.left.left.value == cell.left.value == value:
                cell.domain.remove(value)
                continue
            if cell.up and cell.up.up and cell.up.up.value == cell.up.value == value:
                cell.domain.remove(value)
                continue
            if cell.down and cell.down.down and cell.down.down.value == cell.down.value == value:
                cell.domain.remove(value)
                continue
            if cell.right and cell.right.right and cell.right.right.value == cell.right.value == value:
                cell.domain.remove(value)
                continue
            if cell.left and cell.right and cell.left.value == value == cell.right.value:
                cell.domain.remove(value)
                continue
            if cell.down and cell.up and cell.down.value == value == cell.up.value:
                cell.domain.remove(value)
                continue

            # equal number of 0s and 1s check
            zero_number = 0
            one_number = 0
            if value == 0:
                zero_number += 1
            elif value == 1:
                one_number += 1
            for i in range(puzzle.dimension * cell.index[0], puzzle.dimension * (cell.index[0] + 1)):
                if puzzle.cells[i].value == 0:
                    zero_number += 1
                elif puzzle.cells[i].value == 1:
                    one_number += 1
            if zero_number > puzzle.dimension / 2 or one_number > puzzle.dimension / 2:
                cell.domain.remove(value)
                continue
            zero_number = 0
            one_number = 0
            if value == 0:
                zero_number += 1
            elif value == 1:
                one_number += 1
            for j in range(cell.index[1], puzzle.dimension*puzzle.dimension, puzzle.dimension):
                if puzzle.cells[j].value == 0:
                    zero_number += 1
                elif puzzle.cells[j].value == 1:
                    one_number += 1
            if zero_number > puzzle.dimension / 2 or one_number > puzzle.dimension / 2:
                cell.domain.remove(value)
                continue

            # every row and column uniqueness check
            cell.value = value
            row_complete = []
            for i in range(puzzle.dimension):
                row_complete.append(True)
                for j in range(puzzle.dimension * i, puzzle.dimension * (i + 1)):
                    if puzzle.cells[j].value == -1:
                        row_complete[i] = False
                        break
            if row_complete[cell.index[0]]:
                for i in range(len(row_complete)):
                    if i != cell.index[0] and row_complete[i] and cell.domain.count(value):
                        for j in range(len(row_complete)):
                            if puzzle.cells[puzzle.dimension * cell.index[0]+j].value != \
                                    puzzle.cells[puzzle.dimension * i+j].value:
                                break
                            if j == len(row_complete) - 1:
                                cell.domain.remove(value)
            if cell.domain.count(value) == 0:
                cell.value = -1
                continue

            column_complete = []
            for i in range(puzzle.dimension):
                column_complete.append(True)
                for j in range(i, puzzle.dimension * puzzle.dimension, puzzle.dimension):
                    if puzzle.cells[j].value == -1:
                        column_complete[i] = False
                        break
            if column_complete[cell.index[1]]:
                for i in range(len(column_complete)):
                    if i != cell.index[1] and column_complete[i] and cell.domain.count(value):
                        for j in range(i, puzzle.dimension * puzzle.dimension, puzzle.dimension):
                            if puzzle.cells[j].value != \
                                    puzzle.cells[cell.index[1] + int(j/puzzle.dimension)*puzzle.dimension].value:
                                break
                            if j == puzzle.dimension*(puzzle.dimension-1) + i:
                                cell.domain.remove(value)
            cell.value = -1


def mrv(puzzle: Puzzle):
    selected = min(puzzle.not_assigned, key=lambda x: len(x.domain))
    return selected


def print_puzzle(puzzle: Puzzle, x: Cell):
    index = [x.index[0] + 1, x.index[1] + 1]
    if x.value == -1:
        print(index, "= -")
    else:
        print(index, "=", x.value)
    for i in range(puzzle.dimension):
        for j in range(puzzle.dimension):
            if puzzle.cells[i * puzzle.dimension + j].value == -1:
                print("-", end=" ")
            else:
                print(puzzle.cells[i * puzzle.dimension + j].value, end=" ")
        print("")
    print("." * (puzzle.dimension * 3))


def backtracking(puzzle: Puzzle):
    if len(puzzle.assigned) == len(puzzle.cells):
        return puzzle
    x = mrv(puzzle)
    for v in x.domain:
        prev_puzzle = copy.deepcopy(puzzle)
        x = mrv(puzzle)
        puzzle.not_assigned.remove(x)
        puzzle.assigned.append(x)
        x.value = v
        print_puzzle(puzzle, x)
        forward_checking(puzzle)
        flag = False
        for cell in puzzle.not_assigned:
            if len(cell.domain) == 0:
                flag = True
                break
        if flag:
            puzzle = prev_puzzle
            continue
        result = backtracking(puzzle)
        if result:
            return result
        puzzle = prev_puzzle
    x.value = -1
    print_puzzle(puzzle, x)
    return False


if __name__ == '__main__':
    start = time.time()
    for problem in range(7, 8):
        test_read = open("puzzles/puzzle{}.txt".format(problem), "r")
        test_write = open("output/FC/output{}_fc.txt".format(problem), "w")
        puzzle_dimension = int(list(test_read.readline().split())[0])
        puzzle_list = []
        for row in range(puzzle_dimension):
            puzzle_list.append(list(test_read.readline().split()))
        test_read.close()

        puzzle1 = Puzzle(puzzle_list)
        puzzle1_solution = backtracking(puzzle1)
        if puzzle1_solution:
            for i1 in range(puzzle1_solution.dimension):
                for j1 in range(puzzle1_solution.dimension):
                    test_write.write(str(puzzle1_solution.cells[i1*puzzle1_solution.dimension + j1].value) + " ")
                test_write.write("\n")
        else:
            test_write.write("There is not any solution")
        test_write.close()
    end = time.time()
    print("\nForward Checking => exec time:", int((end - start) / 60),
          "minutes and", "{:.2f}".format((end - start) % 60), "seconds")
