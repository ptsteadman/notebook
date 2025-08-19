import sys
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict

from rota import RotaAPI


# Board representation helpers
# Positions are 1..9 laid out like a keypad with 5 as the center.
# The ring order clockwise is: 1 -> 2 -> 3 -> 6 -> 9 -> 8 -> 7 -> 4 -> (back to 1)
# Adjacency allows moves along the ring to immediate neighbors and between center (5) and any ring node.
ADJACENT_POSITIONS: Dict[int, List[int]] = {
    1: [2, 4, 5],
    2: [1, 3, 5],
    3: [2, 6, 5],
    4: [1, 7, 5],
    5: [1, 2, 3, 4, 6, 7, 8, 9],
    6: [3, 9, 5],
    7: [4, 8, 5],
    8: [7, 9, 5],
    9: [6, 8, 5],
}


# Winning lines: any 3 consecutive on the ring, and any line across the center (5) between opposite ring nodes
RING_ORDER: List[int] = [1, 2, 3, 6, 9, 8, 7, 4]
RING_TRIPLES: List[List[int]] = [
    [RING_ORDER[i], RING_ORDER[(i + 1) % 8], RING_ORDER[(i + 2) % 8]] for i in range(8)
]
CENTER_LINES: List[List[int]] = [
    [1, 5, 9],
    [2, 5, 8],
    [3, 5, 7],
    [4, 5, 6],
]
WINNING_LINES: List[List[int]] = RING_TRIPLES + CENTER_LINES


def print_board(board: str) -> None:
    # Pretty 3x3 grid with 5 as center
    rows = [
        f"{board[0]} {board[1]} {board[2]}",
        f"{board[3]} {board[4]} {board[5]}",
        f"{board[6]} {board[7]} {board[8]}",
    ]
    print("\n".join(rows), flush=True)


def extract_board(obj) -> str:
    if isinstance(obj, dict):
        # Standard JSON
        if "board" in obj and isinstance(obj["board"], str) and len(obj["board"]) == 9:
            return obj["board"]
        # Nested JSON
        for key in ("state", "result", "data"):
            value = obj.get(key)
            if isinstance(value, dict):
                if "board" in value and isinstance(value["board"], str) and len(value["board"]) == 9:
                    return value["board"]
                if "state" in value and isinstance(value["state"], str) and len(value["state"]) == 9 and set(value["state"]) <= set("-pc"):
                    return value["state"]
            if isinstance(value, str) and len(value) == 9 and set(value) <= set("-pc"):
                return value
        # Tolerate plain-text body stuffed in 'text'
        txt = obj.get("text") if isinstance(obj, dict) and "text" in obj else None
        if isinstance(txt, str) and len(txt) == 9 and set(txt) <= set("-pc"):
            return txt
    if isinstance(obj, str) and len(obj) == 9 and set(obj) <= set("-pc"):
        return obj
    raise ValueError(f"Unable to extract board from response: {obj}")


def board_counts(board: str) -> Tuple[int, int]:
    return board.count("p"), board.count("c")


def current_phase(board: str) -> str:
    player_pieces, computer_pieces = board_counts(board)
    return "placement" if (player_pieces < 3 or computer_pieces < 3) else "movement"


def winner_on_board(board: str) -> Optional[str]:
    # Returns 'p', 'c', or None
    for line in WINNING_LINES:
        a, b, c = (board[i - 1] for i in line)
        if a == b == c and a in ("p", "c"):
            return a
    return None


def empty_positions(board: str) -> List[int]:
    return [i + 1 for i, ch in enumerate(board) if ch == "-"]


def player_positions(board: str, who: str) -> List[int]:
    return [i + 1 for i, ch in enumerate(board) if ch == who]


def legal_moves_from(board: str, pos: int) -> List[int]:
    return [n for n in ADJACENT_POSITIONS[pos] if board[n - 1] == "-"]


def simulate_place(board: str, pos: int, who: str) -> str:
    chars = list(board)
    chars[pos - 1] = who
    return "".join(chars)


def simulate_move(board: str, src: int, dst: int) -> str:
    chars = list(board)
    chars[dst - 1] = chars[src - 1]
    chars[src - 1] = "-"
    return "".join(chars)


def find_immediate_winning_place(board: str, who: str) -> Optional[int]:
    for pos in empty_positions(board):
        next_board = simulate_place(board, pos, who)
        if winner_on_board(next_board) == who:
            return pos
    return None


def find_immediate_winning_move(board: str, who: str) -> Optional[Tuple[int, int]]:
    for src in player_positions(board, who):
        for dst in legal_moves_from(board, src):
            next_board = simulate_move(board, src, dst)
            if winner_on_board(next_board) == who:
                return src, dst
    return None


def score_place(board: str, pos: int, who: str) -> int:
    # Basic heuristic: prefer center, then positions that increase two-in-a-row potential without blocking ourselves
    score = 0
    if pos == 5:
        score += 3
    # Count how many winning lines include pos and have only '-' or our pieces
    for line in WINNING_LINES:
        if pos in line:
            line_marks = [board[i - 1] for i in line]
            if all(ch in ("-", who) for ch in line_marks):
                # reward lines where we already have presence
                presence = sum(1 for ch in line_marks if ch == who)
                if presence == 2:
                    score += 3
                elif presence == 1:
                    score += 2
                else:
                    score += 1
    # Prefer adjacency to our pieces
    for nbr in ADJACENT_POSITIONS[pos]:
        if board[nbr - 1] == who:
            score += 1
    return score


def choose_place(board: str, who: str) -> int:
    # Win now
    win_pos = find_immediate_winning_place(board, who)
    if win_pos is not None:
        return win_pos

    # Block opponent
    opponent = "c" if who == "p" else "p"
    block_pos = find_immediate_winning_place(board, opponent)
    if block_pos is not None:
        return block_pos

    # Prefer center if available
    if board[4] == "-":  # position 5
        # Avoid placements that let opponent win immediately on their placement
        test = simulate_place(board, 5, who)
        opponent = "c" if who == "p" else "p"
        if find_immediate_winning_place(test, opponent) is None:
            return 5

    # Otherwise, pick the highest-scoring spot
    candidates = empty_positions(board)
    best_pos = max(candidates, key=lambda pos: score_place(board, pos, who))
    return best_pos


def choose_move(board: str, who: str) -> Tuple[int, int]:
    # Win now
    win_move = find_immediate_winning_move(board, who)
    if win_move is not None:
        return win_move

    opponent = "c" if who == "p" else "p"

    # Block opponent's immediate win by landing on their winning spot
    # Try any move that results in no immediate opponent win and maximizes our two-in-row potential
    candidate_moves: List[Tuple[int, int]] = []
    for src in player_positions(board, who):
        for dst in legal_moves_from(board, src):
            candidate_moves.append((src, dst))

    # First, try any move that blocks opponent's immediate winning place
    opp_win_spot = find_immediate_winning_place(board, opponent)
    if opp_win_spot is not None:
        for move in candidate_moves:
            if move[1] == opp_win_spot:
                return move

    # Prefer moving into center if open
    for move in candidate_moves:
        if move[1] == 5:
            next_board = simulate_move(board, move[0], move[1])
            if find_immediate_winning_move(next_board, opponent) is None:
                return move

    # Score remaining moves
    def score_move(m: Tuple[int, int]) -> int:
        src, dst = m
        next_board = simulate_move(board, src, dst)

        # Penalize if it gives the opponent an immediate win
        if find_immediate_winning_move(next_board, opponent) is not None:
            return -100

        score = 0
        # Reward if it creates two in a row with a chance to complete
        for line in WINNING_LINES:
            marks = [next_board[i - 1] for i in line]
            if marks.count(who) == 2 and marks.count("-") == 1:
                score += 3
        # Prefer centrality
        if dst == 5:
            score += 2
        # Prefer occupying positions that participate in many open lines
        for line in WINNING_LINES:
            if dst in line:
                line_marks = [next_board[i - 1] for i in line]
                if all(ch in ("-", who) for ch in line_marks):
                    score += 1
        return score

    best_move = max(candidate_moves, key=score_move)
    return best_move


# --------- Minimax with alpha-beta pruning ---------

def evaluate_board(board: str) -> int:
    winner = winner_on_board(board)
    if winner == "p":
        return 10_000
    if winner == "c":
        return -10_000

    score = 0

    # Center control
    if board[4] == "p":
        score += 15
    elif board[4] == "c":
        score -= 15

    # Line potentials
    for line in WINNING_LINES:
        marks = [board[i - 1] for i in line]
        p_count = marks.count("p")
        c_count = marks.count("c")
        empty = marks.count("-")
        if c_count == 0:
            # Only our pieces and empties
            if p_count == 2 and empty == 1:
                score += 50
            elif p_count == 1 and empty == 2:
                score += 10
            elif empty == 3:
                score += 3
        if p_count == 0:
            if c_count == 2 and empty == 1:
                score -= 55  # slightly more negative to prioritize blocking
            elif c_count == 1 and empty == 2:
                score -= 10
            elif empty == 3:
                score -= 3

    # Mobility (only meaningful once both have 3 pieces)
    p_count, c_count = board_counts(board)
    if p_count == 3 and c_count == 3:
        p_moves = sum(len(legal_moves_from(board, pos)) for pos in player_positions(board, "p"))
        c_moves = sum(len(legal_moves_from(board, pos)) for pos in player_positions(board, "c"))
        score += 2 * (p_moves - c_moves)

    return score


Action = Tuple[str, int, int]


def generate_actions(board: str, who: str) -> List[Action]:
    actions: List[Action] = []
    phase = current_phase(board)
    if phase == "placement":
        for pos in empty_positions(board):
            actions.append(("place", pos, 0))
    else:
        for src in player_positions(board, who):
            for dst in legal_moves_from(board, src):
                actions.append(("move", src, dst))
    return actions


def apply_action(board: str, who: str, action: Action) -> str:
    kind, a, b = action
    if kind == "place":
        return simulate_place(board, a, who)
    else:
        return simulate_move(board, a, b)


def minimax(board: str, depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
    winner = winner_on_board(board)
    if depth == 0 or winner is not None:
        return evaluate_board(board)

    who = "p" if maximizing_player else "c"
    actions = generate_actions(board, who)
    if not actions:
        return evaluate_board(board)

    if maximizing_player:
        value = -1_000_000
        for action in actions:
            child = apply_action(board, who, action)
            value = max(value, minimax(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = 1_000_000
        for action in actions:
            child = apply_action(board, who, action)
            value = min(value, minimax(child, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def choose_action_via_minimax(board: str, who: str, depth: int) -> Optional[Action]:
    actions = generate_actions(board, who)
    if not actions:
        return None

    best_action: Optional[Action] = None
    best_score = -1_000_000

    # Optional safety filter: avoid handing opponent immediate win next turn
    safe_actions: List[Action] = []
    opponent = "c" if who == "p" else "p"
    for action in actions:
        next_board = apply_action(board, who, action)
        # If opponent can win immediately after this, mark unsafe
        if current_phase(next_board) == "placement":
            if find_immediate_winning_place(next_board, opponent) is None:
                safe_actions.append(action)
        else:
            if find_immediate_winning_move(next_board, opponent) is None:
                safe_actions.append(action)
    if safe_actions:
        actions = safe_actions

    for action in actions:
        next_board = apply_action(board, who, action)
        score = minimax(next_board, depth - 1, -1_000_000, 1_000_000, who != "p")
        if score > best_score:
            best_score = score
            best_action = action
    return best_action


def detect_last_mover(prev_board: Optional[str], cur_board: str) -> Optional[str]:
    if prev_board is None or len(prev_board) != 9 or len(cur_board) != 9:
        return None
    diffs = [i for i in range(9) if prev_board[i] != cur_board[i]]
    if not diffs:
        return None
    # Placement: exactly one diff where '-' -> 'p' or 'c'
    if len(diffs) == 1:
        i = diffs[0]
        if prev_board[i] == '-' and cur_board[i] in ('p', 'c'):
            return cur_board[i]
        return None
    # Movement: two diffs, one piece moved to '-' and one '-' to that piece
    if len(diffs) == 2:
        i, j = diffs
        a_prev, a_cur = prev_board[i], cur_board[i]
        b_prev, b_cur = prev_board[j], cur_board[j]
        # try mapping from source to dest
        pairs = [
            (a_prev, a_cur, b_prev, b_cur),
            (b_prev, b_cur, a_prev, a_cur),
        ]
        for src_prev, src_cur, dst_prev, dst_cur in pairs:
            if src_cur == '-' and dst_prev == '-' and src_prev in ('p', 'c') and dst_cur == src_prev:
                return src_prev
    return None


def play_one_game(api: RotaAPI, depth: int = 3) -> Optional[str]:
    previous_board: Optional[str] = None
    stagnation_counter = 0
    last_seen_board: Optional[str] = None
    starting_player: Optional[str] = None  # 'p' or 'c' during placement

    for step in range(800):  # increased safety cap
        # Fetch latest board
        try:
            status_obj = api.status()
            # Handle explicit server failures (e.g., sign-in required) without crashing
            if isinstance(status_obj, dict) and status_obj.get("status") == "fail":
                data = status_obj.get("data")
                print("Status fail:", status_obj)
                if isinstance(data, dict) and data.get("request") == "Sign in is required":
                    print("Resetting session due to sign-in required...")
                    try:
                        api.reset()
                    except Exception as e2:
                        print("Reset error:", repr(e2))
                    time.sleep(0.8)
                    continue
                time.sleep(0.5)
                continue
            if isinstance(status_obj, dict) and status_obj.get("status_code") == 400:
                # Likely invalid request or temporary server hiccup; back off and retry next loop
                print("Status 400:", (status_obj.get("text") or "").strip()[:120])
                time.sleep(0.5)
                continue

            board = extract_board(status_obj)
            print("\nStep", step)
            print_board(board)
            if board == last_seen_board:
                stagnation_counter += 1
            else:
                stagnation_counter = 0
            last_seen_board = board
        except Exception as e:
            print("Status fetch error:", repr(e))
            time.sleep(0.8)
            continue

        win = winner_on_board(board)
        if win is not None:
            print(f"Winner detected: {win}")
            return win

        phase = current_phase(board)

        # Infer starting player during placement if unknown
        if starting_player is None and phase == "placement":
            p_count, c_count = board_counts(board)
            if p_count == c_count + 1:
                starting_player = "p"
                print("Inferred starting player: p")
            elif c_count == p_count + 1:
                starting_player = "c"
                print("Inferred starting player: c")

        acted = False
        if phase == "placement":
            p_count, c_count = board_counts(board)
            # Determine our turn robustly
            if starting_player is not None:
                total_moves = p_count + c_count
                to_move = starting_player if (total_moves % 2 == 0) else ("c" if starting_player == "p" else "p")
                our_turn = (to_move == "p")
            else:
                # Fallback: if opponent has one extra piece, it's our turn; if we have one extra, it's not
                if c_count == p_count + 1:
                    our_turn = True
                elif p_count == c_count + 1:
                    our_turn = False
                else:
                    # Equal counts and unknown starter; if we just saw opponent place (via last_mover) then it's our turn
                    last_mover = detect_last_mover(previous_board, board)
                    our_turn = (last_mover == 'c') or (p_count == 0 and c_count == 0)
            if not our_turn:
                print("Not our turn (placement)")
            if our_turn:
                action = choose_action_via_minimax(board, "p", depth) or ("place", choose_place(board, "p"), 0)
                kind, a, b = action
                if kind == "place":
                    result = api.place(str(a))
                else:
                    # Guard against no-op moves
                    if a == b or board[a-1] != 'p' or board[b-1] != '-':
                        result = {"text": "noop"}
                    else:
                        result = api.move(str(a), str(b))
                # Handle invalid move responses gracefully
                if isinstance(result, dict) and result.get("status_code") == 400:
                    print("Placement rejected (400):", (result.get("text") or "").strip()[:120])
                else:
                    try:
                        board = extract_board(result)
                        print("Our action:", kind, a, b)
                        print("Board after our action:")
                        print_board(board)
                        acted = True
                    except Exception as e:
                        print("After placement parse error:", repr(e))
        else:  # movement
            last_mover = detect_last_mover(previous_board, board)
            # It's our turn if computer moved last; if unknown, try cautiously
            our_turn = last_mover == 'c'
            if not our_turn:
                print("Not our turn (movement)")
            if our_turn:
                action = choose_action_via_minimax(board, "p", depth) or ("move",) + choose_move(board, "p")
                kind, a, b = action
                if kind == "place":
                    result = api.place(str(a))
                else:
                    if a == b or board[a-1] != 'p' or board[b-1] != '-':
                        result = {"text": "noop"}
                    else:
                        result = api.move(str(a), str(b))
                if isinstance(result, dict) and result.get("status_code") == 400:
                    print("Move rejected (400):", (result.get("text") or "").strip()[:120])
                else:
                    try:
                        board = extract_board(result)
                        print("Our action:", kind, a, b)
                        print("Board after our action:")
                        print_board(board)
                        acted = True
                    except Exception as e:
                        print("After move parse error:", repr(e))

        # Detect stagnation: no change for many polls but we think it's our turn
        if stagnation_counter > 50 and not acted:
            # Try to break deadlock by polling slower and skipping a turn
            time.sleep(1.5)
            stagnation_counter = 0

        previous_board = board
        time.sleep(0.3)
        continue

    # Final status
    try:
        final = api.status()
        final_board = extract_board(final)
        print_board(final_board)
        win = winner_on_board(final_board)
    except Exception as e:
        print("Final status error:", repr(e))
        win = None
    if win == "p":
        print("Player (p) wins!")
    elif win == "c":
        print("Computer (c) wins.")
    else:
        print("No winner detected.")
    return win


def main(email: str, depth: int = 3, games: int = 1) -> None:
    print(email)
    api = RotaAPI(email)
    p_wins = 0
    c_wins = 0
    draws = 0
    for i in range(games):
        print(f"\n=== Game {i+1}/{games} ===")
        try:
            api.reset()
        except Exception as e:
            print("Reset error:", repr(e))
        result = play_one_game(api, depth)
        if result == 'p':
            p_wins += 1
        elif result == 'c':
            c_wins += 1
        else:
            draws += 1
        time.sleep(1.0)
    print(f"\nSummary over {games} games: Player wins={p_wins}, Computer wins={c_wins}, Draws={draws}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python play_rota.py <email> [depth] [games]")
        sys.exit(1)
    depth = int(sys.argv[2]) if len(sys.argv) >= 3 else 3
    games = int(sys.argv[3]) if len(sys.argv) >= 4 else 1
    main(sys.argv[1], depth, games)


