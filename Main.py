import pygame
import random
import Entities
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("images/background.jpg")

# Background Sound
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Letters")
pygame.display.set_icon(pygame.image.load("images/spaceship32.png"))

# Score
font = pygame.font.Font("fonts/Sketch.otf", 32)
scoreX = 10
scoreY = 10

over_font = pygame.font.Font("fonts/Sketch.otf", 64)
overX = 200
overY = 250

tip_font = pygame.font.Font("fonts/Sketch.otf", 32)

# All letters
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "x", "y", "z"]
original_word_letters = []
word_letters = []
masked_word = []
other_letters = []
enemy_list = []

# Player
player = Entities.Actor("player", pygame.image.load("images/spaceship64.png"), 64, 64, 370, 520, 4, 0)

# Bullet
bullet = Entities.Actor("bullet", pygame.image.load("images/bullet32.png"), 32, 32,
                        0, 520, 0, 8, "ready")


def get_word_and_tip():
    file = open("db.txt", "r")
    lines = file.readlines()
    selected_line = random.randint(0, len(lines) - 1)
    data = lines[selected_line].split(",")
    file.close()
    return data[0], data[1].replace("\n", "")


word, tip = get_word_and_tip()


def create_enemy(letter):
    enemy = Entities.Actor(letter,
                           pygame.image.load("images/letters/letter-" + letter + ".png"), 64, 64,
                           random.randint(0, 736),
                           50, random.randint(1, 3), 40)
    return enemy


def create_letter_from_word():
    letter = random.randint(0, len(word_letters) - 1)
    enemy = create_enemy(word_letters[letter])
    word_letters.pop(letter)
    return enemy


def update_masked_word(enemy):
    initial = 0
    for _ in original_word_letters:
        index = original_word_letters.index(enemy.type, initial)
        if masked_word[index] == "_":
            masked_word[index] = enemy.type
            break
        else:
            initial = index + 1


def update_letter_from_word(enemy):
    update_masked_word(enemy)

    if len(word_letters) == 0:
        update_letter_from_other(enemy)
        return enemy
    else:
        if len(word_letters) == 1:
            letter = random.randint(0, len(word_letters) - 1)
        else:
            letter = 0

        enemy.type = word_letters[letter]
        enemy.image = pygame.image.load("images/letters/letter-" + word_letters[letter] + ".png")
        word_letters.pop(letter)
        return enemy


def create_letter_from_other():
    letter = random.randint(0, len(other_letters) - 1)
    enemy = create_enemy(other_letters[letter])
    return enemy


def update_letter_from_other(enemy):
    letter = random.randint(0, len(other_letters) - 1)
    enemy.type = other_letters[letter]
    enemy.image = pygame.image.load("images/letters/letter-" + other_letters[letter] + ".png")
    return enemy


def show_game_over(win):
    if win:
        text = "Jij wint =)"
    else:
        text = "Jammer =("
    over_text = over_font.render(text, True, (255, 255, 255))
    screen.blit(over_text, (overX, overY))
    for this_enemy in enemy_list:
        this_enemy.change_state("end")
        this_enemy.x = 5000


def show_word():
    masked_word_text = font.render(" ".join(masked_word), True, (255, 255, 255))
    screen.blit(masked_word_text, (scoreX, scoreY))


def show_tip():
    tip_text = tip_font.render("Tip: " + tip, True, (255, 255, 255))
    screen.blit(tip_text, (320, 10))


def move_actor(actor):
    screen.blit(actor.image, (actor.x, actor.y))


def is_collision(enemy, current_bullet):
    if enemy.is_hit(current_bullet):
        colision_sound = mixer.Sound("sounds/explosion.wav")
        colision_sound.play()
        current_bullet.y = player.y + 10
        current_bullet.change_state("ready")

        if enemy.type in original_word_letters:
            update_letter_from_word(enemy)
        else:
            update_letter_from_other(enemy)

        enemy.reset()

        return True

    if enemy.y > player.y - 40:
        show_game_over(False)

    return False


def create_enemy_list():
    enemy_list.append(create_letter_from_word())
    enemy_list.append(create_letter_from_word())
    enemy_list.append(create_letter_from_other())
    enemy_list.append(create_letter_from_other())
    enemy_list.append(create_letter_from_other())


def setup_game(word):
    # Rest default values
    score_value = 0

    original_word_letters = [x for x in word]
    word_letters = [x for x in word]
    other_letters = list(set(letters) - set(word_letters))
    masked_word = []
    for x in word:
        masked_word.append("_")
    player.reset(False)
    bullet.reset(False)

    return score_value, original_word_letters, word_letters, other_letters, masked_word


score_value, original_word_letters, word_letters, other_letters, masked_word = setup_game(word)
create_enemy_list()

# Game Loop
running = True
while running:

    # Screen filled with Black
    screen.fill((0, 0, 0))

    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        command = ""

        # Check keystroke
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                command = "left"

            if event.key == pygame.K_RIGHT:
                command = "right"

            if event.key == pygame.K_SPACE:
                if bullet.state is "ready":
                    bullet_sound = mixer.Sound("sounds/laser.wav")
                    bullet_sound.play()
                    bullet.x = player.x + 16
                    bullet.y = player.y + 10
                    bullet.change_state("fire")

            if event.key == pygame.K_n:
                word, tip = get_word_and_tip()
                enemy_list = []
                score_value, original_word_letters, word_letters, other_letters, masked_word = setup_game(word)
                create_enemy_list()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                command = "stop"

    if bullet.state is "fire":
        bullet.move_up()

    if bullet.y <= 0:
        bullet.y = player.y + 10
        bullet.change_state("ready")

    for enemy in enemy_list:

        if enemy.type in original_word_letters:
            hit = 1
        else:
            hit = 0

        if is_collision(enemy, bullet):
            score_value += hit

    if score_value == len(original_word_letters):
        show_game_over(True)

    # To allow continuous moving
    if command == "left":
        player.move_left()
    elif command == "right":
        player.move_right()
    elif command == "stop":
        player.stop_moving()

    move_actor(player)

    for enemy in enemy_list:
        enemy.move_auto()
        move_actor(enemy)

    if bullet.state is "fire":
        move_actor(bullet)

    show_word()
    show_tip()

    pygame.display.update()
