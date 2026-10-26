import pygame as pg
import math
import pygame.gfxdraw as gfx

WIDTH = 1280
HEIGHT = 720
SPAWN_INTERVAL = 0.3  # Sekunteja uusien kolmioiden välillä.
HUE_STEP = 12.0  # Sävyn muutos asteina per kolmio; 360 astetta on koko värikierros.
COLOR_CYCLES_PER_ORBIT = 1  # Sateenkaaren kierroksia yhtä spiraalin kierrosta kohti.


class Circler(pg.sprite.Sprite):
    def __init__(self, center, hue=0.0):
        super().__init__()
        self.start_hue = hue % 360
        self.color = pg.Color(255, 255, 255)
        self.color.hsva = (self.start_hue, 100, 100, 100)
        self.size = 1.0  # Kolmion keskipisteen etäisyys kärkeen.
        self.max_size = 50.0
        self.size_speed = 6.0  # Kolmion koon kasvu pikseleinä sekunnissa.
        self.rotation = 0.0  # Kolmion oma kiertokulma asteina.
        self.rotation_speed = 60.0  # Positiivinen nopeus pyörittää vastapäivään.
        self.original_image = self.create_image()
        self.draw_image()
        self.rect = self.image.get_rect(center=center)
        self.center = center
        self.radius = 0.0
        self.angle = 0.0
        self.angular_speed = 2.0  # Radiaania sekunnissa.
        self.growth_speed = 20.0  # Säteen kasvu pikseleinä sekunnissa.

    def create_image(self):
        # Tehdään valkoinen peruskuva kerran; se voidaan sävyttää millä tahansa värillä.
        draw_scale = 8
        large_image = pg.Surface((128 * draw_scale, 128 * draw_scale), pg.SRCALPHA)
        cx, cy = large_image.get_rect().center
        size = self.max_size * draw_scale
        half_width = math.sqrt(3) * size / 2
        # Tasasivuisen kolmion kärjet: yläkärki, vasen ja oikea alakärki.
        gfx.filled_trigon(
            large_image,
            cx, round(cy - size),
            round(cx - half_width), round(cy + size / 2),
            round(cx + half_width), round(cy + size / 2),
            (255, 255, 255, 255),
        )
        return pg.transform.smoothscale(large_image, (128, 128))

    def draw_image(self):
        # Skaalataan ja kierretään samaa peruskuvaa yhdellä operaatiolla.
        scale = self.size / self.max_size
        self.image = pg.transform.rotozoom(self.original_image, self.rotation, scale)
        # Sävytys säilyttää läpinäkyvyyden eikä muuta alkuperäistä peruskuvaa.
        self.image.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)

    def update(self, dt, screen_rect):
        if self.size < self.max_size:
            self.size = min(self.max_size, self.size + self.size_speed * dt)
        self.rotation = (self.rotation + self.rotation_speed * dt) % 360
        self.angle += self.angular_speed * dt
        self.radius += self.growth_speed * dt
        hue = (self.start_hue + math.degrees(self.angle) * COLOR_CYCLES_PER_ORBIT) % 360
        self.color.hsva = (hue, 100, 100, 100)
        self.draw_image()

        # Lasketaan sijainti aina saman keskipisteen ympäriltä.
        position = (
            round(self.center[0] + math.cos(self.angle) * self.radius),
            round(self.center[1] + math.sin(self.angle) * self.radius),
        )
        # Kierretyn kuvan mitat voivat muuttua; säilytetään oikea keskipiste.
        self.rect = self.image.get_rect(center=position)

        if not screen_rect.colliderect(self.rect):
            self.kill()  # Poistaa kolmion kaikista sprite-ryhmistä.


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
    clock = pg.time.Clock()
    spawn_timer = 0.0
    hue = 0.0
    all_triangles = pg.sprite.Group(Circler(screen.get_rect().center, hue))
    running = True

    while running:
        dt = clock.tick(60) / 1000  # Edellisestä ruudusta kuluneet sekunnit.
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                running = False

        all_triangles.update(dt, screen.get_rect())
        screen.fill((0, 0, 0))
        all_triangles.draw(screen)
        pg.display.flip()
        spawn_timer += dt
        if spawn_timer >= SPAWN_INTERVAL:
            spawn_timer %= SPAWN_INTERVAL  # Pitkän tauon jälkeen ei luoda ruuhkaa.
            hue = (hue + HUE_STEP) % 360
            all_triangles.add(Circler(screen.get_rect().center, hue))
    pg.quit()


if __name__ == "__main__":
    main()
