from PIL import ImageDraw

CENTER_BOTH  = (True,  True)
CENTER_HORIZ = (True,  False)
CENTER_VERT  = (False, True)
CENTER_NONE  = (False, False)

class TheoriaDraw(ImageDraw.ImageDraw):
  def __init__(self, image):
    self._im = image
    ImageDraw.ImageDraw.__init__(self, image)

  def ctext(self, pos, text, **kwargs):
    (x, y) = pos
    (ch, cv) = kwargs.pop('center')

    if ch:
      x -= self.textsize(text, font=kwargs.get('font'))[0] / 2
    if cv:
      y -= self.textsize(text, font=kwargs.get('font'))[1] / 2

    return self.text((x, y), text, **kwargs)

  def cpaste(self, image, pos, **kwargs):
    (x, y) = pos
    mask = kwargs.get('mask', image)
    (ch, cv) = kwargs.pop('center')

    if ch:
      x -= image.size[0] / 2
    if cv:
      y -= image.size[1] / 2

    self._im.paste(image, (x, y), mask)

