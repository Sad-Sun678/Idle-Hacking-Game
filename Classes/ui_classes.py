import pygame



import pygame


class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.callback = callback

        self.colors = {
            "normal": (220, 220, 220),
            "hover": (180, 180, 180),
            "pressed": (140, 140, 140),
            "disabled": (100, 100, 100),
        }

        self.enabled = True
        self.state = "normal"

        self.font = pygame.font.SysFont("arial", 18)
        self.text = text
        self._update_text()

    def _update_text(self):
        self.text_surf = self.font.render(self.text, True, (20, 20, 20))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def handle_event(self, event):
        if not self.enabled:
            self.state = "disabled"
            return

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.state = "hover"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.state = "pressed"

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.callback()
        else:
            self.state = "normal"

    def draw(self, screen):
        pygame.draw.rect(screen, self.colors[self.state], self.rect)
        screen.blit(self.text_surf, self.text_rect)
class ConfirmPopup:
    def __init__(self, rect, on_confirm, on_cancel):
        self.rect = pygame.Rect(rect)   # <-- FIX HERE
        self.visible = False
        self.just_opened = False

        self.font = pygame.font.SysFont("arial", 18)

        yes_rect = pygame.Rect(
            self.rect.x + 20,
            self.rect.bottom - 50,
            80,
            30
        )
        no_rect = pygame.Rect(
            self.rect.right - 100,
            self.rect.bottom - 50,
            80,
            30
        )

        self.yes_button = Button(yes_rect, "YES", on_confirm)
        self.no_button = Button(no_rect, "NO", on_cancel)

    def open(self):
        self.visible = True
        self.just_opened = True

    def close(self):
        self.visible = False

    def handle_event(self, event):
        if not self.visible:
            return

        # swallow the click that opened the popup
        if self.just_opened:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == pygame.MOUSEBUTTONUP:
                self.just_opened = False
                return

        self.yes_button.handle_event(event)
        self.no_button.handle_event(event)

    def draw(self, screen, text_lines):
        if not self.visible:
            return

        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        y = self.rect.y + 10
        for line in text_lines:
            surf = self.font.render(line, True, (220, 220, 220))
            screen.blit(surf, (self.rect.x + 10, y))
            y += 22

        self.yes_button.draw(screen)
        self.no_button.draw(screen)
class Tooltip:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 16)

    def draw(self, screen, mx, my, lines):
        if not lines:
            return

        padding = 6
        width = max(self.font.size(line)[0] for line in lines) + padding * 2
        height = len(lines) * 18 + padding * 2

        rect = pygame.Rect(mx + 12, my + 12, width, height)

        pygame.draw.rect(screen, (30, 30, 30), rect)
        pygame.draw.rect(screen, (200, 200, 200), rect, 1)

        y = rect.y + padding
        for line in lines:
            surf = self.font.render(line, True, (220, 220, 220))
            screen.blit(surf, (rect.x + padding, y))
            y += 18

class CurrencyDisplay:
    def __init__(self, rect, currency_type, player):
        self.rect = pygame.Rect(rect)
        self.currency_type = currency_type
        self.player = player

        self.font = pygame.font.SysFont("arial", 20)
        self.color = (255, 255, 255)

    def draw(self, screen):
        amount = self.player.currency[self.currency_type]
        text = f"{self.currency_type}: {amount}"

        text_surf = self.font.render(text, True, (20, 20, 20))
        text_rect = text_surf.get_rect(center=self.rect.center)

        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text_surf, text_rect)