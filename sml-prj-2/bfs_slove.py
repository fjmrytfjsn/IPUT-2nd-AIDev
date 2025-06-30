def bfs_solve(maze, start, goal, size):
    start = start
    goal = goal
    queue = [(start, [start])]
    visited = set([start])

    while queue:
        current_pos, path = queue.pop(0)

        if current_pos == goal:
            return path

        y, x = current_pos
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (y + dy, x + dx)
            ny, nx = next_pos
            if 0 <= ny < size and 0 <= nx < size:
                if maze[ny][nx] == 0 and next_pos not in visited:
                    queue.append((next_pos, path + [next_pos]))
                    visited.add(next_pos)
                elif maze[ny][nx] == 3:
                    return path + [next_pos]

    return None
