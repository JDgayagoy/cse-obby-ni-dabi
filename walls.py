# walls.py

import glm

# Define wall bounding boxes as (center, half_size)
def get_walls():
    return [
        (glm.vec3(-6.0, -1.5, -2), glm.vec3(2.0, 0.05, 5.0)),   # floor

    ]

def get_wall_models():
    models = []

    # Floor (rotated wall)
    floor = glm.translate(glm.mat4(1.0), glm.vec3(-6.0, -1.5, -2))
    floor = glm.rotate(floor, glm.radians(90.0), glm.vec3(1, 0, 0))  # Rotate to lay flat
    floor = glm.scale(floor, glm.vec3(2.0, 2.0, 0.1))  # Thin Z axis after rotation
    models.append(floor)


    return models

def aabb_collision_with_body(pos, body_half_size, box_center, box_half_size):
    return (
        abs(pos.x - box_center.x) <= (body_half_size.x + box_half_size.x) and
        abs(pos.y - box_center.y) <= (body_half_size.y + box_half_size.y) and
        abs(pos.z - box_center.z) <= (body_half_size.z + box_half_size.z)
    )

def get_obstacles():
    return [
        # Stage 1: Wider spaced large platforms
        (glm.vec3(0.0, -1.0, -2.0), glm.vec3(1.0, 0.1, 1.0)),
        (glm.vec3(5.0, -1.0, -2.0), glm.vec3(1.0, 0.1, 1.0)),
        (glm.vec3(11.0, -1.0, -2.0), glm.vec3(1.0, 0.1, 1.0)),

        # Stage 2: Thin beams - horizontal with wider gaps
        (glm.vec3(17.0, -0.8, -2.0), glm.vec3(0.25, 0.1, 1.5)),
        (glm.vec3(21.5, -0.5, -2.5), glm.vec3(0.25, 0.1, 1.5)),
        (glm.vec3(26.0, -0.2, -3.0), glm.vec3(0.25, 0.1, 1.5)),

        # Stage 3: Thin beams - vertical (Z-axis narrow) with gaps
        (glm.vec3(31.0, 0.0, -4.0), glm.vec3(1.5, 0.1, 0.25)),
        (glm.vec3(35.5, 0.3, -5.0), glm.vec3(1.5, 0.1, 0.25)),
        (glm.vec3(40.0, 0.6, -6.0), glm.vec3(1.5, 0.1, 0.25)),

        # Stage 4: Raised narrow paths (more spaced)
        (glm.vec3(45.0, 1.0, -7.5), glm.vec3(0.3, 0.1, 1.0)),
        (glm.vec3(49.5, 1.3, -9.0), glm.vec3(0.3, 0.1, 1.0)),
        (glm.vec3(54.5, 1.6, -10.5), glm.vec3(0.3, 0.1, 1.0)),

        # Stage 5: Diagonal thin stepping blocks with wider spacing
        (glm.vec3(59.0, 2.0, -12.0), glm.vec3(0.25, 0.1, 0.25)),
        (glm.vec3(61.5, 2.3, -13.2), glm.vec3(0.25, 0.1, 0.25)),
        (glm.vec3(64.0, 2.6, -14.6), glm.vec3(0.25, 0.1, 0.25)),
        (glm.vec3(66.5, 2.9, -16.0), glm.vec3(0.25, 0.1, 0.25)),

        # Final pads before goal with very wide spacing
        (glm.vec3(69.5, 3.1, -17.2), glm.vec3(0.2, 0.1, 0.2)),
        (glm.vec3(72.5, 3.3, -18.8), glm.vec3(0.2, 0.1, 0.2)),
        (glm.vec3(75.5, 3.5, -20.5), glm.vec3(0.2, 0.1, 0.2)),

        # Goal platform
        (glm.vec3(78.0, 3.5, -22.5), glm.vec3(0.5, 0.5, 0.5)),
    ]



def get_obstacle_models():
    models = []
    for center, half_size in get_obstacles():
        model = glm.mat4(1.0)

        # Translate to position
        model = glm.translate(model, center)

        # Rotate the platform so it lays flat like the floor
        model = glm.rotate(model, glm.radians(90.0), glm.vec3(1, 0, 0))

        # Apply scale after rotation to prevent stretching vertically
        model = glm.scale(model, glm.vec3(half_size.x * 2.0, half_size.z * 2.0, half_size.y * 2.0))

        models.append(model)
    return models

