import pygame as pg

class SpriteAnimated(pg.sprite.Sprite):

    def __init__(self,surface: pg.surface,state:str,time_per_frame:float=0.2):
        super().__init__()
        self.surface=surface
        self.state = state

        self.num_frames=0
        self.current_frame=0

        self.idle = [pg.image.load('./image/clipart1580513.png')]
        self.move = [pg.image.load('./image/sprite_worm_tile006.png'),pg.image.load('./image/sprite_worm_tile007.png'),
                        pg.image.load('./image/sprite_worm_tile008.png'),pg.image.load('./image/sprite_worm_tile009.png'),
                        pg.image.load('./image/sprite_worm_tile010.png'),pg.image.load('./image/sprite_worm_tile011.png')]


        self.jump_left = [pg.image.load('./image/sprite_worm_tile012.png'), pg.image.load('./image/sprite_worm_tile013.png'),
                          pg.image.load('./image/sprite_worm_tile014.png'), pg.image.load('./image/sprite_worm_tile015.png'),
                          pg.image.load('./image/sprite_worm_tile016.png'), pg.image.load('./image/sprite_worm_tile017.png'),
                          pg.image.load('./image/sprite_worm_tile018.png'),pg.image.load('./image/sprite_worm_tile026.png')]

        self.jump_right = [pg.image.load('./image/sprite_worm_tile019.png'), pg.image.load('./image/sprite_worm_tile020.png'),
                          pg.image.load('./image/sprite_worm_tile021.png'), pg.image.load('./image/sprite_worm_tile022.png'),
                          pg.image.load('./image/sprite_worm_tile023.png'), pg.image.load('./image/sprite_worm_tile024.png'),
                          pg.image.load('./image/sprite_worm_tile025.png'),pg.image.load('./image/sprite_worm_tile027.png')]
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
        elif self.state == "jump_left":
            self.animation = self.jump_left
            self.num_frames = len(self.jump_left)
        elif self.state == "jump_right":
            self.animation = self.jump_right
            self.num_frames = len(self.jump_right)
        elif self.state=="idle":
            self.animation=self.idle
            self.num_frames=len(self.idle)

    def setCenterPos(self,center:tuple[int,int]):
        self.rect.center=center

    def setScaleImg(self):
        img = self.animation[self.current_frame]
        self.image = pg.transform.scale(img, (40,40))

    def update(self):
        self.current_tick = pg.time.get_ticks()
        self.setNumFrame()
        if self.current_tick-self.prev_tick>=self.time_per_frames*1000:
            self.current_frame+=1
            self.current_frame%=self.num_frames
            self.prev_tick=self.current_tick
            self.setScaleImg()

    def draw(self):
        self.surface.blit(self.image,self.rect)