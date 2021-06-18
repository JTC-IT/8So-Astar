from copy import deepcopy
import time

# Các phép biến đổi trạng thái
Operator = {"UP": [-1, 0], "DOWN": [1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}

# Read file
file = open('input.txt', 'r')
data = file.read().strip()

Ar = []
for i in data:
    if i.isnumeric():
        Ar.append(int(i))

START = [Ar[0:3], Ar[3:6], Ar[6:9]]
END = [Ar[9:12], Ar[12:15], Ar[15:18]]


class State:
    def __init__(self, matrix = [], parent_State = None, g = 0, h = 0, op = ''):
        self.matrix = matrix
        self.parent_State = parent_State
        self.g = g
        self.h = h
        self.op = op

    def f(self):
        return self.g + self.h   #f = gx + hx

    def print_matrix(self):
        if self.op != '':
            print('->'+self.op+':')
            print()
        for ar in self.matrix:
            for i in ar:
                print(i, end = ' ')
            print()


def get_pos(matrix, element): #lấy vị trí của element trong matrix
    for row in range(0,3):
        for col in range(0,3):
            if element == matrix[row][col]:
                return [row, col]


def cal_cost(matrix): #Tính toán chi phí của 1 trạng thái
    cost = 0 
    for row in range(0,3):
        for col in range(0,3):
            pos = get_pos(END, matrix[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost


def getState_Next(state): #Trả về danh sách các trạng thái tiếp theo
    listState = []
    emptyPos = get_pos(state.matrix, 0) #vi tri nut 0

    for op in Operator.keys():
        newPos = (emptyPos[0] + Operator[op][0], emptyPos[1] + Operator[op][1])

        if 0 <= newPos[0] < 3 and 0 <= newPos[1] < 3:
            matrix = deepcopy(state.matrix)
            matrix[emptyPos[0]][emptyPos[1]] = state.matrix[newPos[0]][newPos[1]]
            matrix[newPos[0]][newPos[1]] = 0
            listState.append(State(matrix, state, state.g + 1, cal_cost(matrix), op))

    return listState


def getBestState(Open):
    firstIter = True
    for state in Open.values():
        if firstIter or state.f() < bestF:
            firstIter = False
            bestState = state
            bestF = state.f()
    return bestState


def buildPath(Close): #trả về danh sách lưu cách di chuyển và trạng thái lúc đó
    state = Close[str(END)]
    branch = []

    while state.op != '':
        branch.append(state)
        state = Close[str(state.parent_State.matrix)]
    branch.append(state)
    branch.reverse()
    return branch

def outPut(branch):
    print('--------------------------------')
    print('Bước di chuyển: ', len(branch) - 1)
    print()
    for state in branch:
        state.print_matrix()
        print()
    print('--------------------------------')
    print('->END.')

def main():
    Open = {str(START): State(START, None, 0, cal_cost(START), '')}
    Close = {}
    start_time = time.time()
    while len(Open) > 0:
        cur_State = getBestState(Open)
        Close[str(cur_State.matrix)] = cur_State

        if cur_State.matrix == END:
            outPut(buildPath(Close))
            return

        list_State_next = getState_Next(cur_State)
        for state in list_State_next:
            if str(state.matrix) not in Close.keys() and str(state.matrix) not in Open.keys():
                Open[str(state.matrix)] = state
            elif str(state.matrix) in Open.keys():
                if state.f() < Open[str(state.matrix)].f():
                    Open[str(state.matrix)] = state
        del Open[str(cur_State.matrix)]
        if time.time() - start_time > 2:
                print("Ko tim ra ket qua!")
                return

if __name__ == '__main__':
    main()