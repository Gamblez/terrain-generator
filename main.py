import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from noise import pnoise2

def generate_terrain(width, depth, height_scale, resolution):
    terrain = np.zeros((width, depth))
    for x in range(width):
        for z in range(depth):
            # Adjust these parameters to change the noise characteristics
            y = pnoise2(x / resolution, z / resolution, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0)
            terrain[x][z] = y * height_scale
    return terrain

def draw_terrain(terrain):
    glBegin(GL_QUADS)
    for x in range(terrain.shape[0] - 1):
        for z in range(terrain.shape[1] - 1):
            # Simplified drawing logic for each tile as a quad
            # Set color based on height
            glColor3f(0, max(min(terrain[x][z] / 20 + 0.5, 1), 0), 0)
            glVertex3f(x, terrain[x][z], z)
            glVertex3f(x + 1, terrain[x + 1][z], z)
            glVertex3f(x + 1, terrain[x + 1][z + 1], z + 1)
            glVertex3f(x, terrain[x][z + 1], z + 1)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(-20, -30, -40)
    glRotatef(10, 2, 1, 0)

    # Generate terrain
    terrain = generate_terrain(40, 40, 10, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_terrain(terrain)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
