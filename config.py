from OpenGL.GL import *

def setup_opengl():
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
