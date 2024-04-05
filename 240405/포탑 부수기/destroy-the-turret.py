import copy
from collections import deque

N, M, K = list(map(int, input().split()))

TURRET_MAP = []
for _ in range(M):
    TURRET_MAP.append(list(map(int, input().split())))


def find_attack_turret(attack_time_list):
    weakest_attack = 5001
    weakest_turret_list = []
    for r in range(M):
        for c in range(N):
            if TURRET_MAP[r][c] == 0:
                continue
            if TURRET_MAP[r][c] == weakest_attack:
                weakest_turret_list.append({'index': [r, c], 'time': attack_time_list[r][c]})
            elif TURRET_MAP[r][c] < weakest_attack:
                weakest_attack = TURRET_MAP[r][c]
                weakest_turret_list = [{'index': [r, c], 'time': attack_time_list[r][c]}]

    if len(weakest_turret_list) == 1:
        weakest_turret_list.sort(key=lambda x: (x['time'], -sum(x['index']), -x['index'][1]))

    r = weakest_turret_list[0]['index'][0]
    c = weakest_turret_list[0]['index'][1]

    TURRET_MAP[r][c] += N + M

    return weakest_turret_list[0]['index']


def find_attacked_turret(attack_time_list):
    strongest_attack = -1
    strongest_attack_list = []
    for r in range(M):
        for c in range(N):
            if TURRET_MAP[r][c] == 0:
                continue
            if TURRET_MAP[r][c] == strongest_attack:
                strongest_attack_list.append({'index': [r, c], 'time': attack_time_list[r][c]})
            elif TURRET_MAP[r][c] > strongest_attack:
                strongest_attack = TURRET_MAP[r][c]
                strongest_attack_list = [{'index': [r, c], 'time': attack_time_list[r][c]}]

    if len(strongest_attack_list) > 1:
        strongest_attack_list.sort(key=lambda x: (x['time'], -sum(x['index']), -x['index'][1]))

    return strongest_attack_list[0]['index']


def razor_attack(attack_r, attack_c, attacked_r, attacked_c) :
    visited = [[False for _ in range(N)] for _ in range(M)]
    cnt = 0
    q = deque()
    q.append([attack_r, attack_c, cnt, [[attack_r, attack_c]]])

    dr = [0, 1, 0, 1]
    dc = [1, 0, -1, 0]
    answer_route = []
    find_shortest_path = False
    while q :
        r, c, cnt, route = q.popleft()
        visited[r][c] = True

        for dr_, dc_ in zip(dr, dc) :
            r_ = (r + dr_)%M
            c_ = (c + dc_)%N

            if visited[r_][c_] or TURRET_MAP[r_][c_] == 0:
                continue

            route_ = copy.deepcopy(route)
            route_.append([r_, c_])

            if (r_, c_) == (attacked_r, attacked_c) :
                answer_route = route_
                find_shortest_path = True
                break

            q.append([r_, c_, cnt+1, route_])

        if find_shortest_path :
            break

    if answer_route :
        return answer_route
    else :
        return False

def bomb_attack(attack_r, attack_c, attacked_r, attacked_c) :
    attack_power = TURRET_MAP[attack_r][attack_c]

    TURRET_MAP[attacked_r][attacked_c] -= attack_power
    dr = [0, 0, 1, 1, 1, -1, -1, -1]
    dc = [1, -1, 1, -1, 0, 1, -1, 0]

    route = []
    for dr_, dc_ in zip(dr, dc) :
        r_, c_ = (r+dr_)%M, (c+dc_)%N
        if TURRET_MAP[r_][c_] > 0 or (r_, c_) != (attacked_r, attacked_c) :
            TURRET_MAP[r_][c_] = max(TURRET_MAP[r_][c_]-attack_power//2, 0)
            route.append([r_, c_])

    return route

def give_one_more_life(route) :
    for r in range(M) :
        for c in range(N) :
            if TURRET_MAP[r][c] == 0 or [r,c] in route:
                continue

            TURRET_MAP[r][c] += 1

if __name__ == '__main__':
    for _ in range(K) :
        attack_time_list = [[0 for _ in range(N)] for _ in range(M)]

        attack_r, attack_c = find_attack_turret(attack_time_list)
        attacked_r, attacked_c = find_attacked_turret(attack_time_list)

        route = razor_attack(attack_r, attack_c, attacked_r, attacked_c)

        if route :
            # 경로로 공격
            attack_power = TURRET_MAP[attack_r][attack_c]
            for r,c in route :
                if (r,c) == (attack_r, attack_c) :
                    continue

                if (r,c) == (attacked_r, attacked_c) :
                    TURRET_MAP[r][c] -= attack_power
                    continue

                TURRET_MAP[r][c] = max(TURRET_MAP[r][c]-attack_power//2, 0)
        else :
            route = bomb_attack(attack_r, attack_c, attacked_r, attacked_c)

        # for _ in range(M):
        #     print(TURRET_MAP[_])
        # print()

        route.append([attack_r, attack_c])
        route.append([attacked_r, attacked_c])

        give_one_more_life(route)


        # for _ in range(M):
        #     print(TURRET_MAP[_])
        # print()

    answer = -1
    for r in range(M) :
        for c in range(N) :
            if TURRET_MAP[r][c] > answer :
                answer = TURRET_MAP[r][c]

    print(answer)