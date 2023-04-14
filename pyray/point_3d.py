from __future__ import annotations
import random
import glm


def dot(vec1: tuple, vec2: tuple) -> float:
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2])


def add(vec1, vec2) -> tuple:
    return (vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2])


def sub(vec1, vec2) -> tuple:
    return (vec1[0] - vec2[0], vec1[1] - vec2[1], vec1[2] - vec2[2])


def mul(vec1, vec2) -> tuple:
    if isinstance(vec2, tuple):
        return (vec1[0] * vec2[0], vec1[1] * vec2[1], vec1[2] * vec2[2])

    return (vec1[0] * vec2, vec1[1] * vec2, vec1[2] * vec2)


def normalize(vec):
    factor = 1 / glm.sqrt(dot(vec, vec))
    return (vec[0] * factor, vec[1] * factor, vec[2] * factor)


def negate(vec):
    return (vec[0] * -1, vec[1] * -1, vec[2] * -1)


def reflect_vector(i: glm.vec3, n: glm.vec3, roughness: float):
    # Calculate the reflection vector without roughness
    # i - (n * (2 * i.dot(n)))
    reflection_vector = glm.reflect(i, n)

    # Add random roughness
    roughness_vector = glm.vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
    roughness_vector = glm.normalize(roughness_vector)
    reflection_vector += roughness_vector * roughness
    return reflection_vector
