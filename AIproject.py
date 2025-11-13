class PostalRobot:
    def __init__(self):
        self.N = 17  # number of nodes
        self.graph = {
            0: [(2, 9), (1, 13)],  # H1
            1: [(0, 13), (2, 8), (5, 3), (6, 6), (7, 5), (8, 4), (9, 1), (4, 4), (3, 5)],  # H2
            2: [(0, 9), (1, 8), (13, 10), (14, 10), (15, 10), (16, 5)],  # H3
            3: [(1, 5)],   # 1001
            4: [(1, 4)],   # 1002
            5: [(1, 3)],   # 1003
            6: [(1, 6)],   # 1004
            7: [(1, 5), (8, 1)],   # 1005
            8: [(1, 4), (7, 1), (9, 3)],   # 1006
            9: [(1, 1), (8, 3), (10, 2)],  # 1007
            10: [(9, 2), (2, 5)],  # 1008
            11: [(10, 3), (12, 3)],  # 1009
            12: [(11, 3), (13, 2)],  # 1010
            13: [(12, 2), (14, 2), (2, 10)],  # 1011
            14: [(13, 2), (15, 4), (2, 10)],  # 1012
            15: [(14, 4), (16, 2), (2, 10)],  # 1013
            16: [(15, 2), (2, 5)]   # 1014
        }

        self.weights = {
            (0, 2): 8, (2, 0): 8,
            (0, 1): 12, (1, 0): 12,
            (1, 5): 2, (5, 1): 2,
            (10, 2): 4, (2, 10): 4,
            (11, 10): 1, (10, 11): 1,
            (1, 6): 5, (6, 1): 5,
            (1, 2): 7, (2, 1): 7,
            (1, 7): 4, (7, 1): 4,
            (1, 8): 3, (8, 1): 3,
            (8, 7): 0, (7, 8): 0,
            (8, 9): 2, (9, 8): 2,
            (1, 9): 0, (9, 1): 0,
            (1, 4): 3, (4, 1): 3,
            (1, 3): 4, (3, 1): 4,
            (11, 12): 2, (12, 11): 2,
            (12, 13): 2, (13, 12): 2,
            (13, 14): 1, (14, 13): 1,
            (14, 15): 3, (15, 14): 3,
            (15, 16): 1, (16, 15): 1,
            (2, 13): 9, (13, 2): 9,
            (2, 14): 9, (14, 2): 9,
            (2, 15): 9, (15, 2): 9,
            (2, 16): 4, (16, 2): 4,
        }

        self.building_names = {
            0: "H1", 1: "H2", 2: "H3", 3: "1001", 4: "1002", 5: "1003", 6: "1004",
            7: "1005", 8: "1006", 9: "1007", 10: "1008", 11: "1009", 12: "1010",
            13: "1011", 14: "1012", 15: "1013", 16: "1014"
        }

        self.graph_bfs_dfs = self.load_graph_from_file("map_data.txt")

        print("\n<-- Welcome to the Qassim University Unaizah building -->\n")
        self.print_building_list()

        print("\nChoose the algorithm:")
        print("1 : BFS")
        print("2 : DFS")
        print("3 : A*")
        print("0 : Exit")

        choice = int(input("\nChoice: "))
        if choice == 0:
            exit()

        start = int(input("\nEnter the current building number (0-16): "))
        goal = int(input("Enter the destination building number (0-16): "))
        print(f"From {self.ret_building(start)} to {self.ret_building(goal)}")

        if choice == 1:
            self.BFS(start, goal)
        elif choice == 2:
            self.DFS(start, goal)
        elif choice == 3:
            self.A_star(start, goal)
        else:
            print("Invalid choice!")
            self.__init__()

    def load_graph_from_file(self, filename):
        graph = {i: [] for i in range(self.N)}
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    a, b = parts
                    a_idx = self.get_index(a)
                    b_idx = self.get_index(b)
                    graph[a_idx].append(b_idx)
                    graph[b_idx].append(a_idx)
        return graph

    def get_index(self, name):
        for idx, val in self.building_names.items():
            if val == name:
                return idx
        return int(name)  # fallback for numeric-only names like 1001

    def ret_building(self, idx):
        return self.building_names.get(idx, str(idx))

    def print_building_list(self):
        print("Building list:")
        for i in range(self.N):
            print(f"{i}: {self.ret_building(i)}")

    def BFS(self, start, goal):
        from collections import deque
        visited = [False] * self.N
        prev = [None] * self.N
        queue = deque([start])
        visited[start] = True
        visited_nodes = []

        while queue:
            current = queue.popleft()
            visited_nodes.append(current)
            if current == goal:
                break
            for neighbor in self.graph_bfs_dfs.get(current, []):
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    prev[neighbor] = current

        self.print_path(prev, start, goal)
        print("Visited nodes:", ' -> '.join(self.ret_building(n) for n in visited_nodes))

    def DFS(self, start, goal):
        visited = [False] * self.N
        prev = [None] * self.N
        visited_nodes = []

        def dfs(current):
            visited[current] = True
            visited_nodes.append(current)
            if current == goal:
                return True
            for neighbor in self.graph_bfs_dfs.get(current, []):
                if not visited[neighbor]:
                    prev[neighbor] = current
                    if dfs(neighbor):
                        return True
            return False

        dfs(start)
        self.print_path(prev, start, goal)
        print("Visited nodes:", ' -> '.join(self.ret_building(n) for n in visited_nodes))

    def A_star(self, start, goal):
        import heapq

        def heuristic(a, b):
            return abs(a - b) * 2

        open_set = [(0, start)]
        came_from = {}
        g_score = {node: float('inf') for node in range(self.N)}
        g_score[start] = 0

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                break

            for neighbor, cost in self.graph.get(current, []):
                tentative_g_score = g_score[current] + cost
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

        path = []
        current = goal
        total_distance = 0
        while current in came_from:
            path.append(current)
            prev = came_from[current]
            total_distance += self.weights.get((prev, current), 1)
            current = prev
        path.append(start)
        path.reverse()

        print("\nPath:")
        for i in range(len(path)):
            name = self.ret_building(path[i])
            print(name, end="")
            if i != len(path) - 1:
                dist = self.weights.get((path[i], path[i + 1]), 1)
                print(f" --[{dist}m]--> ", end="")
        print(f"\n\nTotal distance: {total_distance} meters")

    def print_path(self, prev, start, goal):
        path = []
        at = goal
        while at is not None:
            path.append(at)
            at = prev[at]
        path.reverse()

        if path[0] == start:
            print("\nPath:")
            for i in range(len(path)):
                name = self.ret_building(path[i])
                print(name, end="")
                if i != len(path) - 1:
                    print(" --> ", end="")
            print()
        else:
            print("No path found.")

PostalRobot()
