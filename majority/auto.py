import pygame

class automaton:
    WIDTH = 100
    HEIGHT = 50
    LIVE = 1
    DEAD = 0

    def __init__(self, pattern: str="23/3"):
        self.reset()
        self.__alive = [int(v) for v in pattern.split("/")[0]]
        self.__born = [int(v) for v in pattern.split("/")[1]]
        self.__iterations = 0

    @property
    def iterations(self) -> int:
        return self.__iterations

    @property
    def livecells(self) -> int:
        return self.__world.count(1)

    def reset(self) -> None:
        self.__iterations = 0
        self.__world = [0] * (self.WIDTH * self.HEIGHT)
        self.__next = [0] * (self.WIDTH * self.HEIGHT)

        # 3 puntos iniciales (dos puntos juntos y uno un poco separado)
        mid = self.WIDTH // 2
        self.write(mid, 0, 1)
        self.write(mid+1, 0, 1)
        self.write(mid-4, 0, 1)

    def read(self, x:int, y:int) -> int:
        if x >= self.WIDTH: x -= self.WIDTH
        elif x < 0: x += self.WIDTH
        if y >= self.HEIGHT: y -= self.HEIGHT
        elif y < 0: y += self.HEIGHT
        return self.__world[(y * self.WIDTH) + x]

    def write(self, x:int, y:int, value:int) -> None:
        if x >= self.WIDTH: x -= self.WIDTH
        elif x < 0: x += self.WIDTH
        if y >= self.HEIGHT: y -= self.HEIGHT
        elif y < 0: y += self.HEIGHT
        self.__world[(y * self.WIDTH) + x] = value

    def update(self) -> None:
        self.__iterations += 1

        # recorremos de abajo hacia arriba
        for y in range(self.HEIGHT - 1, 0, -1):
            for x in range(self.WIDTH):
                left   = self.read(x - 1, y - 1)
                center = self.read(x,     y - 1)
                right  = self.read(x + 1, y - 1)

                # como es regla de mayoria, tiene que haber minimo 2 celulas vivas de las 3 que estamos tomando en cuenta
                suma = left + center + right

                # regla: mayoria
                if suma == 2:
                    self.__next[(y * self.WIDTH) + x] = 1
                else:
                    self.__next[(y * self.WIDTH) + x] = 0

        # mantener la primera fila igual (inicio)
        for x in range(self.WIDTH):
            self.__next[x] = self.__world[x]

        # copiar al mundo, o sea, la matriz
        for i in range(self.WIDTH * self.HEIGHT):
            self.__world[i] = self.__next[i]



    def draw(self, context:pygame.Surface) -> None:
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                current = self.read(x,y)
                if current == self.LIVE:
                    pygame.draw.rect(context, (255,255,255), (x*10, y*10, 10, 10))
                else:
                    pygame.draw.rect(context, (15,15,15), (x*10, y*10, 10, 10))
                    pygame.draw.rect(context, (30,30,30), (x*10, y*10, 10, 10), 1)

    def save(self, filename:str) -> None:
        with open(filename, mode="w", encoding="utf-8") as fp:
            fp.write(str(self.__world))

    def load(self, filename:str) -> None:
        with open(filename, mode="r", encoding="utf-8") as fp:
            data = fp.read()
            data = data.strip("[] \n\t")  # elimina corchetes y espacios
            self.__world = [int(v.strip()) for v in data.split(",") if v.strip().isdigit()]

