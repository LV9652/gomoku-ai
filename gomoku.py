import copy
from classes import Board


class MoveTree:
    def __init__(self, board: list, move: tuple, is_turn: bool) -> None:
        self.board = board
        self.move = move
        self.score = None
        self.is_turn = is_turn
        self.alpha = -1
        self.beta = 100000
        self.parent = None
        self.children = []

    def add_child(self, child) -> None:
        child.parent = self
        if self.is_turn:
            for kid in self.children:
                if kid.score > child.alpha:
                    child.alpha = kid.score
        else:
            for kid in self.children:
                if kid.score > child.beta:
                    child.beta = kid.score

        self.children.append(child)

    def set_score(self, score: int) -> None:
        self.score = score
        if self.parent:
            if self.is_turn:
                self.parent.alpha = score
            else:
                self.parent.beta = score

    def is_valid(self) -> bool:
        return self.beta > self.alpha

    def get_num_leafs(self, tree):
        if tree.children == []:
            return 1
        num = 0
        for child in tree.children:
            num += self.get_num_leafs(child)
        return num
        


class PlayerLV:
    def __init__(self, id: int, stone: str) -> None:
        self.id = id
        self.opp = 3 - id
        self.stone = stone

    def extend_in_four_directions(self, board: list, move: tuple) -> dict:
        lis = []
        i = move[0]
        j = move[1]

        cur_row = '3'
        idx_row = [(len(board), len(board))]
        for k in range(len(board)):
            cur_row += str(board[i][k])
            idx_row.append((i, k))
        cur_row += '3'
        idx_row.append((len(board), len(board)))
        lis.append((cur_row, idx_row))

        cur_col = '3'
        idx_col = [(len(board), len(board))]
        for k in range(len(board)):
            cur_col += str(board[k][j])
            idx_col.append((k, j))
        cur_col += '3'
        idx_col.append((len(board), len(board)))
        lis.append((cur_col, idx_col))

        cur_backslash = '3'
        idx_backslash = [(len(board), len(board))]
        for k in range(max(-i, -j), min(len(board) - i, len(board) - j)):
            cur_backslash += str(board[i+k][j+k])
            idx_backslash.append((i+k,j+k))
        cur_backslash += '3'
        idx_backslash.append((len(board), len(board)))
        lis.append((cur_backslash, idx_backslash))

        cur_slash = '3'
        idx_slash = [(len(board), len(board))]
        for k in range(max(-i, j - len(board) + 1), min(len(board) - i, j + 1)):
            cur_slash += str(board[i+k][j-k])
            idx_slash.append((i+k,j-k))
        cur_slash += '3'
        idx_slash.append((len(board), len(board)))
        lis.append((cur_slash, idx_slash))

        return lis

    def win_move(self, cur_row: str, for_row: str, id: int) -> int:
        opp = 3 - id

        ptn_5_id = str(id) * 5
        ptn_040_id = '0' + str(id) * 4 + '0'
        ptn_041_id = '0' + str(id) * 4 + str(opp)
        ptn_140_id = str(opp) + str(id) * 4 + '0'
        ptn_301_id = str(id) * 3 + '0' + str(id)
        ptn_103_id = str(id) + '0' + str(id) * 3
        ptn_202_id = str(id) * 2 + '0' + str(id) * 2
        ptn_40_id = '3' + str(id) * 4 + '0'
        ptn_04_id = '0' + str(id) * 4 + '3'

        ptn_02010_id = '0' + str(id) * 2 + '0' + str(id) + '0'
        ptn_01020_id = '0' + str(id) + '0' + str(id) * 2 + '0'

        if id == self.id:
            if ptn_5_id in cur_row:
                return 10 

            elif ptn_040_id in cur_row:
                return 5 

            elif ptn_301_id in cur_row or ptn_103_id in cur_row or ptn_202_id in cur_row or ptn_041_id in cur_row or ptn_140_id in cur_row or ptn_40_id in cur_row or ptn_04_id in cur_row:
                return 4 
        else:
            if ptn_5_id in cur_row:
                return -4

            elif ptn_040_id in cur_row:
                return -3

            elif ptn_301_id in cur_row or ptn_103_id in cur_row or ptn_202_id in cur_row:
                if ptn_02010_id in for_row or ptn_01020_id in for_row:
                    return -3

        return -1
    
    def get_moves(self, board: list, id: int) -> list:
        moves = []
        move_dic = {}
        opp = 3 - id

        extended_board = [[0 for i in range(len(board) + 4)] for j in range(len(board) + 4)]
        for a in range(len(board)):
            for b in range(len(board)):
                extended_board[a+2][b+2] = board[a][b]

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    surround_1 = [extended_board[i-1+2][j-1+2], extended_board[i-1+2][j+2], extended_board[i-1+2][j+1+2], 
                                  extended_board[i+2][j-1+2], extended_board[i+2][j+1+2], 
                                  extended_board[i+1+2][j-1+2], extended_board[i+1+2][j+2], extended_board[i+1+2][j+1+2]]
                    surround_2 = [extended_board[i-2+2][j-2+2], extended_board[i-2+2][j+2], extended_board[i-2+2][j+2+2], 
                                  extended_board[i+2][j-2+2], extended_board[i+2][j+2+2], 
                                  extended_board[i+2+2][j-2+2], extended_board[i+2+2][j+2], extended_board[i+2+2][j+2+2]]
                    original_rows = self.extend_in_four_directions(board, (i, j))
                    if any(surround_1) or id in surround_2:
                        new_board = copy.deepcopy(board)
                        new_board[i][j] = self.id
                        next_row = self.extend_in_four_directions(new_board, (i, j))

                        for k in range(4):
                            sign = self.win_move(next_row[k][0], original_rows[k][0], self.id)
                            if sign != -1:
                                if sign in move_dic:
                                    move_dic[sign].append((i, j))
                                else:
                                    move_dic[sign] = [(i, j)]
                        
                        moves.append((i, j))

                    if any(surround_1) or opp in surround_2:
                        new_board = copy.deepcopy(board)
                        new_board[i][j] = self.opp
                        next_row = self.extend_in_four_directions(new_board, (i, j))

                        for k in range(4):
                            sign = self.win_move(next_row[k][0], original_rows[k][0], self.opp)
                            if sign != -1:
                                if sign in move_dic:
                                    move_dic[sign].append((i, j))
                                else:
                                    move_dic[sign] = [(i, j)]

        # print("move_dic: " + str(move_dic))

        if 10 in move_dic:
            return []
        elif -4 in move_dic:
            return move_dic[-4][:1]
        elif 5 in move_dic:
            return move_dic[5][:1]
        elif -3 in move_dic:
            if 4 in move_dic:
                return move_dic[4] + move_dic[-3]
            else:
                return move_dic[-3]
        return moves

    def evaluate_score(self, cur_row: str, move_idx: int) -> int:
        ptn_5_id = str(self.id) * 5
        ptn_040_id = '0' + str(self.id) * 4 + '0'
        ptn_303_id= str(self.id) * 3 + '0' + str(self.id) * 3
        ptn_10301_id = str(self.id) + '0' + str(self.id) * 3 + '0' + str(self.id)
        ptn_20202_id = str(self.id) * 2 + '0' + str(self.id) * 2 + '0' + str(self.id) * 2

        ptn_041_id = '0' + str(self.id) * 4 + str(self.opp)
        ptn_140_id = str(self.opp) + str(self.id) * 4 + '0'
        ptn_301_id = str(self.id) * 3 + '0' + str(self.id)
        ptn_103_id = str(self.id) + '0' + str(self.id) * 3
        ptn_202_id = str(self.id) * 2 + '0' + str(self.id) * 2
        ptn_40_id = '3' + str(self.id) * 4 + '0'
        ptn_04_id = '0' + str(self.id) * 4 + '3'

        ptn_030_id = '0' + str(self.id) * 3 + '0'
        ptn_02010_id = '0' + str(self.id) * 2 + '0' + str(self.id) + '0'
        ptn_01020_id = '0' + str(self.id) + '0' + str(self.id) * 2 + '0'

        ptn_021_opp = '0' + str(self.opp) * 2 + str(self.id)
        ptn_120_opp = str(self.id) + str(self.opp) * 2 + '0'

        # ptn_01010_opp, ptn_01010_id

        ptn_130_opp = str(self.id) + str(self.opp) * 3 + '0'
        ptn_031_opp = '0' + str(self.opp) * 3 + str(self.id)
        ptn_02110_opp = '0' + str(self.opp) * 2 + str(self.id) + str(self.opp) + '0'
        ptn_01120_opp = '0' + str(self.opp) + str(self.id) + str(self.opp) * 2 + '0'
        ptn_12010_opp = str(self.id) + str(self.opp) * 2 + '0' + str(self.opp) + '0'
        ptn_02011_opp = '0' + str(self.opp) * 2 + '0' + str(self.opp) + str(self.id)
        ptn_01021_opp = '0' + str(self.opp) + '0' + str(self.opp) * 2 + str(self.id)
        ptn_11020_opp = str(self.id) + str(self.opp) + '0' + str(self.opp) * 2 + '0'

        ptn_020_id = '0' + str(self.id) * 2 + '0'

        ptn_130_id = str(self.opp) + str(self.id) * 3 + '0'
        ptn_031_id = '0' + str(self.id) * 3 + str(self.opp)

        ptn_03_id = '0' + str(self.id) * 3 + '3'
        ptn_30_id = '3' + str(self.id) * 3 + '0'
        ptn_0201_id = '0' + str(self.id) * 2 + '0' + str(self.id) + '3'
        ptn_2010_id = '3' + str(self.id) * 2 + '0' + str(self.id) + '0'
        ptn_0102_id = '0' + str(self.id) + '0' + str(self.id) * 2 + '3'
        ptn_1020_id = '3' + str(self.id) + '0' + str(self.id) * 2 + '0'

        ptn_110_opp = str(self.id) + str(self.opp) + '0'
        ptn_011_opp = '0' + str(self.opp) + str(self.id)

        score = 0
        cur_row_7 = cur_row[max(move_idx - 7, 0): min(move_idx + 8, len(cur_row))]
        cur_row_6 = cur_row[max(move_idx - 6, 0): min(move_idx + 7, len(cur_row))]
        cur_row_5 = cur_row[max(move_idx - 5, 0): min(move_idx + 6, len(cur_row))]
        cur_row_4 = cur_row[max(move_idx - 4, 0): min(move_idx + 5, len(cur_row))]
        cur_row_3 = cur_row[max(move_idx - 3, 0): min(move_idx + 4, len(cur_row))]
        cur_row_2 = cur_row[max(move_idx - 2, 0): min(move_idx + 3, len(cur_row))]

        if ptn_5_id in cur_row_4 or ptn_040_id in cur_row_4 or ptn_303_id in cur_row_6 or ptn_10301_id in cur_row_6 or ptn_20202_id in cur_row_7:
            score += 1000

        elif ptn_030_id in cur_row_3:
            score += 10

        elif ptn_02010_id in cur_row_4 or ptn_01020_id in cur_row_4:
            score += 9

        elif ptn_041_id in cur_row_4 or ptn_140_id in cur_row_4 or ptn_301_id in cur_row_4 or ptn_103_id in cur_row_4 or ptn_202_id in cur_row_4 or ptn_40_id in cur_row_4 or ptn_04_id in cur_row_4:
            score += 8
        
        elif ptn_130_opp in cur_row_4 or ptn_031_opp in cur_row_4 or ptn_02110_opp in cur_row_3 or ptn_01120_opp in cur_row_3:
            score += 5
        elif ptn_12010_opp in cur_row_5 or ptn_01021_opp in cur_row_5 or ptn_02011_opp in cur_row_5 or ptn_11020_opp in cur_row_5:
            score += 4

        elif ptn_021_opp in cur_row_3 or ptn_120_opp in cur_row_3:
            score += 5
        elif ptn_020_id in cur_row_2:
            score += 4
        elif ptn_130_id in cur_row_3 or ptn_031_id in cur_row_3:
            score += 3
        elif ptn_03_id in cur_row_3 or ptn_30_id in cur_row_3 or ptn_0201_id in cur_row_3 or ptn_2010_id in cur_row_3 or ptn_0102_id in cur_row_3 or ptn_1020_id in cur_row_3:
            score += 1
        elif ptn_011_opp in cur_row_2 or ptn_110_opp in cur_row_2:
            score += 1

        return score

    def calculate_score(self, tree, board: list, id: int, steps: int) -> None:
        if not tree.is_valid():
            print("haha")
            return None

        moves = self.get_moves(board, id)
        # print("moves: " + str(moves))
        # if len(moves) > 10:
        #     moves = moves[:8]

        if steps <= 0 or moves == []:
            row_lis = self.extend_in_four_directions(tree.board, tree.move)
            score = 0
            for cur_row in row_lis:
                score += self.evaluate_score(cur_row[0], cur_row[1].index(tree.move))
            tree.set_score(score)
            # print("Steps and Score -- " + str(steps) + ": " + str(score))
            return None

        for move in moves:
            next_board = copy.deepcopy(board)
            next_board[move[0]][move[1]] = id
            next_tree = MoveTree(next_board, move, id == self.id)
            tree.add_child(next_tree)

            self.calculate_score(next_tree, next_board, 3 - id, steps - 1)

        if tree.is_turn:
            tree.set_score(tree.beta)
        else:
            tree.set_score(tree.alpha)
        final_score = tree.score
        print("final score: " + str(steps) + " -- " + str(tree.move) + " -- " + str(final_score))


    def move(self, board: Board) -> tuple:
        moves = self.get_moves(board.board, self.id)
        if len(moves) == 1:
            return moves[0]
        elif len(moves) == 0:
            return (7, 7)

        move_tree = MoveTree(board.board, board.last_move, False)

        self.calculate_score(move_tree, board.board, self.id, 2)

        print("num_of_leafs: " + str(move_tree.get_num_leafs(move_tree)))

        max_score = -1
        max_child = None
        for child in move_tree.children:

            print("Then: " + str(child.move) + ", " + str(child.score))

            if child.score is not None and child.score > max_score:
                max_child = child
                max_score = child.score
        
        return max_child.move



