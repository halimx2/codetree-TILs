import copy

## M: 몬스터 수
## T: 전체 라운드
M, T = list(map(int, input().split()))

## 팩맨 위치
_r_packman, _c_packman = list(map(int, input().split()))
_r_packman -= 1
_c_packman -= 1

## 몬스터 위치
_monster_list = []
_dead_monster_list = []
R_IDX = 0
C_IDX = 1
D_IDX = 2
for _ in range(M) :
    monster_ = list(map(int, input().split()))
    monster_[R_IDX] -= 1
    monster_[C_IDX] -= 1
    monster_[D_IDX] -= 1
    _monster_list.append(monster_)

def duplicate_monster():
    return copy.deepcopy(_monster_list)

def is_there_dead_monster(r, c,) :
    if not _dead_monster_list :
        return False

    for dead_monster in _dead_monster_list:
        if (dead_monster[R_IDX], dead_monster[C_IDX]) == (r, c) :
            return True
    else :
        return False

def monster_move(monster, idx) :
    global _monster_list

    d_r = [-1, -1, 0, 1, 1, 1, 0, -1] # 반시계 방향 45도
    d_c = [0, -1, -1, -1, 0, 1, 1, 1]

    r = monster[R_IDX]
    c = monster[C_IDX]
    direction = monster[D_IDX]

    for rotate_time in range(8) :
        d_r_ = d_r[(direction + rotate_time)%8]
        d_c_ = d_c[(direction + rotate_time)%8]

        r_ = r + d_r_
        c_ = c + d_c_

        if not(0 <= r_ < 4) or not(0 <= c_ < 4) :
            continue

        if is_there_dead_monster(r_, c_) :
            continue

        if (r_, c_) == (_r_packman, _c_packman) :
            continue

        _monster_list[idx][R_IDX] += d_r_
        _monster_list[idx][C_IDX] += d_c_
        _monster_list[idx][D_IDX] = (direction + rotate_time)%8
        break

    else :
        pass


def is_there_monster(r, c,) :
    for monster in _monster_list :
        if (monster[R_IDX], monster[C_IDX]) == (r, c) :
            return True

    else :
        return False

_d_r_packman = [-1, 0, 1, 0]
_d_c_packman = [0, -1, 0, 1]
_route_list = []

def dfs(r, c, direction_list, cnt_eating_monster):
    global _route_list

    if len(direction_list) >= 3 :
        _route_list.append([r, c, direction_list.copy(), cnt_eating_monster])
        return 0

    for direction in range(4):
        r_ = r + _d_r_packman[direction]
        c_ = c + _d_c_packman[direction]

        if not (0 <= r_ < 4) or not (0 <= c_ < 4):
            continue

        if is_there_monster(r_, c_) :
            cnt_eating_monster += 1

        direction_list.append(direction)
        dfs(r_, c_, direction_list, cnt_eating_monster)
        direction_list.pop()
        # print('-', direction_list, cnt_eating_monster)
        # direction_list = direction_list[:cnt]

def packman_move() :
    global _dead_monster_list, _r_packman, _c_packman, _route_list

    _route_list = []

    dfs(_r_packman, _c_packman, [], 0)
    best_route = sorted(_route_list, key = lambda x:(-x[3], x[2]))[0]
    # print("route:", _route_list)
    # print("best:", best_route)
    remove_list = []
    for direction in best_route[2] : # direction_list
        _r_packman += _d_r_packman[direction]
        _c_packman += _d_c_packman[direction]

        for idx, monster in enumerate(_monster_list) :
            if (monster[R_IDX], monster[C_IDX]) == (_r_packman, _c_packman):
                remove_list.append(idx)

                monster = monster[:2]
                monster.append(3)
                _dead_monster_list.append(monster)

    remove_list.sort(reverse=True)
    # print("remove:", remove_list)
    # print(remove_list)
    for idx in remove_list :
        # print(idx)
        # print(_monster_list)
        _monster_list.pop(idx)
        # print(_monster_list)

def print_map() :
    maze_ = [[0 for _ in range(4)] for _ in range(4)]

    for r, c, d in _monster_list :
        maze_[r][c] += 1

    maze_[_r_packman][_c_packman] = '-'

    for line in maze_ :
        print(line)
    print()


def remove_dead_monster() :
    global _dead_monster_list

    remove_list = []
    for idx, dead_monster in enumerate(_dead_monster_list) :
        dead_monster[2] -= 1

        if dead_monster[2] == 0 :
            remove_list.append(idx)

    remove_list.sort(reverse=True)
    for idx in remove_list :
        _dead_monster_list.pop(idx)

def make_monster(eggs_list) :
    global _monster_list

    for egg in eggs_list :
        _monster_list.append(egg)

if __name__ == '__main__' :
    for round in range(T) :
        # print_map()
        eggs_list = duplicate_monster()

        # print(_monster_list)
        for idx, monster in enumerate(_monster_list) :
            monster_move(monster, idx)
        # print(_monster_list)
        # print()
        # print('after monsters move')
        # print_map()
        packman_move()
        remove_dead_monster()

        make_monster(eggs_list)
        # print('after packman move')
        # print(_monster_list)
        # print_map()
        # print('-----------')

    print(len(_monster_list))
    # print_map()
    # print(_monster_list)