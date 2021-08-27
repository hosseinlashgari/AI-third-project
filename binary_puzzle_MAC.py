import copy
import itertools
import time


class Puzzle:
    def __init__(self, puzzle: list):
        self.dimension = len(puzzle)

        variables = []
        not_assigned = []
        assigned = []
        for row in range(self.dimension):
            temp = Variable(puzzle[row], "row", row)
            variables.append(temp)
            not_assigned.append(temp)
        for column in range(self.dimension):
            temp_list = []
            for row in range(self.dimension):
                temp_list.append(puzzle[row][column])
            temp = Variable(temp_list, "column", column)
            variables.append(temp)
            not_assigned.append(temp)
        self.variables = variables
        self.assigned = assigned
        self.not_assigned = not_assigned
        queue = []
        for v1 in variables:
            for v2 in variables:
                if v1 != v2:
                    queue.append([v1, v2])
        ac3(self, queue)


class Variable:
    def __init__(self, cells_list: list, direction: str, index: int):
        self.dimension = len(cells_list)
        self.direction = direction
        self.index = index

        cells = []
        if direction == "row":
            for j in range(self.dimension):
                if cells_list[j] == '-':
                    temp = Cell([index, j])
                else:
                    temp = Cell([index, j], [int(cells_list[j])])
                cells.append(temp)
        elif direction == "column":
            for i in range(self.dimension):
                if cells_list[i] == '-':
                    temp = Cell([i, index])
                else:
                    temp = Cell([i, index], [int(cells_list[i])])
                cells.append(temp)

        domain = []
        domains_list = []
        for cell in cells:
            domains_list.append(cell.domain)
        temp_domain = list(itertools.product(*domains_list))
        for d in temp_domain:
            flag = True
            for cell in range(len(d) - 2):
                if d[cell] == d[cell + 1] == d[cell + 2]:
                    flag = False
                    break
            if flag and d.count(0) == d.count(1):
                domain.append(d)
        self.value = None
        self.cells = cells
        self.domain = domain


class Cell:
    def __init__(self, index: list, domain: list = None):
        if domain:
            self.domain = domain
        else:
            self.domain = [0, 1]
        self.index = index


def ac3(puzzle: Puzzle, queue: list):
    while len(queue):
        arc = queue.pop(0)
        if revise(arc):
            if len(arc[0].domain) == 0:
                return False
            for v in puzzle.not_assigned:
                if v != arc[0] and v != arc[1]:
                    queue.append([v, arc[0]])
    return True


def revise(arc: list):
    revised = False
    new_domain = []
    if arc[0].direction == arc[1].direction:
        for d in arc[0].domain:
            if len(arc[1].domain) == 1 and arc[1].domain[0] == d:
                revised = True
            else:
                new_domain.append(d)
    else:
        for d in arc[0].domain:
            flag = True
            for d2 in arc[1].domain:
                if d2[arc[0].index] == d[arc[1].index]:
                    new_domain.append(d)
                    flag = False
                    break
            if flag:
                revised = True
    arc[0].domain = new_domain
    return revised


def mrv(puzzle: Puzzle):
    selected = min(puzzle.not_assigned, key=lambda x: len(x.domain))
    return selected


def print_puzzle(puzzle: Puzzle, x: Variable):
    index = x.index + 1
    if x.value:
        print(x.direction, index, "=", x.value)
    else:
        print(x.direction, index, "=", "- " * puzzle.dimension)
    for i in range(puzzle.dimension):
        if puzzle.variables[i].value:
            for j in range(puzzle.dimension):
                print(puzzle.variables[i].value[j], end=" ")
        else:
            for j in range(puzzle.dimension, 2 * puzzle.dimension):
                if puzzle.variables[j].value:
                    print(puzzle.variables[j].value[i], end=" ")
                else:
                    print("-", end=" ")
        print("")
    print("." * (puzzle.dimension * 4))


def backtracking(puzzle: Puzzle):
    if len(puzzle.assigned) == len(puzzle.variables):
        return puzzle
    x = mrv(puzzle)
    for v in x.domain:
        prev_puzzle = copy.deepcopy(puzzle)
        x = mrv(puzzle)
        puzzle.not_assigned.remove(x)
        puzzle.assigned.append(x)
        x.value = v
        x.domain = [v]
        print_puzzle(puzzle, x)
        queue = []
        for v2 in puzzle.not_assigned:
            queue.append([v2, x])
        ac3(puzzle, queue)
        flag = False
        for variable in puzzle.variables:
            if len(variable.domain) == 0:
                flag = True
                break
        if flag:
            puzzle = prev_puzzle
            continue
        result = backtracking(puzzle)
        if result:
            return result
        puzzle = prev_puzzle
    x.value = None
    print_puzzle(puzzle, x)
    return False


if __name__ == '__main__':
    start = time.time()
    for problem in range(7, 8):
        test_read = open("puzzles/puzzle{}.txt".format(problem), "r")
        test_write = open("output/MAC/output{}_mac.txt".format(problem), "w")
        puzzle_dimension = int(list(test_read.readline().split())[0])
        puzzle_list = []
        for r in range(puzzle_dimension):
            puzzle_list.append(list(test_read.readline().split()))
        test_read.close()

        puzzle1 = Puzzle(puzzle_list)
        puzzle1_solution = backtracking(puzzle1)
        if puzzle1_solution:
            for i1 in range(puzzle1_solution.dimension):
                for j1 in range(puzzle1_solution.dimension):
                    test_write.write(str(puzzle1_solution.variables[i1].value[j1]) + " ")
                test_write.write("\n")
        else:
            test_write.write("There is not any solution")
        test_write.close()
    end = time.time()
    print("\nMAC => exec time:", int((end - start) / 60), "minutes and", "{:.2f}".format((end - start) % 60), "seconds")
