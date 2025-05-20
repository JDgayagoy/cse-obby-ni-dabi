import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import glm
import time


from config import setup_opengl
from shader import create_shader, VERTEX_SHADER, FRAGMENT_SHADER
from square import create_cube
from crosshair import draw_crosshair
from walls import get_walls, get_wall_models, get_obstacles, get_obstacle_models, aabb_collision_with_body

is_sprinting = False
pygame.mixer.init()
pygame.font.init()
jump_sound = pygame.mixer.Sound("C:/Users/David/Downloads/cube/391670__jeckkech__jump.wav")
winner_sound = pygame.mixer.Sound("winner.wav")
font = pygame.font.SysFont('Arial', 48)

def render_text(text, position, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    # Set up OpenGL 2D mode
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glRasterPos2f(position[0], position[1])
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_win_popup():
    # Draw a semi-transparent black box in the center
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.0, 0.0, 0.0, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(200, 250)
    glVertex2f(600, 250)
    glVertex2f(600, 350)
    glVertex2f(200, 350)
    glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    # Render "You Win!" text
    render_text("You Win!", (800 // 2 - 100, 600 // 2 - 24), font, color=(255, 255, 0))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def load_texture(path):
    surface = pygame.image.load(path)
    image = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_id

pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Obby Game")

setup_opengl()
glClearColor(72/255, 72/255, 72/255, 1.0)  # Set background to white (RGBA)
shader = create_shader(VERTEX_SHADER, FRAGMENT_SHADER)
vao, index_count = create_cube()
wall_texture = load_texture("wall.png")

clock = pygame.time.Clock()

camera_pos = glm.vec3(-6.0, 0, -2.0)
camera_front = glm.vec3(0.0, 0.0, -1.0)
camera_up = glm.vec3(0.0, 1.0, 0.0)
move_speed = 3
sprint_speed = 5
yaw = -90.0
pitch = 0.0
sensitivity = 0.1
player_half_size = glm.vec3(0.25, 0.85, 0.25)
trial_count = 0


pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
center_x = screen.get_width() // 2
center_y = screen.get_height() // 2
pygame.mouse.set_pos(center_x, center_y)

projection = glm.perspective(glm.radians(45.0), 800 / 600, 0.1, 100.0)
last_time = time.time()

walls = get_walls()
wall_models = get_wall_models()
obstacles = get_obstacles()
obstacle_models = get_obstacle_models()

gravity = -9.81
vertical_velocity = 0.0
on_ground = False
jump_strength = 5.0
won_game = False
win_time = None
running = True

pygame.mouse.set_visible(True)
pygame.event.set_grab(False)

def show_start_menu():
    showing_menu = True
    while showing_menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if 300 <= x <= 500 and 250 <= y <= 310:
                    showing_menu = False  # Start game

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw background
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw button rectangle
        glColor4f(0.2, 0.2, 0.2, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(300, 250)
        glVertex2f(500, 250)
        glVertex2f(500, 310)
        glVertex2f(300, 310)
        glEnd()

        title_text = "OBBY NI DABI"
        title_surface = font.render(title_text, True, (255, 255, 255))
        title_width, title_height = title_surface.get_size()
        title_x = (800 - title_width) // 2  # Horizontally center
        title_y = 520  # Adjust this for how high you want it

        render_text(title_text, (title_x, title_y), font, color=(255, 255, 255))

        render_text("PLAY", (355, 260), font, color=(255, 255, 255))

        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()
        pygame.time.wait(10)

show_start_menu()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while running:
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    x_offset = (mouse_x - center_x) * sensitivity
    y_offset = (center_y - mouse_y) * sensitivity

    yaw += x_offset
    pitch += y_offset
    pitch = max(-89.0, min(89.0, pitch))

    front = glm.vec3()
    front.x = glm.cos(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    front.y = glm.sin(glm.radians(pitch))
    front.z = glm.sin(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    camera_front = glm.normalize(front)

    pygame.mouse.set_pos(center_x, center_y)

    new_pos = glm.vec3(camera_pos)
    keys = pygame.key.get_pressed()

    horizontal_move = glm.vec3(0.0)
    if keys[pygame.K_w]:
        horizontal_move += glm.normalize(glm.vec3(camera_front.x, 0, camera_front.z))
    if keys[pygame.K_s]:
        horizontal_move -= glm.normalize(glm.vec3(camera_front.x, 0, camera_front.z))
    if keys[pygame.K_a]:
        right = glm.normalize(glm.cross(camera_front, camera_up))
        horizontal_move -= glm.vec3(right.x, 0, right.z)
    if keys[pygame.K_d]:
        right = glm.normalize(glm.cross(camera_front, camera_up))
        horizontal_move += glm.vec3(right.x, 0, right.z)

    if glm.length(horizontal_move) > 0:
        horizontal_move = glm.normalize(horizontal_move)

    # Only allow sprint toggle when on ground
    if on_ground and keys[pygame.K_LSHIFT]:
        is_sprinting = True
    elif on_ground and not keys[pygame.K_LSHIFT]:
        is_sprinting = False

    current_speed = sprint_speed if is_sprinting else move_speed

    new_pos += horizontal_move * current_speed * delta_time

    if keys[pygame.K_SPACE] and on_ground:
        vertical_velocity = jump_strength
        on_ground = False
        jump_sound.play()  # <-- play jump sound

    vertical_velocity += gravity * delta_time
    new_pos.y += vertical_velocity * delta_time

    colliding = False
    collided_on_y = False
    for center, half_size in walls + obstacles:
        if aabb_collision_with_body(new_pos, player_half_size, center, half_size):
            colliding = True
            test_y = glm.vec3(camera_pos.x, new_pos.y, camera_pos.z)
            if aabb_collision_with_body(test_y, player_half_size, center, half_size):
                vertical_velocity = 0.0
                new_pos.y = camera_pos.y
                collided_on_y = True
            else:
                new_pos.x = camera_pos.x
                new_pos.z = camera_pos.z
            break

    if not colliding or collided_on_y:
        camera_pos = new_pos

    on_ground = vertical_velocity == 0.0 and camera_pos.y <= new_pos.y + 0.01

    # Restart if player falls
    if camera_pos.y < -10:
        camera_pos = glm.vec3(-6.0, 0, -2.0)
        trial_count += 1
        vertical_velocity = 0.0
        print("You fell! Restarting...")

    goal_pos = glm.vec3(78.0, 3.5, -22.5)
    goal_half = glm.vec3(0.7, 1.0, 0.7)

    if not won_game and aabb_collision_with_body(camera_pos, player_half_size, goal_pos, goal_half):
        print("You reached the goal!")
        won_game = True
        win_time = time.time()

    # Show "Congrats" message if won
    if won_game:
        winner_sound.play()
        draw_win_popup()
        print("win")
        if time.time() - win_time > 2:
            camera_pos = glm.vec3(-6.0, 0.0, -2.0)
            trial_count = 1
            vertical_velocity = 0.0
            won_game = False
            win_time = None
            print("Restarting game...")


    view = glm.lookAt(camera_pos, camera_pos + camera_front, camera_up)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader)

    glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
    glUniform1i(glGetUniformLocation(shader, "wallTexture"), 0)

    glBindVertexArray(vao)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, wall_texture)

    for model_matrix in wall_models + obstacle_models:
        glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, glm.value_ptr(model_matrix))
        glDrawElements(GL_TRIANGLES, index_count, GL_UNSIGNED_INT, None)

    glBindVertexArray(0)
    draw_crosshair(800, 600, size=8, line_width=1.5, color=(1.0, 1.0, 1.0))
    render_text(f"Tries: {trial_count}", (20, 540), font, color=(255, 255, 255))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
