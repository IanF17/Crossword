import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for grid and window
GRID_SIZE = 5
CELL_SIZE = 50
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
WINDOW_WIDTH = GRID_WIDTH + 400  # Adjusted for more clue space
WINDOW_HEIGHT = GRID_HEIGHT + 70

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)  # Color for hovered square
SELECTED_COLOR = (173, 216, 230)  # Color for selected square (light blue)
CONGRATULATIONS_COLOR = (15, 128, 38)  # Color for the congratulations message (green)
BLACKED_OUT_COLOR = (50, 50, 50)  # Color for blacked-out squares

# Define answer keys and clues for puzzles
puzzles = [
    {
        'answers': [
            ['', '', 'M', 'T', 'V'],
            ['', 'T', 'O', 'R', 'E'],
            ['D', 'I', 'N', 'A', 'R'],
            ['I', 'N', 'E', 'P', 'T'],
            ['M', 'A', 'T', 'S', '']
        ],
        'across_clues': {
            1: "Music television channel known for reality shows",
            4: "Ripped it up",
            5: "Currency of Algeria, Serbia, and Jordan",
            6: "Unskillful",
            7: "These can be of type: welcome or yoga"
        },
        'down_clues': {
            1: "French Impressionist painter Claude",
            2: "Devices for catching animals or people",
            3: "Suffix with 'co' or 'in'",
            4: "____ Turner or Fey",
            5: "Not too bright"
        },
        'blacked_out': [(0, 0), (0, 1), (1, 0), (4, 4)],
        'numbered_cells': [(0, 2, 1), (0, 3, 2), (0, 4, 3), (1, 1, 4), (2, 0, 5), (3, 0, 6), (4, 0, 7)]
    },
    {
        'answers': [
            ['', '', 'B', 'A', 'G'],
            ['', 'B', 'A', 'M', 'A'],
            ['F', 'I', 'N', 'A', 'L'],
            ['A', 'L', 'A', 'S', ''],
            ['M', 'E', 'L', 'S', '']
        ],
        'across_clues': {
            1: "Container often made of plastic, cloth, or paper",
            4: "University of Alabama, informally",
            5: "Ultimate; End",
            6: "Expression of concern",
            7: "Famous Californian 'Drive In' diner"
        },
        'down_clues': {
            1: "Boring; Ordinary",
            2: "To accumulate or collect",
            3: "Girl, informally",
            4: "Digestive fluid from the liver",
            5: "Close friends or relatives, in slang"
        },
        'blacked_out': [(0, 0), (0, 1), (1, 0), (3, 4), (4, 4)],
        'numbered_cells': [(0, 2, 1), (0, 3, 2), (0, 4, 3), (1, 1, 4), (2, 0, 5), (3, 0, 6), (4, 0, 7)]
    },
    {
        'answers': [
            ['', 'D', 'R', 'E', ''],
            ['P', 'R', 'O', 'V', 'E'],
            ['H', 'O', 'M', 'E', 'R'],
            ['A', 'V', 'A', 'N', 'T'],
            ['T', 'E', 'N', 'T', '']
        ],
        'across_clues': {
            1: "Record producer that Eminem says people ''Forgot about''",
            4: "To demonstrate through evidence or argument",
            6: "Simpson who wrote the Odyssey?",
            7: "_____-garde",
            8: "A camper's home"
        },
        'down_clues': {
            1: "Operated a vehicle",
            2: "The culture of Julius Caesar",
            3: "Occurrence or happening",
            4: "Highly attractive or hot, in slang",
            5: "Suffix with 'exp' or 'al'"
        },
        'blacked_out': [(0, 0), (0, 4), (4, 4)],
        'numbered_cells': [(0, 1, 1), (0, 2, 2), (0, 3, 3), (1, 0, 4), (1, 4, 5), (2, 0, 6), (3, 0, 7), (4, 0, 8)]
    }
]


# Initialize grid data
def initialize_grid():
    return [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


grid = initialize_grid()

# Pygame display setup
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Crossword Game")

# Font setup
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 16)  # Smaller font for cell numbers

# Variables to track selected cell
selected_row = None
selected_col = None

# Track current puzzle index
current_puzzle = 0


# Function to check if the current grid matches the answer key
def check_puzzle_complete(grid, answer_key):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != answer_key[row][col]:
                return False
    return True


# Function to wrap text
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    return lines


# Function to draw the grid
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (row, col) in puzzles[current_puzzle]['blacked_out']:
                pygame.draw.rect(screen, BLACKED_OUT_COLOR, cell_rect)
            else:
                if selected_row == row and selected_col == col:
                    pygame.draw.rect(screen, SELECTED_COLOR, cell_rect)
                elif selected_row is None and cell_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, LIGHT_GRAY, cell_rect)
                else:
                    pygame.draw.rect(screen, GRAY, cell_rect, 1)
                letter_surface = font.render(grid[row][col], True, BLACK)
                screen.blit(letter_surface, (col * CELL_SIZE + 20, row * CELL_SIZE + 20))

    # Draw numbers in the top left corner of specific cells
    for row, col, num in puzzles[current_puzzle]['numbered_cells']:
        num_surface = small_font.render(str(num), True, BLACK)
        screen.blit(num_surface, (col * CELL_SIZE + 2, row * CELL_SIZE + 2))


# Main game loop
running = True
puzzle_completed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not puzzle_completed:
                # Get grid coordinates based on mouse position
                x, y = pygame.mouse.get_pos()
                grid_col = x // CELL_SIZE
                grid_row = y // CELL_SIZE
                if 0 <= grid_col < GRID_SIZE and 0 <= grid_row < GRID_SIZE and (grid_row, grid_col) not in \
                        puzzles[current_puzzle]['blacked_out']:
                    selected_row, selected_col = grid_row, grid_col
                else:
                    selected_row, selected_col = None, None
        elif event.type == pygame.KEYDOWN:
            if not puzzle_completed and selected_row is not None and selected_col is not None:
                if event.key == pygame.K_BACKSPACE:
                    grid[selected_row][selected_col] = ''
                elif event.unicode.isalpha():
                    grid[selected_row][selected_col] = event.unicode.upper()
                    if check_puzzle_complete(grid, puzzles[current_puzzle]['answers']):
                        current_puzzle += 1
                        if current_puzzle < len(puzzles):
                            grid = initialize_grid()
                            selected_row, selected_col = None, None
                        else:
                            puzzle_completed = True

    # Clear screen
    screen.fill(WHITE)

    if puzzle_completed:
        # Display congratulations message
        congrats_message_line1 = "Congratulations! You completed all puzzles! Thanks for playing!"
        congrats_message_line2 = "-IF"
        text_surface_line1 = font.render(congrats_message_line1, True, CONGRATULATIONS_COLOR)
        text_surface_line2 = font.render(congrats_message_line2, True, CONGRATULATIONS_COLOR)
        screen.blit(text_surface_line1, (WINDOW_WIDTH // 2 - text_surface_line1.get_width() // 2, WINDOW_HEIGHT // 2))
        screen.blit(text_surface_line2, ((WINDOW_WIDTH // 2 - text_surface_line2.get_width() // 2) + 70, WINDOW_HEIGHT // 2 + 40))

    else:
        # Draw grid
        draw_grid()

        # Draw clues header
        across_header = "Across Clues"
        down_header = "Down Clues"
        across_header_surface = font.render(across_header, True, BLACK)
        down_header_surface = font.render(down_header, True, BLACK)
        screen.blit(across_header_surface, (GRID_WIDTH + 20, 0))
        screen.blit(down_header_surface, (GRID_WIDTH + 220, 0))

        # Draw clues (across)
        current_across_clues = puzzles[current_puzzle]['across_clues']
        across_y = across_header_surface.get_height()
        for number, clue in current_across_clues.items():
            wrapped_clue = wrap_text(f"{number}. {clue}", font, 180)
            for line in wrapped_clue:
                text_surface = font.render(line, True, BLACK)
                screen.blit(text_surface, (GRID_WIDTH + 20, across_y * 1.8))
                across_y += text_surface.get_height()

        # Draw clues (down)
        current_down_clues = puzzles[current_puzzle]['down_clues']
        down_y = down_header_surface.get_height()
        for number, clue in current_down_clues.items():
            wrapped_clue = wrap_text(f"{number}. {clue}", font, 180)
            for line in wrapped_clue:
                text_surface = font.render(line, True, BLACK)
                screen.blit(text_surface, (GRID_WIDTH + 220, down_y * 1.8))
                down_y += text_surface.get_height()

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
