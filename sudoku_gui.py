import tkinter as tk
from sudoku import Problem, Solver

class GUI(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		
		# App title
		self.title("Sudoku Solver")

		# Window size
		self.geometry("500x500")

		# Build widgets
		self.init_buttons()
		self.init_sudoku_board()
		self.init_message_display()

	def init_buttons(self):
		# Frame
		self.button_frame_solver = tk.Frame(self)
		self.button_frame_options = tk.Frame(self)
		self.button_frame_options.pack(side="bottom", padx=10, pady=10)
		self.button_frame_solver.pack(side="bottom", padx=10, pady=10)

		# Buttons
		self.cancel = tk.Button(self.button_frame_options, text="Close", command=self.quit)
		self.reset = tk.Button(self.button_frame_options, text="Reset", command=self.reset_board)
		self.solve_dfs = tk.Button(self.button_frame_solver, text="DFS", command=lambda: self.solve_board('DFS'))
		self.solve_bestfs = tk.Button(self.button_frame_solver, text="Best First", command=lambda: self.solve_board('BestFS'))

		self.solve_dfs.grid(column=0, row=1)
		self.solve_bestfs.grid(column=1, row=1)
		self.reset.grid(column=0, row=1)
		self.cancel.grid(column=1, row=1)

	def init_sudoku_board(self):
		# Frame
		self.board_frame = tk.Frame(self)
		self.board_frame.pack(side="top", padx=30, pady=20)

		# Build cell entries
		self.cells = {}
		for row in range(9):
			for col in range(9):
				self.cells[str(row)+str(col)] = tk.Entry(self.board_frame, width=4)

		# Place cell entries into grid
		for row in range(9):
			for col in range(9):
				address = str(row)+str(col)

				# Row padding
				if (row+1)%3 == 0:
					pady=(0,4)
				else:
					pady=0

				# Column padding
				if (col+1)%3 == 0:
					padx=(0,4)
				else:
					padx=0

				# Place cell into grid
				self.cells[address].grid(row=row, column=col, padx=padx, pady=pady)

	def init_message_display(self):
		# Frame
		self.message_frame = tk.Frame(self)
		self.message_frame.pack(side="bottom", padx=10, pady=10)

		# Label
		self.message_label = tk.Label(self.message_frame)
		self.message_label.grid(column=1, row=2)

	def get_board(self):
				# Build array from user input
		board = []
		for row in range(9):

			# Build one row at a time
			new_row = []
			for col in range(9):

				# Ensure user input is correct during retrieval
				# TODO: ensure integers 1-9
				address = str(row)+str(col)
				try:
					if self.cells[address].get() != '':
						new_row.append(int(self.cells[address].get()))
					else:
						new_row.append(int(0))
				except ValueError:
					self.notifyUser("Non-number found in cell.")
					return None

			# Append row to board
			board.append(new_row)
		return board

	def solve_board(self, algorithm):
		# Retrieve user input
		board = self.get_board()
		if board==None:
			return

		# Solve board
		method = 'blind' if algorithm == 'DFS' else 'heuristic'
		problem = Problem(board, method)
		solver = Solver(problem, algorithm)
		solution = solver.solve()
		# Display result
		for row in range(9):
			for col in range(9):
				address = str(row)+str(col)
				self.cells[address].delete(0, 'end')
				self.cells[address].insert(0, solution[row][col])

		# Display solved message
		message = "Elapsed time = {} seconds\nVisited nodes = {}".format(solver.elapsed_time, solver.visited_nodes)
		self.message_label.config(text=message)

	def reset_board(self):
		# Empty entire grid
		for row in range(9):
			for col in range(9):
				address = str(row)+str(col)
				self.cells[address].delete(0, 'end')

		# Set cursor to (0,0) cell
		self.cells[str(0)+str(0)].icursor(0)

		# Empty display message
		self.message_label.config(text="")

# Open UI
app = GUI()
app.mainloop()