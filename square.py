import numpy as np
from OpenGL.GL import *

def create_cube():
    # Vertex data: [x, y, z, u, v]
    vertices = np.array([
        # Back face
        -0.5, -0.5, -0.5, 0.0, 0.0,
         0.5, -0.5, -0.5, 1.0, 0.0,
         0.5,  0.5, -0.5, 1.0, 1.0,
        -0.5,  0.5, -0.5, 0.0, 1.0,
        # Front face
        -0.5, -0.5,  0.5, 0.0, 0.0,
         0.5, -0.5,  0.5, 1.0, 0.0,
         0.5,  0.5,  0.5, 1.0, 1.0,
        -0.5,  0.5,  0.5, 0.0, 1.0,
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2, 2, 3, 0,  # back
        4, 5, 6, 6, 7, 4,  # front
        0, 4, 7, 7, 3, 0,  # left
        1, 5, 6, 6, 2, 1,  # right
        3, 2, 6, 6, 7, 3,  # top
        0, 1, 5, 5, 4, 0   # bottom
    ], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    stride = 5 * 4  # 5 floats per vertex, 4 bytes each

    # Position attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

    # Texture coordinate attribute
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))

    glBindVertexArray(0)
    return vao, len(indices)
