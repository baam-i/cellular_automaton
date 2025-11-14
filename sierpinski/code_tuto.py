import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chaos Game - Sierpinski Triangle')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define vertices of the triangle
vertices = [
    (WIDTH // 2, 50),
    (50, HEIGHT - 50),
    (WIDTH - 50, HEIGHT - 50)
]

# Function to draw the vertices
def draw_vertices():
    for vertex in vertices:
        pygame.draw.circle(window, WHITE, vertex, 3)

# Function to perform the Chaos Game
def chaos_game(iterations, point):
    for _ in range(iterations):
        chosen_vertex = random.choice(vertices)
        point = (
            (point[0] + chosen_vertex[0]) // 2,
            (point[1] + chosen_vertex[1]) // 2
        )
        pygame.draw.circle(window, WHITE, point, 1)
        pygame.display.update()

def main():
    # Initial point (randomly chosen inside the triangle)
    point = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        window.fill(BLACK)
        draw_vertices()
        chaos_game(10000, point)  # Perform 10000 iterations for each frame
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()