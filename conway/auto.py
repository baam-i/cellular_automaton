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
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                near = [
                    self.read(x+1, y-1), self.read(x, y-1), self.read(x-1, y-1),
                    self.read(x+1, y),                 self.read(x-1, y),
                    self.read(x-1, y+1), self.read(x, y+1), self.read(x+1, y+1)
                ]
                alive_count = near.count(self.LIVE)
                current = self.read(x, y)

                if current == self.LIVE:
                    self.__next[(y * self.WIDTH) + x] = self.LIVE if alive_count in self.__alive else self.DEAD
                else:
                    self.__next[(y * self.WIDTH) + x] = self.LIVE if alive_count in self.__born else self.DEAD

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

