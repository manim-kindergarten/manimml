class Mobject:
    pass


class Scene:
    def add(self, obj):
        print(f'Scene.add({obj})')


class Point:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.z = 1


class Object3D:
    def __init__(self):
        self.position = Point()

    def add(self, obj):
        print(f'Object3D.add({obj})')


class Mesh:
    def __init__(self, geometry, material):
        print(f'Mesh({geometry}, {material})')

    def scale(self, x, y, z):
        print(f'Mesh.scale({x}, {y}, {z})')


class PointLight:
    def __init__(self, color, strength):
        print(f'PointLight({color}, {strength})')
