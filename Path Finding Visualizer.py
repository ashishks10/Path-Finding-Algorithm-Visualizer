import pygame
import pygwidgets
import math
from queue import PriorityQueue, Queue
import time

WIDTH = 750
WINDOW = pygame.display.set_mode((1250,WIDTH))
pygame.display.set_caption("Path Finding Visualizer")

startButton = pygwidgets.TextButton(WINDOW, (800, 675), 'Start Path Finding', width=150, height=50, fontSize=24)
clearPathButton = pygwidgets.TextButton(WINDOW, (820, 565), 'Clear PATH', height=35, fontSize=22)
resetButton = pygwidgets.TextButton(WINDOW, (820, 620), 'RESET', height=35, fontSize=22)
Algo1 = pygwidgets.TextRadioButton(WINDOW, (800, 80), 'Algos','A* Algorithm',value = True)
Algo2 = pygwidgets.TextRadioButton(WINDOW, (800, 120), 'Algos','Greedy Best-First Search',value = False)
Algo3 = pygwidgets.TextRadioButton(WINDOW, (800, 160), 'Algos','Breadth First Search',value = False)
Algo4 = pygwidgets.TextRadioButton(WINDOW, (800, 200), 'Algos','Depth First Search',value = False)
Algo5 = pygwidgets.TextRadioButton(WINDOW, (800, 240), 'Algos','Dijkstra\'s Algorithm',value = False)
Text1 = pygwidgets.DisplayText(WINDOW, (760, 30), value='  ALGORITHM TO BE USED :', fontName=None, fontSize=24, backgroundColor=None)
Text2= pygwidgets.DisplayText(WINDOW, (760, 300), value=' SPEED :', fontName=None, fontSize=24, backgroundColor=None)
Text3= pygwidgets.DisplayText(WINDOW, (760, 515), value='Current Node :', fontName=None, fontSize=22, backgroundColor=None)
Text4= pygwidgets.DisplayText(WINDOW, (900, 515), value='', fontName=None,fontSize=24)
Text5= pygwidgets.DisplayText(WINDOW, (1010, 20), value='INSTRUCTIONS:', fontName='TimesRoman', fontSize=26, backgroundColor=None)
Text6= pygwidgets.DisplayText(WINDOW, (1010, 80), value='Use the left-mouse button to draw \nthe start node, the end node and \nbarriers.\n\nOn clicking left-mouse button over \nan empty node:\n - If start node is not present on \n   screen, then start node will be \n   created.\n - Else if end node is not present ,\n   then end node will be created.\n - Else barrier will be created.\n\nUse the right-mouse button to erase \nthe nodes (the start node, the end \nnode and barriers).\n', fontName=None, fontSize=20,width=230, height=250, backgroundColor=None)
Text7= pygwidgets.DisplayText(WINDOW, (1010, 360), value='NODES :', fontName='TimesRoman', fontSize=26, backgroundColor=None)
Text8= pygwidgets.DisplayText(WINDOW, (1070, 404), value=': UNVISITED NODE', fontName='TimesRoman', fontSize=18)
Text9= pygwidgets.DisplayText(WINDOW, (1070, 454), value=': START NODE', fontName='TimesRoman', fontSize=18)
Text10= pygwidgets.DisplayText(WINDOW, (1070, 504), value=': END NODE', fontName='TimesRoman', fontSize=18)
Text11= pygwidgets.DisplayText(WINDOW, (1070, 554), value=': BARRIER/ WALL', fontName='TimesRoman', fontSize=18)
Text12= pygwidgets.DisplayText(WINDOW, (1070, 604), value=': PATH NODE', fontName='TimesRoman', fontSize=18)
Text13= pygwidgets.DisplayText(WINDOW, (1070, 654), value=': VISITED NODE\n\n:', fontName='TimesRoman', fontSize=18)
Text14= pygwidgets.DisplayText(WINDOW, (1070, 700), value='   UNVISITED NEIGHBOUR\n   OF VISITED NODE', fontName='TimesRoman', fontSize=14)
Speed1 = pygwidgets.TextRadioButton(WINDOW, (800, 340), 'Speed','Fast',value = True, nickname = '0.0')
Speed2 = pygwidgets.TextRadioButton(WINDOW, (800, 380), 'Speed','Medium',value = False,nickname = '0.05')
Speed3 = pygwidgets.TextRadioButton(WINDOW, (800, 420), 'Speed','Slow',value = False,nickname = '0.1')
Speed4 = pygwidgets.TextRadioButton(WINDOW, (800, 460), 'Speed','Very Slow',value = False,nickname = '0.2')


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_barrier(self):
		return self.color == BLACK

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = CYAN

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = ORANGE

	def make_end(self):
		self.color = RED

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def add_neighbors(self, grid):
		self.neighbors = []
		
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col - 1])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.col])



	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1.get_pos()
	x2, y2 = p2.get_pos()
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, time_delay):
	count = 0
	while current in came_from:
		time.sleep(time_delay)
		current = came_from[current]
		count += 1
		current.make_path()
		draw()
	print("The length of the path is " + str(count))

def A_star_algorithm(draw, grid, start, end, time_delay):
	count = 0
	pq = PriorityQueue()
	pq.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start, end)
	visited = {}

	while not pq.empty():
		time.sleep(time_delay)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		current = pq.get()[2]
		if current in visited:
			continue
		visited[current]=1;
		Text4.setValue(str(current.get_pos()[0]+1)+', '+ str(current.get_pos()[1]+1))

		if current == end:
			reconstruct_path(came_from, end, draw, time_delay)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			if temp_g_score < g_score[neighbor]: 
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor, end)
				came_from[neighbor] = current
				if neighbor not in visited:
					count -= 1
					pq.put((f_score[neighbor], count, neighbor))
					neighbor.make_open()
		draw()

		if current != start:
			current.make_closed()

	print("Cannot find path!")
	return False


def greedy_Best_First_Search_algorithm(draw, grid, start, end, time_delay):
	count = 0
	pq = PriorityQueue()
	pq.put((0, count, start))
	came_from = {}
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start, end)
	visited = {}

	while not pq.empty():
		time.sleep(time_delay)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = pq.get()[2]
		if current in visited:
			continue;
		visited[current]=1
		Text4.setValue(str(current.get_pos()[0]+1)+', '+ str(current.get_pos()[1]+1))

		if current == end:
			reconstruct_path(came_from, end, draw, time_delay)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_f_score = h(neighbor, end)

			if temp_f_score < f_score[neighbor]: 
				f_score[neighbor] = h(neighbor, end)
				came_from[neighbor] = current
				if neighbor not in visited:
					count += 1
					pq.put((f_score[neighbor], count, neighbor))
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	print("Cannot find path!")
	return False



def Dijkstras_algorithm(draw, grid, start, end, time_delay):
	count = 0
	pq = PriorityQueue()
	pq.put((0, count, start))
	came_from = {}
	distance = {spot: float("inf") for row in grid for spot in row}
	distance[start] = 0
	visited = {start}

	open_set_hash = {start}
	
	while not pq.empty():
		time.sleep(time_delay)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = pq.get()[2]
		open_set_hash.remove(current)
		Text4.setValue(str(current.get_pos()[0]+1)+', '+ str(current.get_pos()[1]+1))

		if current == end:
			reconstruct_path(came_from, end, draw, time_delay)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_distance = distance[current] + 1
			if temp_distance < distance[neighbor]:
				count+=1
				if neighbor in open_set_hash:
					count = pq.get()[1]
					pq.remove((distance[neighbor], count, neighbor))
				open_set_hash.add(neighbor)
				distance[neighbor] = temp_distance	
				came_from[neighbor] = current
				pq.put((distance[neighbor], count, neighbor))
				neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	print("Cannot find path!")
	return False



def BFS_algorithm(draw, grid, start, end, time_delay):
	queue = Queue()
	queue.put(start)
	came_from = {}
	added = {start}

	while not queue.empty():
		time.sleep(time_delay)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = queue.get()
		Text4.setValue(str(current.get_pos()[0]+1)+', '+ str(current.get_pos()[1]+1))

		if current == end:
			reconstruct_path(came_from, end, draw, time_delay)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			if neighbor not in added:
				came_from[neighbor] = current
				queue.put(neighbor)
				added.add(neighbor)
				neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	print("Cannot find path!")
	return False



def DFS_algorithm(draw, grid, start, end, time_delay):
	stack = []
	stack.append(start)
	came_from = {}
	visited = {start}

	while (len(stack)>0):
		time.sleep(time_delay)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = stack[-1]
		stack.pop()
		Text4.setValue(str(current.get_pos()[0]+1)+', '+ str(current.get_pos()[1]+1))

		if current == end:
			reconstruct_path(came_from, end, draw, time_delay)
			start.make_start()
			end.make_end()
			return True

		visited.add(current)
		for neighbor in current.neighbors:
			if neighbor not in visited:
				stack.append(neighbor)
				came_from[neighbor] = current

		draw()

		if current != start:
			current.make_closed()

	print("Cannot find path!")
	return False




def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) 	# HORIZONTAL LINES
		pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))		# VERTICAL LINES
	pygame.draw.line(win, GREY, (50 * gap, 0), (50 * gap, width))

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.draw.line(win, GREY, (1000, 0), (1000, width))
	pygame.draw.line(win, GREY, (750, 0), (1250,0))
	pygame.draw.rect(win, (211,211,211), pygame.Rect(880, 508, 100, 30))

	startButton.draw()
	clearPathButton.draw()
	resetButton.draw()
	Algo1.draw()
	Algo2.draw()
	Algo3.draw()
	Algo4.draw()
	Algo5.draw()
	Speed1.draw()
	Speed2.draw()
	Speed3.draw()
	Speed4.draw()
	Text1.draw()
	Text2.draw()
	Text3.draw()
	Text4.draw()
	Text5.draw()
	Text6.draw()
	Text7.draw()
	Text8.draw()
	Text9.draw()
	Text10.draw()
	Text11.draw()
	Text12.draw()
	Text13.draw()
	Text14.draw()
	pygame.draw.rect(win, BLACK, pygame.Rect(1020, 400, 30, 30),2)
	pygame.draw.rect(win, ORANGE, pygame.Rect(1020, 450, 30, 30))
	pygame.draw.rect(win, RED, pygame.Rect(1020, 500, 30, 30))
	pygame.draw.rect(win, BLACK, pygame.Rect(1020, 550, 30, 30))
	pygame.draw.rect(win, PURPLE, pygame.Rect(1020, 600, 30, 30))
	pygame.draw.rect(win, CYAN, pygame.Rect(1020, 650, 30, 30))
	pygame.draw.rect(win, GREEN, pygame.Rect(1020, 700, 30, 30))
	pygame.display.update()

def get_clicked_pos(pos, rows, width):			
	gap = width // rows
	y, x = pos 									

	row = y // gap
	col = x // gap 
	return row, col

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	started = False

	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if(event.type) == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: 						# If Left Mouse Button is pressed
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				if row <50 and col< 50:								# If position of mouse if within the Grid
					spot = grid[row][col]
					if not start:
						start = spot
						start.make_start()
					elif not end and spot != start:
						end = spot
						end.make_end()

					elif spot != end and spot != start:
						spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]:						# If Right Mouse Button is pressed
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				if row <50 and col< 50:								# If position of mouse if within the Grid
					spot = grid[row][col]
					spot.reset()
					if spot == start:
						start = None
					elif spot == end:
						end = None


			if startButton.handleEvent(event):						# If Start Path Finding Button is Pressed

				if started == True or start == None or end == None:
					if started == True:						# If path already visible on screen
						print('Clear Path or RESET!')
					elif start == None:						# If Start position is not set
						print('Start Node not Found!')
					elif end == None:						# If End position is not set
						print('End Node not Found!')
					continue

				time_delay = float(Speed1.getSelectedRadioButton())		# Set value of time delay for Speed


				for row in grid:
					for spot in row:
						spot.add_neighbors(grid)

				if Algo1.getValue() == True:							# A* Algorithm
					A_star_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, time_delay)
				elif Algo2.getValue() == True:							# Greedy Best-First Search
					greedy_Best_First_Search_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, time_delay)
				elif Algo3.getValue() == True:							# Breadth First Search
					BFS_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, time_delay)
				elif Algo4.getValue() == True:							# Depth First Search
					DFS_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, time_delay)
				elif Algo5.getValue() == True:							# Dijkstra's Algorithm
					Dijkstras_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, time_delay)

				started = True


			if clearPathButton.handleEvent(event):					# If Clear PATH Button is pressed
				started = False
				Text4.setValue('')
				for row in grid:
					for spot in row:
						if spot!= start and spot != end and spot.is_barrier() !=True:
							spot.reset()

			if resetButton.handleEvent(event):					# If RESET Button is pressed
				start = None
				end = None
				started = False
				Text4.setValue('')
				for row in grid:
					for spot in row:
						spot.reset()


			if Algo1.handleEvent(event):
				pass
			if Algo2.handleEvent(event):
				pass
			if Algo3.handleEvent(event):
				pass
			if Algo4.handleEvent(event):
				pass
			if Algo5.handleEvent(event):
				pass
			if Speed1.handleEvent(event):
				time_delay
			if Speed2.handleEvent(event):
				pass
			if Speed3.handleEvent(event):
				pass
			if Speed4.handleEvent(event):
				pass
			

	pygame.quit()

main(WINDOW, WIDTH)
