N, M, K = list(map(int, input().split()))

GUN_MAP = []
for _ in range(N) :
    GUN_MAP.append(list(map(int, input().split())))

PLAYERS = []
NO_PLAYER = -1

IS_THERE_PLAYER = [[NO_PLAYER for _ in range(N)] for _ in range(N)]

R_IDX = 0
C_IDX = 1
DIRECTION_IDX = 2
SKILL_IDX = 3
GUN_IDX = 4

for idx in range(M) :
    info = list(map(int, input().split())) # r, c, d(direction), s(skill)
    info[0] -= 1
    info[1] -= 1
    info.append(0) # gun 추가
    PLAYERS.append(info) # r:0, c:1, direction:2, skill:3, gun:4

    IS_THERE_PLAYER[info[0]][info[1]] = idx

d_r = [-1, 0, 1, 0]
d_c = [0, 1, 0, -1]

def player_move(idx) :
    r, c, direction, skill, gun = PLAYERS[idx]

    r_ = r + d_r[direction]
    c_ = c + d_c[direction]

    if not(0 <= r_ < N) or not(0 <= c_ < N) :
        r_ = r + d_r[(direction+2)%4]
        c_ = c + d_c[(direction+2)%4]
        PLAYERS[idx][DIRECTION_IDX] = (direction+2)%4

    IS_THERE_PLAYER[r][c] = NO_PLAYER
    PLAYERS[idx][0] = r_
    PLAYERS[idx][1] = c_

    if IS_THERE_PLAYER[r_][c_] != NO_PLAYER :
        return [True, IS_THERE_PLAYER[r_][c_]]
    else :
        IS_THERE_PLAYER[r_][c_] = idx
        return [False, NO_PLAYER]


def loser_player_move(loser_idx) :
    r = PLAYERS[loser_idx][R_IDX]
    c = PLAYERS[loser_idx][C_IDX]
    direction = PLAYERS[loser_idx][DIRECTION_IDX]

    for _ in range(4) :
        direction_ = (direction + _) % 4
        r_ = r + d_r[direction_]
        c_ = c + d_c[direction_]

        if not(0 <= r_ < N) or not(0 <= c_ < N) or IS_THERE_PLAYER[r_][c_] != NO_PLAYER :
            continue

        PLAYERS[loser_idx][R_IDX] = r_
        PLAYERS[loser_idx][C_IDX] = c_
        PLAYERS[loser_idx][DIRECTION_IDX] = direction_

        IS_THERE_PLAYER[r][c] = IS_THERE_PLAYER[r_][c_]
        IS_THERE_PLAYER[r_][c_] = NO_PLAYER

        break

    else :
        print("--- 에러 인듯..? ---")

def player_fight(player_idx, fight_player_idx, point_list) :
    r, c = PLAYERS[player_idx][R_IDX], PLAYERS[player_idx][C_IDX]

    player_power = PLAYERS[player_idx][SKILL_IDX]+PLAYERS[player_idx][GUN_IDX]
    fight_player_power = PLAYERS[fight_player_idx][SKILL_IDX]+PLAYERS[fight_player_idx][GUN_IDX]

    # 승자와 패자 정하기
    if player_power > fight_player_power :
        winner_idx = player_idx
        loser_idx = fight_player_idx
    elif player_power < fight_player_power:
        winner_idx = fight_player_idx
        loser_idx = player_idx
    else :
        if PLAYERS[player_idx][SKILL_IDX] > PLAYERS[fight_player_idx][SKILL_IDX] :
            winner_idx = player_idx
            loser_idx = fight_player_idx
        elif PLAYERS[player_idx][SKILL_IDX] < PLAYERS[fight_player_idx][SKILL_IDX] :
            winner_idx = fight_player_idx
            loser_idx = player_idx
        else :
            print('에러')

    ## 진 플레이어가 해야할 것들
    ## 1) 총 내려두기
    GUN_MAP[r][c] = max(GUN_MAP[r][c], PLAYERS[loser_idx][GUN_IDX])
    PLAYERS[loser_idx][GUN_IDX] = 0

    ## 2) 이동
    loser_player_move(loser_idx)

    ## 3) 이동 후 총 줍기
    change_gun(loser_idx)


    ## 이긴 플레이어가 해야할 것들
    ## 1) 총 줍기
    change_gun(winner_idx)
    point_list[winner_idx] += abs(player_power - fight_player_power)

    return point_list

def change_gun(player_idx) :
    r_ = PLAYERS[player_idx][R_IDX]
    c_ = PLAYERS[player_idx][C_IDX]
    gun_list = [PLAYERS[player_idx][GUN_IDX], GUN_MAP[r_][c_]]

    PLAYERS[player_idx][GUN_IDX] = max(gun_list)
    GUN_MAP[r_][c_] = min(gun_list)


if __name__ == '__main__' :
    point_list = [0 for _ in range(M)]

    for round in range(K) :
        for player_idx in range(M) :
            is_fight, fight_player_idx = player_move(player_idx)

            if is_fight :
                point_list = player_fight(player_idx, fight_player_idx, point_list)
            else :
                change_gun(player_idx)

    for point in point_list :
        print(point, end = ' ')