N, M, K = list(map(int, input().split())) # N: 미로 크기, M: 사람 수, K: 라운드 수

VACANT = 0
_maze = []
_maze_for_runner = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(N) :
    _maze.append(list(map(int, input().split())))

R_IDX = 0
C_IDX = 1
_runner_list = []
for _ in range(M) :
    runner = list(map(int, input().split()))
    runner[R_IDX] -= 1
    runner[C_IDX] -= 1

    _runner_list.append(runner) # r,c

_exit = list(map(int, input().split()))
_exit[R_IDX] -= 1
_exit[C_IDX] -= 1


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

_d_r = [-1, 1, 0, 0] # 상 하
_d_c = [0, 0, -1, 1] #      좌 우
_move_score = 0
def distance(r,c) :
    return abs(_exit[R_IDX]-r) + abs(_exit[C_IDX]-c)

def move_runners() :
    global _runner_list, _move_score

    departure_list = []
    for idx, runner in enumerate(_runner_list) :
        r = runner[R_IDX]
        c = runner[C_IDX]
        for direction in range(4) :
            r_ = r + _d_r[direction]
            c_ = c + _d_c[direction]

            try :
                ## 1) 탈출할 수 있다면?
                if [r_, c_] == _exit :
                    departure_list.append(idx)
                    break

                ## 2) 벽이라면?
                if _maze[r_][c_] != VACANT :
                    continue

                ## 3) 최단거리가 줄어든다면?
                if distance(r_,c_) >= distance(r,c) :
                    continue

                _runner_list[idx][R_IDX] = r_
                _runner_list[idx][C_IDX] = c_
                _move_score += 1
                # print("move_score:", _move_score)
                # print("r_, c_:", r_, c_)

                break

            except IndexError :
                pass

    ## 탈출한 사람 제외
    if departure_list :
        departure_list.sort(reverse=True)

        for idx in departure_list :
            _runner_list.pop(idx)
            _move_score += 1

    return

def find_smallest_square() :
    shortest_length = N*N
    smallest_square_list = []
    for idx, runner in enumerate(_runner_list) :
        length = max(abs(runner[R_IDX] - _exit[R_IDX]), abs(runner[C_IDX] - _exit[C_IDX]))

        if shortest_length > length :
            shortest_length = length
            smallest_square_list = [[runner[R_IDX], runner[C_IDX]]]
        elif shortest_length == length :
            smallest_square_list.append([runner[R_IDX], runner[C_IDX]])

    person_for_square = sorted(smallest_square_list, key = lambda x:(x[R_IDX], x[C_IDX]))[0]
    down_r, down_c = sorted([person_for_square, _exit], key = lambda x:(x[0], x[1]))[-1]

    upper_r = 0 if down_r - shortest_length <= 0 else down_r - shortest_length
    upper_c = 0 if down_c - shortest_length <= 0 else down_c - shortest_length

    return upper_r, upper_c, shortest_length

def is_in_square(upper_r, upper_c, length, runner) :
    if (upper_r <= runner[R_IDX] <= upper_r + length) and (upper_c <= runner[C_IDX] <= upper_c + length) :
        return True
    else :
        return False


def rotate(upper_r, upper_c, length) :
    global _runner_list, _exit

    ## maze rotate
    temp_for_rotate = [[0 for _ in range(N)] for _ in range(N)]
    for r_ in range(upper_r, upper_r+length+1) :
        for c_ in range(upper_c, upper_c+length+1) :
            i_ = r_ - upper_r
            j_ = c_ - upper_c

            temp_for_rotate[upper_r + j_][upper_c + length - i_] = _maze[r_][c_]

    for r_ in range(upper_r, upper_r+length+1):
        for c_ in range(upper_c, upper_c+length+1):
            _maze[r_][c_] = max(temp_for_rotate[r_][c_]-1, 0)

    ## runner rotate
    for idx, runner in enumerate(_runner_list) :
        if not is_in_square(upper_r, upper_c, length, runner):
            # print("idx")
            # print(upper_r, upper_c, length, runner)
            continue
        i_ = runner[R_IDX] - upper_r
        j_ = runner[C_IDX] - upper_c

        _runner_list[idx][R_IDX] = upper_r + j_
        _runner_list[idx][C_IDX] = upper_c + length - i_

    ## exit rotate
    if is_in_square(upper_r, upper_c, length, _exit) :
        i_ = _exit[R_IDX] - upper_r
        j_ = _exit[C_IDX] - upper_c

        _exit[R_IDX] = upper_r + j_
        _exit[C_IDX] = upper_c + length - i_

def print_maze(maze) :
    for _ in maze :
        print(_)
    print()

def print_runner() :
    temp = [[0 for _ in range(N)] for _ in range(N)]

    for runner in _runner_list :
        temp[runner[R_IDX]][runner[C_IDX]] = 1

    temp[_exit[R_IDX]][_exit[C_IDX]] = 'x'
    for t in temp :
        print(t)
    print()


if __name__ == '__main__' :
    for round in range(K) :
        ## 참가자 이동
        move_runners()
        # print_maze(_maze)
        # print_runner()

        ## 정사각형 만들기
        upper_r, upper_c, length = find_smallest_square()
        # print(upper_r, upper_c, length, '\n')
        rotate(upper_r, upper_c, length)

        # print_maze(_maze)
        # print_runner()
        # print(f'-----{round+2}-----')

    print(_move_score)
    print(_exit[R_IDX]+1, _exit[C_IDX]+1)