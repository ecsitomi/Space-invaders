import pygame
import sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser

class Game:
    def __init__(self):
        # HEJ upgrades
        self.alien_laser_speed = 5
        self.move_down_distance = 2
        self.alien_timer = 1100
        self.extra_timer = 20000
        self.update_text = None
        self.update_enemy_text = None
        self.starting = True

        # rect
        self.rect_width = WIDTH
        self.rect_height = 10
        self.rect_color = (0, 0, 255)
        self.rect_y = -20
        self.update_anime = False

        # Player setup
        player_sprite = Player((WIDTH / 2, screen_height), WIDTH)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('../graphics/player.png').convert_alpha()
        self.live_x_start_pos = WIDTH - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('../font/Pixeled.ttf', 16)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 5
        self.obstacle_x_positions = [num * (WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(self.obstacle_x_positions, x_start=WIDTH / 15, y_start=HEIGHT - 400)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=7, cols=13)
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(80, 120)

        # Audio
        music = pygame.mixer.Sound('../audio/music.wav')
        music.set_volume(0.5)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.5)

        # Countdown setup
        self.countdown_time = 20
        self.countdown_font = pygame.font.Font('../font/Pixeled.ttf', 40)

    def restart(self):
        # HEJ upgrades
        self.alien_laser_speed = 5
        self.move_down_distance = 2
        self.alien_timer = 1100
        self.extra_timer = 20000
        self.update_text = None
        self.update_enemy_text = None

        # rect
        self.rect_width = WIDTH
        self.rect_height = 10
        self.rect_color = (0, 0, 255)
        self.rect_y = -20
        self.update_anime = False

        # Player setup
        player_sprite = Player((WIDTH / 2, screen_height), WIDTH)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('../graphics/player.png').convert_alpha()
        self.live_x_start_pos = WIDTH - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('../font/Pixeled.ttf', 16)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 5
        self.obstacle_x_positions = [num * (WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(self.obstacle_x_positions, x_start=WIDTH / 15, y_start=HEIGHT - 400)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=7, cols=13)
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(80, 120)

        # Audio
        music = pygame.mixer.Sound('../audio/music.wav')
        music.set_volume(0.5)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.5)

        # Countdown setup
        self.countdown_time = 20
        self.countdown_font = pygame.font.Font('../font/Pixeled.ttf', 40)

    def create_obstacle(self, x_start, y_start, offset_x, offset_y):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size + offset_y
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, offsets, x_start, y_start):
        for index, offset_x in enumerate(offsets):
            offset_y = index * 50
            self.create_obstacle(x_start, y_start, offset_x, offset_y)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= WIDTH:
                self.alien_direction = -abs(self.alien_direction)
                self.alien_move_down(self.move_down_distance)
            elif alien.rect.left <= 0:
                self.alien_direction = abs(self.alien_direction)
                self.alien_move_down(self.move_down_distance)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, self.alien_laser_speed, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), WIDTH))
            self.extra_spawn_time = randint(500, 800)

    def collision_checks(self):
        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                    self.score -= 150

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1                 

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        screen.blit(score_surf, score_rect)

    def display_countdown(self):
        countdown_surf = self.countdown_font.render(f'{self.countdown_time}', False, 'white')
        countdown_rect = countdown_surf.get_rect(center=(WIDTH / 2, 30))
        screen.blit(countdown_surf, countdown_rect)
        
        if self.update_text is not None:
            update_surf = self.font.render(f'{self.update_text}', False, 'white')
            update_rect = update_surf.get_rect(topleft=(10, 20))
            screen.blit(update_surf, update_rect)

        if self.update_enemy_text is not None:
            update_enemy_surf = self.font.render(f'{self.update_enemy_text}', False, 'white')
            update_enemy_rect = update_surf.get_rect(topleft=(10, 50))
            screen.blit(update_enemy_surf, update_enemy_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('JOB DONE!', False, 'white')
            victory_rect = victory_surf.get_rect(center=(WIDTH / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)
            victory2_surf = self.font.render('Press  ENTER  to  restart!', False, 'yellow')
            victory2_rect = victory2_surf.get_rect(center=(WIDTH / 2, screen_height -100))
            screen.blit(victory2_surf, victory2_rect)

    def defeat_message(self):
        defeat_surf = self.font.render('JOB FAILED!', False, 'white')
        defeat_rect = defeat_surf.get_rect(center=(WIDTH / 2, screen_height / 2))
        screen.blit(defeat_surf, defeat_rect)
        victory2_surf = self.font.render('Press  ENTER  to  restart!', False, 'yellow')
        victory2_rect = victory2_surf.get_rect(center=(WIDTH / 2, screen_height -100))
        screen.blit(victory2_surf, victory2_rect)

    def extra_function(self):
        self.update_anime = True
        # Player upgrades
        player_a = self.player.sprite.speed + 3
        player_b = self.player.sprite.laser_cooldown - 100
        player_c = self.player.sprite.laser_speed - 4

        # Alien upgrades
        alien_a = self.alien_laser_speed + 4
        alien_b = self.alien_timer - 200
        alien_c = self.alien_direction + 3

        # véletlen upgrade
        chosen_player_upgrade = choice([player_a, player_b, player_c])
        if chosen_player_upgrade == player_a:
            if self.player.sprite.speed < 20:
                self.player.sprite.speed = chosen_player_upgrade
                self.update_text = 'Player  Speed  Increased'
            else:
                self.update_text = 'Nothing  Happened'
        elif chosen_player_upgrade == player_b:
            if self.player.sprite.laser_cooldown > 200:
                self.player.sprite.laser_cooldown = chosen_player_upgrade
                self.update_text = 'Player  Laser  Cooldown  Decreased'
            else:
                self.update_text = 'Nothing  Happened'
        elif chosen_player_upgrade == player_c:
            if self.player.sprite.laser_speed > -20:
                self.player.sprite.laser_speed = chosen_player_upgrade
                self.update_text = 'Player  Laser  Speed  Increased'
            else:
                self.update_text = 'Nothing  Happened'

        chosen_alien_upgrade = choice([alien_a, alien_b, alien_c])
        if chosen_alien_upgrade == alien_a:
            if self.alien_laser_speed < 15:
                self.alien_laser_speed = chosen_alien_upgrade
                self.update_enemy_text = 'Alien  Laser  Speed  Increased'
            else:
                self.update_enemy_text = 'Nothing  Happened  With  The  Enemy'
        elif chosen_alien_upgrade == alien_b:
            if self.alien_timer > 500:
                self.alien_timer = chosen_alien_upgrade
                pygame.time.set_timer(ALIENLASER, self.alien_timer)
                self.update_enemy_text = 'Alien  Laser  Cooldown  Decreased'
            else:
                self.update_enemy_text = 'Nothing  Happened  With  The  Enemy'
        elif chosen_alien_upgrade == alien_c:
            if self.alien_direction < 10:
                self.alien_direction = chosen_alien_upgrade
                self.update_enemy_text = 'Alien  Speed  Increased'
            else:
                self.update_enemy_text = 'Nothing  Happened  With  The  Enemy'

    def animation(self):
        if self.update_anime:
            self.rect_y += 50
        if self.rect_y >= HEIGHT:
            self.rect_y = -20
            self.update_anime = False

    def run(self):
        if self.lives > 0:
            self.player.update()
            self.alien_lasers.update()
            self.extra.update()
            self.aliens.update(self.alien_direction)
            self.alien_position_checker()
            self.extra_alien_timer()
            self.collision_checks()
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            self.extra.draw(screen)
            self.display_lives()
            self.display_score()
            self.display_countdown()
            self.victory_message()

            # Rect animation
            self.animation()
            pygame.draw.rect(screen, self.rect_color, (0, self.rect_y, self.rect_width, self.rect_height))

        if self.lives <= 0:
            self.player.empty()
            self.alien_lasers.empty()
            self.aliens.empty()
            self.defeat_message()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.restart()

        if not self.aliens.sprites():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.alien_lasers.empty()
                self.player.empty()
                self.restart()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load('../graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (WIDTH, HEIGHT))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(HEIGHT / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (WIDTH, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))

def starting_message():
        global starting
        font = pygame.font.Font('../font/Pixeled.ttf', 22)
        starting_surf = font.render('YOUR  JOB:', False, 'white')
        starting_rect = starting_surf.get_rect(center=(WIDTH / 2, screen_height / 2))
        screen.blit(starting_surf, starting_rect)

        starting2_surf = font.render('DESTROY  THE  SPACE  INVADERS ', False, 'red')
        starting2_rect = starting2_surf.get_rect(center=(WIDTH / 2, screen_height / 2+60))
        screen.blit(starting2_surf, starting2_rect)

        starting3_surf = font.render('TO  SAVE  MOTHER  EARTH !', False, 'white')
        starting3_rect = starting3_surf.get_rect(center=(WIDTH / 2, screen_height / 2+120))
        screen.blit(starting3_surf, starting3_rect)

        victory2_surf = font.render('Press  ENTER  to  Start!', False, 'yellow')
        victory2_rect = victory2_surf.get_rect(center=(WIDTH / 2, screen_height -100))
        screen.blit(victory2_surf, victory2_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            starting = False

if __name__ == '__main__':
    pygame.init()
    MONITOR = pygame.display.Info()
    WIDTH = MONITOR.current_w
    HEIGHT = MONITOR.current_h
    screen_height = HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    crt = CRT()
    starting = True
    game = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not starting and event.type == ALIENLASER:
                game.alien_shoot()
            if not starting and event.type == EXTRATIMER:  # Correct handling for the extra timer
                game.countdown_time = 20
                game.extra_function()
            if not starting and event.type == COUNTDOWN:
                game.countdown_time -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


        screen.fill((30, 30, 30))
        if starting:
            starting_message()
        if not starting:
            if game is None:
                game = Game()
                # időzítők
                alientimer = game.alien_timer
                ALIENLASER = pygame.USEREVENT + 1
                pygame.time.set_timer(ALIENLASER, alientimer)

                extratimer = game.extra_timer
                EXTRATIMER = pygame.USEREVENT + 2
                pygame.time.set_timer(EXTRATIMER, extratimer)

                COUNTDOWN = pygame.USEREVENT + 3
                pygame.time.set_timer(COUNTDOWN, 1000)

            game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)
