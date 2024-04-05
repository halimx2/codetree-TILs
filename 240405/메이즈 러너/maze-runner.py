import copy
from collections import deque

# 입력 및 시작
N, M, K = list(map(int, input().split()))

maze = []
for _ in range(N) :
    maze.append(list(map(int, input().split())))


for _ in range(M) :
    [r,c] = list(map(int, input().split()))
    maze[r - 1][c - 1] = -1

EXIT_NUM = N*N*N

r,c = list(map(int, input().split()))
maze[r - 1][c - 1] = EXIT_NUM
CNT = copy.deepcopy(M)

d_r = [-1, 1, 0, 0]
d_c = [0, 0, 1, -1]

ANSWER_CNT = 0

def can_go(r,c) :
    if maze[r][c] > 0 :
        return True
    else :
        return False

def distance(r1, c1, r2, c2) :
    return abs(r1-r2) + abs(c1-c2)

def move_people() :
    people = []
    global ANSWER_CNT

    for r in range(N) :
        for c, box in enumerate(maze[r]) :
            if box <= -1 :
                people.append([r,c])
            elif box == EXIT_NUM :
                exit_r = r
                exit_c = c

    for person_r, person_c in people :
        for d_r_, d_c_ in zip(d_r, d_c) :
            if person_r + d_r_ < 0 or person_c + d_c_ < 0 :
                continue

            try :
                if maze[person_r+d_r_][person_c+d_c_] == EXIT_NUM :
                    ANSWER_CNT += abs(maze[person_r][person_c])
                    # print('---', maze[person_r][person_c])
                    maze[person_r][person_c] = 0


                    break

                origin_distance = distance(person_r, person_c, exit_r, exit_c)
                moved_distance = distance(person_r + d_r_, person_c + d_c_, exit_r, exit_c)

                if origin_distance < moved_distance :
                    continue

                if maze[person_r+d_r_][person_c+d_c_] == 0 :
                    maze[person_r+d_r_][person_c+d_c_] = maze[person_r][person_c]
                    # print(maze[person_r+d_r_][person_c+d_c_])

                    maze[person_r][person_c] = 0

                    ANSWER_CNT += abs(maze[person_r+d_r_][person_c+d_c_])

                    break

                elif maze[person_r+d_r_][person_c+d_c_] <= -1 :
                    maze[person_r+d_r_][person_c+d_c_] += maze[person_r][person_c]
                    # print(maze[person_r+d_r_][person_c+d_c_])

                    maze[person_r][person_c] = 0

                    ANSWER_CNT += abs(maze[person_r+d_r_][person_c+d_c_])

                    break

            except IndexError :
                pass

    return [exit_r, exit_c]

def find_smallest_rectangle(r, c) :
    """
    bfs 사용해
    :return:
    """
    answer_list = []
    visited = [[False for _ in range(N)] for _ in range(N)]
    cnt = 0
    q = deque()
    q.append([r, c, cnt])
    d_r = [1, -1, 0, 0]
    d_c = [0, 0, 1, -1]
    smallest_cnt = 99999
    while q:
        [r, c, cnt] = q.popleft()
        # print([r, c, cnt])
        if cnt > smallest_cnt :
            break

        visited[r][c] = True

        for d_r_, d_c_ in zip(d_r, d_c) :
            if not(N > r+d_r_ >= 0) or not(N > c+d_c_ >= 0) :
                continue

            if visited[r+d_r_][c+d_c_] :
                continue

            if maze[r+d_r_][c+d_c_] == -1 :
                answer_list.append([r+d_r_, c+d_c_])
                smallest_cnt = cnt+1
            else :
                q.append([r+d_r_, c+d_c_, cnt+1])

    if not answer_list :
        return [-1 ,-1]
    elif len(answer_list) == 1 :
        return answer_list[0]
    else :
        answer_list.sort(key = lambda x:(x[0], x[1]))
        return answer_list[0]

def rotate_square(person_r, person_c, exit_r, exit_c) :
    length = max(abs(person_r -exit_r), abs(person_c - exit_c))

    r, c = max([person_r, person_c], [exit_r, exit_c])
    r_sub, c_sub = min([person_r, person_c], [exit_r, exit_c])

    r_start = max(person_r-length, exit_r-length, 0)
    c_start = max(person_c-length, exit_c-length, 0)

    maze_ = [line[c_start:c_start+length+1] for line in maze[r_start:r_start+length+1]]
    maze_ = list(map(list, zip(*maze_[::-1])))

    for r_ in range(r_start, r_start+length+1) :
        for c_ in range(c_start, c_start+length+1) :
            if maze_[r_ - r_start][c_ - c_start] in [-1, EXIT_NUM] :
                maze[r_][c_] = maze_[r_ - r_start][c_ - c_start]
                continue

            maze[r_][c_] = max(maze_[r_ - r_start][c_ - c_start]-1, 0)



if __name__ == "__main__" :
    for _ in range(K) :
        [exit_r, exit_c] = move_people()
        person_r, person_c = find_smallest_rectangle(exit_r, exit_c)

        if person_r == -1 and person_c == -1 :
            break
        rotate_square(person_r, person_c, exit_r, exit_c)

    break_ = False
    for r in range(len(maze)) :
        for c in range(len(maze[0])) :
            if maze[r][c] == EXIT_NUM :
                answer = [r,c]
                break_ = True
                break

        if break_ :
            break

    # for _ in maze :
    #     print(_)
    
    print(ANSWER_CNT)
    print(answer[0]+1, answer[1]+1)