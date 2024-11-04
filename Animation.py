import pygame

class SpriteAnimated(pygame.sprite.Sprite):

    def __init__(self,surface: pygame.surface,state:str,time_per_frame:float=0.2):
        super().__init__()
        self.surface=surface
        self.state = state

        self.num_frames=0
        self.current_frame=0

        self.shooting = [pygame.image.load('./image/clipart1580513.png')]
        self.idle=[pygame.image.load('./image/sprite_worm_tile006.png')]
        self.move = [pygame.image.load('./image/sprite_worm_tile006.png'),pygame.image.load('./image/sprite_worm_tile007.png'),
                        pygame.image.load('./image/sprite_worm_tile008.png'),pygame.image.load('./image/sprite_worm_tile009.png'),
                        pygame.image.load('./image/sprite_worm_tile010.png'),pygame.image.load('./image/sprite_worm_tile011.png')]

        self.jump = [pygame.image.load('./image/sprite_worm_tile019.png'), pygame.image.load('./image/sprite_worm_tile020.png'),
                          pygame.image.load('./image/sprite_worm_tile021.png'), pygame.image.load('./image/sprite_worm_tile022.png'),
                          pygame.image.load('./image/sprite_worm_tile023.png'), pygame.image.load('./image/sprite_worm_tile024.png'),
                          pygame.image.load('./image/sprite_worm_tile025.png'),pygame.image.load('./image/sprite_worm_tile027.png')]
        self.animation=[]

        self.prev_tick=0 # milliseconds
        self.current_tick=0 # milliseconds
        self.time_per_frames=time_per_frame # seconds

        self.setNumFrame()
        self.image=self.animation[self.current_frame]
        self.setScaleImg()
        self.rect=self.image.get_rect()

    def setNumFrame(self):
        if self.state == "move":
            self.animation = self.move
            self.num_frames = len(self.move)

        elif self.state == "jump":
            self.animation = self.jump
            self.num_frames = len(self.jump)
        elif self.state=="idle":
            self.animation=self.idle
            self.num_frames=len(self.idle)
        elif self.state=="shooting":
            self.animation = self.shooting
            self.num_frames = len(self.shooting)

    def setCenterPos(self,center:tuple[int,int]):
        self.rect.center=center

    def setScaleImg(self):
        img = self.animation[self.current_frame]
        self.image = pygame.transform.scale(img, (40,40))

    def update(self):
        self.current_tick = pygame.time.get_ticks()
        self.setNumFrame()
        if self.current_tick-self.prev_tick>=self.time_per_frames*1000:
            self.current_frame+=1
            self.current_frame%=self.num_frames
            self.prev_tick=self.current_tick
            self.setScaleImg()

    def draw(self):
        self.surface.blit(self.image,self.rect)