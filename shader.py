from OpenGL.GL import *

VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texcoord;

out vec2 TexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    TexCoord = texcoord;
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D wallTexture;

void main() {
    FragColor = texture(wallTexture, TexCoord);
}
"""

def create_shader(vertex_src, fragment_src):
    shader_program = glCreateProgram()
    vertex = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex, vertex_src)
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(vertex).decode())

    glShaderSource(fragment, fragment_src)
    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(fragment).decode())

    glAttachShader(shader_program, vertex)
    glAttachShader(shader_program, fragment)
    glLinkProgram(shader_program)
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(shader_program).decode())

    glDeleteShader(vertex)
    glDeleteShader(fragment)
    return shader_program
