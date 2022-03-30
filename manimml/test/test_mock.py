from manimml import ManimML, Mobject, Scene

class SphereGeometry(Mobject):
    def __init__(self, n):
        self.n = n


class MeshPhongMaterial:
    def __init__(self, *args, **kw):
        self.emissive = kw.get('emissive', None)
        self.color = kw.get('color', None)


data = {
  'geometry': {
    'sphere': SphereGeometry(1),
  },
  'material': {
    'sun': MeshPhongMaterial(emissive=0xffcc44),
    'earth': MeshPhongMaterial(
      color=0x2233ff,
      emissive=0x112244
    ),
    'moon': MeshPhongMaterial(
      color=0x888888,
      emissive=0x222222
    )
  }
}

app = ManimML(file='test_mock.xml', data=data, scene=Scene())
print(app.objs)
print(app.ids)
print(app.classes)
