import copy
import time
import heapq
import operator

# 9x9 Sudoku
class Problem:
	def __init__(self, initial, method):
		self.initial = initial
		self.method = method # blind or heuristic
		self.type = 9 # 9x9 grid

	def goal_test(self, state):
		# Validate each row
		for row in range(self.type):
			# Remove zeros
			row_arr = list(filter(lambda a: a != 0, state[row]))

			# Ensure unique value
			if (len(row_arr) < self.type) or len(row_arr) != len(set(row_arr)):
				return False

		# Validate each col
		for col in range(self.type):
			# Build col array
			col_arr = []
			for row in range(self.type):
				col_arr.append(state[row][col])
			# Remove zeros
			col_arr = list(filter(lambda a: a != 0, col_arr))

			# Ensure unique values
			if (len(col_arr) < self.type) or len(col_arr) != len(set(col_arr)):
				return False

		# Validate each quadrant
		for quad in range(self.type):
			quad_arr = self.get_quad(state, quad)

			# Remove zeros
			quad_arr = list(filter(lambda a: a != 0, quad_arr))

			# Ensure unique values
			if (len(quad_arr) < self.type) or len(quad_arr) != len(set(quad_arr)):
				return False

		# Everything checks out
		return True

	def get_quad(self, state, quad_index):
		quad_map = {
			0:[[0,1,2],[0,1,2]],
			1:[[0,1,2],[3,4,5]],
			2:[[0,1,2],[6,7,8]],
			3:[[3,4,5],[0,1,2]],
			4:[[3,4,5],[3,4,5]],
			5:[[3,4,5],[6,7,8]],
			6:[[6,7,8],[0,1,2]],
			7:[[6,7,8],[3,4,5]],
			8:[[6,7,8],[6,7,8]]
		}

		quad_arr = []

		for row in range(self.type):
			for col in range(self.type):
				if row in quad_map[quad_index][0] and col in quad_map[quad_index][1]:
					quad_arr.append(state[row][col])


		return quad_arr

	def get_quad_index(self, state, row, col):
		quad_index_map = {
			((0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)): 0,
			((0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)): 1,
			((0,6), (0,7), (0,8), (1,6), (1,7), (1,8), (2,6), (2,7), (2,8)): 2,
			((3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)): 3,
			((3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5)): 4,
			((3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8)): 5,
			((6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)): 6,
			((6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5)): 7,
			((6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)): 8,
		}
		for keys, ind in quad_index_map.items():
			if (row, col) in keys:
				return ind
	
	def get_col(self, state, col):
		col_arr = []
		for row in range(self.type):
			col_arr.append(state[row][col])
		return col_arr

	# Return set of valid numbers from values that do not appear in used
	def filter_values(self, values, used):
		return [number for number in values if number not in used]

	def get_spot(self, state):
		if self.method == 'blind':
			return self.get_spot_blind(state)
		elif self.method == 'heuristic':
			return self.get_spot_heuristic(state)

	# Return first empty spot on grid (marked with 0)
	def get_spot_blind(self, state):
		for row in range(self.type):
			for col in range(self.type):
				if state[row][col] == 0:
					return {
						"row": row,
						"col": col
					}

	# Return first empty empty spot with minimum remaining values
	def get_spot_heuristic(self, state):
		mrv_vals = {}
		for row in range(self.type):
			for col in range(self.type):
				if state[row][col] == 0:
					# calculate row, col and quad mrv for current empty spot
					row_mrv = len(list(filter(lambda a: a == 0, state[row])))
					col_mrv = len(list(filter(lambda a: a == 0, self.get_col(state, col))))
					quad = self.get_quad_index(state, row, col)
					quad_mrv = len(list(filter(lambda a: a == 0, self.get_quad(state, quad))))
					# get minimum remaining value
					mrv = min(row_mrv, col_mrv, quad_mrv)
					mrv_vals[(row, col)] = mrv
		row, col = sorted(mrv_vals, key=mrv_vals.get)[0]
		return {
			"row": row,
			"col": col,
			"h": mrv_vals[(row, col)]
		}

	# Filter valid values based on row
	def filter_row(self, state, row):
		number_set = range(1, self.type+1) # Defines set of valid numbers that can be placed on board
		in_row = [number for number in state[row] if (number != 0)]
		options = self.filter_values(number_set, in_row)
		return options

	# Filter valid values based on col
	def filter_col(self, options, state, col):
		in_col = [] # List of valid values in spot's col
		for col_index in range(self.type):
			if state[col_index][col] != 0:
				in_col.append(state[col_index][col])
		options = self.filter_values(options, in_col)
		return options

	# Filter valid values based on quadrant
	def filter_quad(self, options, state, row, col):
		quad = self.get_quad_index(state, row, col)
		in_quad = self.get_quad(state, quad) # List of valid values in spot's quadrant
		in_quad = list(filter(lambda a: a != 0, in_quad))
		options = self.filter_values(options, in_quad)
		return options

	def actions(self, state):
		spot = self.get_spot(state) # Get first empty spot on board
		row, col = spot["row"], spot["col"]
		heuristic = spot.get("h") if spot.get("h") else 9
		# Remove spot's invalid options
		options = self.filter_row(state, row)
		options = self.filter_col(options, state, col)
		options = self.filter_quad(options, state, row, col)

		# Yield a state for each valid option
		for number in options:
			new_state = copy.deepcopy(state)
			new_state[row][col] = number
			yield {"state": new_state, "h": heuristic}

# Node in states space 
class Node:
	def __init__(self, state, h=9):
		self.state = state
		self.h = h 

	def expand(self, problem):
		# Return list of valid states
		return [Node(state["state"], state["h"]) for state in problem.actions(self.state)]

	def __lt__(self, other):
		return self.h < other.h

# Solver class using DFS or BestFS
class Solver:
	def __init__(self, problem, solver):
		self.problem = problem
		self.solver = solver # DFS or BestFS
		self.visited_nodes = 0
		self.elapsed_time = 0

	def DFS(self):
		self.visited_nodes = 0
		start = Node(self.problem.initial)
		if self.problem.goal_test(start.state):
			return start.state

		stack = []
		stack.append(start) # Place initial node onto the stack
		while stack:
			node = stack.pop()
			self.visited_nodes += 1
			if self.problem.goal_test(node.state):
				return node.state
			stack.extend(node.expand(self.problem)) # Add viable states onto the stack

		return None

	def BestFS(self):
		self.visited_nodes = 0
		start = Node(self.problem.initial)
		if self.problem.goal_test(start.state):
			return start.state

		heap = []
		heapq.heappush(heap, start)
		while heap:
			node = heapq.heappop(heap)
			self.visited_nodes += 1
			
			if self.problem.goal_test(node.state):
				return node.state
			for new_node in node.expand(self.problem):
				heapq.heappush(heap, new_node)

		return None

	def solve(self):
		if self.solver == "DFS":
			start_time = time.time()
			solution = self.DFS()
			end_time = time.time()
		else:
			start_time = time.time()
			solution = self.BestFS()
			end_time = time.time()
		self.elapsed_time = end_time - start_time
		return solution
