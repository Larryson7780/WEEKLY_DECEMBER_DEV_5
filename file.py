import sys
import pygame

# initialisation
pygame.init()

width, height = 800, 600
fenetre = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

couleur_fenetre = (255, 228, 225)
objet_width, objet_height = 30, 30
objet = pygame.Rect(50, height - objet_height, objet_width, objet_height)
couleur_objet = (173, 200, 230)

# Ajout de la vélocité verticale et horizontale
velocite_objet_x = 0
velocite_objet_y = 0
acceleration_x = 1  # Nouvelle variable pour l'accélération

# Ajout d'un tuyau fixe
tuyau_width, tuyau_height = 50, 150
tuyau = pygame.Rect(500, height - tuyau_height, tuyau_width, tuyau_height)
couleur_tuyau = (0, 128, 0)

# Ajout du message de bienvenue
font = pygame.font.Font(None, 36)
welcome_text = font.render("Bienvenue ! Appuyez sur une touche pour commencer", True, (0, 0, 0))
welcome_rect = welcome_text.get_rect(center=(width // 2, height // 2))

# Boucle principale
running = False
while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
        elif event.type == pygame.KEYDOWN:
            running = True

    fenetre.fill(couleur_fenetre)
    fenetre.blit(welcome_text, welcome_rect)
    pygame.display.flip()

# Réinitialisation de la position de l'objet
objet.x = 50
objet.y = height - objet_height

# Boucle principale du jeu
running = True
victoire = False
restart_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocite_objet_y = -10
            elif event.key == pygame.K_LEFT:
                velocite_objet_x = max(velocite_objet_x - acceleration_x, -5)
            elif event.key == pygame.K_RIGHT:
                velocite_objet_x = min(velocite_objet_x + acceleration_x, 5)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Vérifier si le clic de souris est à l'intérieur du bouton de redémarrage
            if restart_button_rect.collidepoint(event.pos):
                # Réinitialiser les variables pour recommencer
                victoire = False
                objet.x = 50
                objet.y = height - objet_height
                velocite_objet_x = 0
                velocite_objet_y = 0

    # Mise à jour de la vélocité verticale et de la position y de l'objet
    velocite_objet_y += 1
    objet.y += velocite_objet_y

    # Limiter la position y pour éviter que l'objet ne disparaisse hors de l'écran
    if objet.y > height - objet_height:
        objet.y = height - objet_height
        velocite_objet_y = 0

    # Mise à jour de la position x de l'objet
    objet.x += velocite_objet_x

    # Limiter la position x pour éviter que l'objet ne disparaisse hors de l'écran
    objet.x = max(0, min(objet.x, width - objet_width))

    # Vérifier la collision avec le tuyau
    if objet.colliderect(tuyau) and objet.y < tuyau.y:
        objet.y = tuyau.y - objet_height
        velocite_objet_y = 0
        victoire = True

    # Rafraîchissement de l'écran
    fenetre.fill(couleur_fenetre)
    pygame.draw.rect(fenetre, couleur_objet, objet)
    pygame.draw.rect(fenetre, couleur_tuyau, tuyau)

    # Afficher un message de victoire si nécessaire
    if victoire:
        font = pygame.font.Font(None, 36)
        victory_text = font.render("Vous avez gagné, l'oiseau fait une pause !", True, (0, 0, 0))
        victory_rect = victory_text.get_rect(center=(width // 2, height // 2))
        fenetre.blit(victory_text, victory_rect)

        # Afficher le bouton de redémarrage
        pygame.draw.rect(fenetre, (0, 255, 0), restart_button_rect)
        font = pygame.font.Font(None, 30)
        restart_text = font.render("Recommencer", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=restart_button_rect.center)
        fenetre.blit(restart_text, restart_rect)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()
