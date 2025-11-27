import sys
from time import sleep
import pygame
#Asking Python to import tool kits, sys (settings) and pygame (game engine)
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Yasmin's Alien Invasion")
        self.clock = pygame.time.Clock()
        # Set the background color.
        self.settings = Settings()
        self.settings.bg_color = (0, 0, 0)
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.game_active = True

        self._create_fleet()
    def run_game(self):
        while True:
            pygame.display.flip()
            self._check_events()
            if self.game_active:
              self.ship.update()
              self._update_aliens()
              self._update_bullets()
            self._update_screen()
            self.clock.tick(60) 
        # Handle events
    def _check_events(self):
        # Make the most recently drawn screen visible.  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: 
                 self._check_keydown_events(event) 
            elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
    def _check_keydown_events(self, event):
                if event.key == pygame.K_RIGHT:
                     self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                    #Below code is for quitting the game when the 'q' key is pressed
                elif event.key == pygame.K_q:
                     sys.exit()
                elif event.key == pygame.K_SPACE:
                     self._fire_bullet()
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
    def _check_keyup_events(self, event): 
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:  # optional limit on bullets
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)  
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_y = alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            current_x = alien_width  # reset to left for each row
            while current_x < (self.settings.screen_width - 2 * alien_width):
                  self._create_alien(current_x, current_y)
                  current_x += 2 * alien_width
            current_y += 2 * alien_height  # move down to next row
    def _update_aliens(self):
         """Update the positions of all aliens in the fleet."""
         self._check_fleet_edges()
         self.aliens.update()
            # Look for alien-ship collisions.   
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self._ship_hit()
         self._check_aliens_bottom()
    def _check_fleet_edges(self):
         """Respond appropriately if any aliens have reached an edge."""
         for alien in self.aliens.sprites():
             if alien.check_edges():
                 self._change_fleet_direction()
                 break
    def _change_fleet_direction(self):
         """Drop the entire fleet and change the fleet's direction."""
         for alien in self.aliens.sprites():
             alien.rect.y += self.settings.fleet_drop_speed
         self.settings.fleet_direction *= -1
    def _create_alien(self, x_position, y_position):
         """Create an alien and place it in the row."""
         new_alien = Alien(self)
         new_alien.x = x_position
         new_alien.rect.x = x_position
         self.aliens.add(new_alien)
         new_alien.rect.y = y_position
    def _update_bullets(self):
         self.bullets.update()
         """Update position of bullets and get rid of old bullets."""
         # Update bullet positions.
         collisions = pygame.sprite.groupcollide(
         self.bullets, self.aliens, True, True)
         if not self.aliens:
             # Destroy existing bullets and create a new fleet.
             self.bullets.empty()
             self._create_fleet()
             self.settings.increase_speed()
         # Get rid of bullets that have disappeared.
         for bullet in self.bullets.copy():
             if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)
         # Redraw the bullets.
         for bullet in self.bullets.sprites():
             bullet.draw_bullet()      
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
    def _ship_hit(self):    
        """Respond to ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            # If the ship runs out of lives, set game_active to False.
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this as if the ship got hit.
                self._ship_hit()
                break


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()


        





