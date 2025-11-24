import math
import pygame

try:
    from OpenGL import GL
except Exception:
    GL = None


class OpenGLPresenter:
    """
    Aplica um pós-processamento simples: joga a Surface 2D em um quad e adiciona
    uma vinheta suave + leve brilho central. Uso opcional, fallback para Pygame.
    """

    def __init__(self, width: int, height: int):
        if GL is None:
            raise ImportError("PyOpenGL não encontrado. Instale com 'pip install PyOpenGL'.")
        self.width = width
        self.height = height
        self.texture_id = GL.glGenTextures(1)
        self.texture_initialized = False
        self._setup_gl_state()
        self._update_viewport(width, height)

    def _setup_gl_state(self):
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glClearColor(0.04, 0.08, 0.07, 1.0)

    def _update_viewport(self, width: int, height: int):
        self.width = width
        self.height = height
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, width, height, 0, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def present_surface(self, surface: pygame.Surface, vignette_strength: float = 0.20):
        w, h = surface.get_size()
        if w != self.width or h != self.height:
            self._update_viewport(w, h)
            self.texture_initialized = False

        pixels = pygame.image.tostring(surface, "RGBA", False)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
        if not self.texture_initialized:
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, w, h, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, pixels)
            self.texture_initialized = True
        else:
            GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, 0, 0, w, h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, pixels)

        GL.glBegin(GL.GL_QUADS)
        GL.glColor4f(1.0, 1.0, 1.0, 1.0)
        # Coordenadas ajustadas para evitar inversão vertical
        GL.glTexCoord2f(0.0, 0.0); GL.glVertex2f(0.0, 0.0)
        GL.glTexCoord2f(1.0, 0.0); GL.glVertex2f(float(w), 0.0)
        GL.glTexCoord2f(1.0, 1.0); GL.glVertex2f(float(w), float(h))
        GL.glTexCoord2f(0.0, 1.0); GL.glVertex2f(0.0, float(h))
        GL.glEnd()

        self._draw_center_glow()
        self._draw_vignette_overlay(vignette_strength)
        GL.glColor4f(1.0, 1.0, 1.0, 1.0)

    def _draw_center_glow(self):
        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_TRIANGLE_FAN)
        GL.glColor4f(0.12, 0.35, 0.20, 0.18)
        GL.glVertex2f(self.width * 0.5, self.height * 0.5)
        GL.glColor4f(0.05, 0.12, 0.09, 0.0)
        steps = 32
        radius = min(self.width, self.height) * 0.60
        for i in range(steps + 1):
            ang = (i / steps) * math.tau
            GL.glVertex2f(self.width * 0.5 + math.cos(ang) * radius,
                          self.height * 0.5 + math.sin(ang) * radius)
        GL.glEnd()
        GL.glEnable(GL.GL_TEXTURE_2D)

    def _draw_vignette_overlay(self, strength: float):
        if strength <= 0:
            return
        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_TRIANGLE_FAN)
        GL.glColor4f(0.0, 0.0, 0.0, 0.0)
        GL.glVertex2f(self.width * 0.5, self.height * 0.5)
        GL.glColor4f(0.0, 0.0, 0.0, max(0.0, strength * 0.6))  # sombra mais leve
        steps = 48
        rx = self.width * 0.82
        ry = self.height * 0.82
        for i in range(steps + 1):
            ang = (i / steps) * math.tau
            GL.glVertex2f(self.width * 0.5 + math.cos(ang) * rx,
                          self.height * 0.5 + math.sin(ang) * ry)
        GL.glEnd()
        GL.glEnable(GL.GL_TEXTURE_2D)
