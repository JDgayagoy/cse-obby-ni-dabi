# crosshair.py

from OpenGL.GL import *
from OpenGL.GLU import *

def draw_crosshair(screen_width, screen_height, size=10, line_width=2.0, color=(1.0, 1.0, 1.0)):
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Switch to orthographic projection for 2D drawing
    glUseProgram(0)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, screen_width, screen_height, 0)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glColor3f(*color)
    glLineWidth(line_width)

    glBegin(GL_LINES)
    # Horizontal line
    glVertex2f(center_x - size, center_y)
    glVertex2f(center_x + size, center_y)
    # Vertical line
    glVertex2f(center_x, center_y - size)
    glVertex2f(center_x, center_y + size)
    glEnd()

    # Restore previous states
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
