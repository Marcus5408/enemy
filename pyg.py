import pygame

class Square:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (255, 0, 0)
        self.velocity = 0
        self.gravity = 0.5

    def update(self):
        self.velocity += self.gravity
        if self.velocity > 15:
            self.velocity = 15
        self.rect.y += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.rect.y -= 10
        if keys[pygame.K_s]:
            self.rect.y += 5

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 255, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Goal:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (255, 255, 0)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Barrier:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.color = (0, 0, 255)
        self.placed = False

    def place(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.placed = True

    def draw(self, screen):
        if self.placed:
            pygame.draw.rect(screen, self.color, self.rect)

class Game:
    def __init__(self):
        self.screenSize = (800, 600)
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("Game Making Toolkit")
        self.clock = pygame.time.Clock()
        self.running = True
        self.square = Square(400, 50, 50)
        self.platform = Platform(300, 500, 300, 10)
        self.goal = Goal(self.screenSize[0] - 70, 450, 50)
        self.barrier = Barrier()
        self.positions = []
        self.replaying = False
        self.replay_index = 0

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.replaying:
                    x, y = event.pos
                    self.barrier.place(x, y, 50, 10)

            if not self.replaying:
                self.square.handle_keys()
                self.square.update()
                self.positions.append((self.square.rect.x, self.square.rect.y))
            else:
                if self.replay_index < len(self.positions):
                    self.square.rect.x, self.square.rect.y = self.positions[self.replay_index]
                    self.replay_index += 1
                else:
                    self.running = False

            if self.square.rect.colliderect(self.platform.rect):
                self.square.rect.bottom = self.platform.rect.top
                self.square.velocity = 0

            if self.square.rect.top > self.screenSize[1]:
                self.square.rect.x = (self.screenSize[0] // 2) - (self.square.rect.width // 2)
                self.square.rect.y = (self.screenSize[1] // 2) - (self.square.rect.height // 2)
                self.square.velocity = 0

            if self.square.rect.colliderect(self.goal.rect) and not self.replaying:
                self.replaying = True
                self.square.rect.x, self.square.rect.y = self.positions[0]
                self.replay_index = 0

            if self.square.rect.colliderect(self.barrier.rect):
                self.running = False

            self.screen.fill((0, 0, 0))
            self.square.draw(self.screen)
            self.platform.draw(self.screen)
            self.goal.draw(self.screen)
            self.barrier.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()