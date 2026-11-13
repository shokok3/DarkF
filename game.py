
# ================================================
# ИГРА «ТЕМНЫЙ ЛЕС»
# Автор: Буслаев Матвей
# Дата: сентябрь 2026
#
# Бонус эликсира прибавляется после расчёта критического урона.
# Каждая штука эликсира увеличивает бонус на 2.
# ================================================

import random

# --- Заголовок ------------------------------------
title = "ТЕМНЫЙ ЛЕС"
frame = "=" * 16

# --- Расчёт урона ---------------------------------
base_attack = 10

# --- Знакомство с героем --------------------------
print(frame)
print(" " + title + " ")
print(frame)
print()

print("Как тебя зовут,путник")
hero_name = input()
print(f"Приветсвую тебя, {hero_name}!")
print("Ты входишь в лес. Здесь темно и пахнет гилой плотью.")
print()

# --- Настройка героя ------------------------------
print("Настройка героя.")
print("Здоровье, сила, ловкость, воля — по одному числу в строке:")

while True:
    try:
        health = int(input())
        strength = int(input())
        agility = int(input())
        will = int(input())

        if health <= 0:
            raise ValueError(
                f"Здоровье должно быть положительным, а введено {health}"
            )

        if strength < 0 or agility < 0 or will < 0:
            raise ValueError(
                "Сила, ловкость и воля не могут быть отрицательными"
            )

        break

    except ValueError as e:
        print(f"{e}. Введите все четыре числа заново:")

# --- Расчёт характеристик -------------------------
damage = base_attack + strength * 1.5
crit_damage = damage * 2

stamina = health // 10 + will
max_health = health
max_stamina = stamina

# --- Формуляр героя -------------------------------
print("Характеристики героя:")
print(f"Здоровье: {health}")
print(f"Сила: {strength}")
print(f"Ловкость: {agility}")
print(f"Воля: {will}")
print()
print(f"Урон героя: {damage:.1f}")
print(f"Критический урон: {crit_damage:.1f}")
print(f"Запас сил: {stamina}")
print()

# --- Враги, журнал, золото и инвентарь -------------
enemies = ["волк", "дикий кабан", "лесной упырь", "скелет"]

enemy_stats = {
    "волк": {"hp": 45, "damage": 3, "loot": 10},
    "дикий кабан": {"hp": 45, "damage": 5, "loot": 20},
    "лесной упырь": {"hp": 30, "damage": 4, "loot": 15},
    "скелет": {"hp": 45, "damage": 6, "loot": 25},
}

log = []
gold_total = 0
ability_bonus = 0

prices = {
    "зелье": 10,
    "масло для факела": 15,
    "боевой эликсир": 40
}

inventory = {}


# --- Карта леса ------------------------------------
MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
]

# Позиция героя: строка и столбец стартовой клетки
hero_r, hero_c = 4, 2

# Множество посещённых комнат
visited = {(4, 2)}

# Уникальный лут в комнатах
LOOT = {
    (1, 1): "древняя монета",
    (2, 1): "пыльное зелье",
    (3, 3): "драгоценный камень стража"
}

# Множество уже найденных предметов
found_loot = set()

# Направления движения
DIRECTIONS = {
    "север": (-1, 0),
    "юг": (1, 0),
    "запад": (0, -1),
    "восток": (0, 1)
}


# --- Функция критического удара --------------------
def hero_hit(strike_n):
    """Принимает номер удара.
    Возвращает пару (урон, признак критического удара).
    Читает damage и crit_damage, глобальные переменные не меняет.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


# --- Функция боя -----------------------------------
def fight(enemy, hero_health, bonus=0):
    """Бой с enemy до гибели одного из двоих.
    Карточка врага берётся из enemy_stats по имени: нужны ключи
    hp, damage, loot. Печатает строки раундов.
    Бонус прибавляется после расчёта критического урона.
    Возвращает (rounds, won, hero_health, loot).
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
    rounds = []
    round_n = 0

    print(
        f"Ты пробираешься в чащу. "
        f"Из темноты появляется {enemy}!"
    )

    while enemy_hp > 0 and hero_health > 0:
        round_n += 1

        hit, crit = hero_hit(round_n)
        hit += bonus
        enemy_hp -= hit

        if crit:
            line = (
                f"Раунд {round_n}: ты наносишь "
                f"{hit:.1f} урона — критический удар!"
            )
        else:
            line = f"Раунд {round_n}: ты наносишь {hit:.1f} урона."

        if enemy_hp <= 0:
            line += " Враг повержен."
            rounds.append([round_n, hit, 0])
        else:
            blow = stats["damage"]
            hero_health -= blow

            line += (
                f" Здоровье врага: {enemy_hp:.1f}. "
                f"{enemy.capitalize()} атакует и наносит "
                f"{blow} урона."
            )

            rounds.append([round_n, hit, blow])

        print(line)

    won = enemy_hp <= 0
    loot = stats["loot"] if won else 0

    return rounds, won, hero_health, loot


# --- Функция таблицы лидеров -----------------------
def print_leaderboard(log):
    """Принимает журнал боёв.
    Возвращает None.
    Печатает топ-3 раундов по урону героя и рекорд врага.
    """
    if not log:
        print("Ты ещё не сражался с врагами.")
        return

    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]

    print("Таблица лидеров (урон героя):")

    for i in range(len(top)):
        print(
            f"{i + 1}. Раунд {top[i][0]}: "
            f"{top[i][1]:.1f}"
        )

    worst = max(log, key=lambda r: r[2])

    print(
        f"Самый сильный удар врага: {worst[2]} "
        f"(раунд {worst[0]})."
    )


# --- Функция итогов забега -------------------------
def print_run_summary(log):
    """Принимает журнал боёв.
    Возвращает None.
    Печатает суммарный и средний урон героя за забег.
    """
    total = sum(r[1] for r in log)
    rounds = len(log)

    if rounds > 0:
        print(
            f"Общий урон: {total:.1f} за {rounds} раундов, "
            f"средний урон: {total / rounds:.1f}."
        )
    else:
        print("За этот забег боёв не было.")


# --- Функция покупки -------------------------------
def buy(price, gold, quantity=1):
    """Покупает quantity товаров по цене price.
    quantity по умолчанию равен 1.
    Возвращает (gold_left, ok), ничего не печатает.
    """
    cost = price * quantity

    if gold >= cost:
        return gold - cost, True

    return gold, False


# --- Функция разведки карты ------------------------
def scout(r, c, seen):
    """Рекурсивно считает количество доступных комнат."""

    # Проверяем, не вышли ли координаты за границы карты
    if r < 0 or r >= len(MAP) or c < 0 or c >= len(MAP[r]):
        return 0

    # Проверяем, посещали ли комнату и не является ли она стеной
    if (r, c) in seen or MAP[r][c] == "#":
        return 0

    seen.add((r, c))
    total = 1

    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)

    return total


# --- Команды и меню --------------------------------
commands = [
    "осмотреться",
    "идти [север/юг/запад/восток]",
    "отдохнуть",
    "прислушаться",
    "зажечь факел",
    "тренировка",
    "исследовать глубины леса",
    "таблица лидеров",
    "магазин",
    "рюкзак",
    "выпить зелье",
    "купить <предмет> [количество]",
    "карта",
    "разведка",
    "помощь",
    "выйти"
]

MENU = [
    "Что делаешь? (номер или команда; помощь — справка)",
    "1 - осмотреться",
    "2 - идти вперёд или указать направление",
    "3 - отдохнуть",
    "4 - прислушаться",
    "5 - зажечь факел",
    "6 - тренировка",
    "7 - исследовать глубины леса",
    "8 - таблица лидеров",
    "9 - магазин",
    "10 - рюкзак",
    "11 - выпить зелье",
    "12 - показать карту",
    "13 - разведать доступные комнаты",
    "0 - выйти из леса"
]

num_to_verb = {
    "1": "осмотреться",
    "2": "идти",
    "3": "отдохнуть",
    "4": "прислушаться",
    "5": "факел",
    "6": "тренировка",
    "7": "исследовать",
    "8": "лидеры",
    "9": "магазин",
    "10": "рюкзак",
    "11": "выпить",
    "12": "карта",
    "13": "разведка",
    "0": "выйти"
}


# --- Главный цикл игры -----------------------------
running = True
actions = 0
outcome = "прерывание"

try:
    while running:
        # --- Меню действий -----------------------------
        print("\n".join(MENU))
        print()

        # --- Чтение и обработка команды -----------------
        line = input()
        cmd = line.strip().lower()

        while cmd == "":
            print("Пустая команда. Введи команду или номер.")
            line = input()
            cmd = line.strip().lower()

        words = cmd.split()
        verb = words[0]

        if cmd in num_to_verb:
            verb = num_to_verb[cmd]

        # --- Выбор героя -------------------------------
        match verb:
            case "осмотреться":
                print(
                    "Вы осмотрелись. Вокруг только тёмные "
                    "деревья и густой туман."
                )

            case "идти":
                if len(words) > 1 and words[1] in DIRECTIONS:
                    dr, dc = DIRECTIONS[words[1]]
                    nr, nc = hero_r + dr, hero_c + dc

                    if (
                        0 <= nr < len(MAP)
                        and 0 <= nc < len(MAP[nr])
                        and MAP[nr][nc] != "#"
                    ):
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))

                        if (hero_r, hero_c) in LOOT:
                            item = LOOT[(hero_r, hero_c)]

                            if item not in found_loot:
                                found_loot.add(item)
                                print(
                                    f"Вы нашли предмет: {item}! "
                                    f"Уникальных находок: {len(found_loot)}."
                                )

                        print(
                            f"Вы идёте на {words[1]}. "
                            f"Комната ({hero_r}, {hero_c})."
                        )
                    else:
                        print(
                            f"Нельзя идти на {words[1]}: "
                            "там стена или край карты."
                        )

                else:
                    cost = 2

                    if stamina >= cost:
                        stamina -= cost
                        print(
                            "Вы осторожно идёте вперёд. "
                            "Ветки хрустят под ногами."
                        )
                    else:
                        health -= cost - stamina
                        stamina = 0
                        print(
                            "Сил больше нет — вы идёте "
                            "на одном упорстве."
                        )

            case "отдохнуть":
                stamina += 3

                if stamina > max_stamina:
                    stamina = max_stamina

                print("Вы остановились и немного отдохнули.")

            case "прислушаться":
                print(
                    "Вы прислушались. В глубине леса "
                    "слышится странный шорох."
                )

            case "факел":
                stamina -= 1
                print("Вы зажгли факел. Стало немного светлее.")

            case "тренировка":
                strikes = 6
                total_damage = 0
                crit_count = 0

                print("Вы подходите к тренировочному чучелу.")
                print("Оно стоит здесь среди старых деревьев.")
                print()
                print(f"Наносите {strikes} ударов.")

                for i in range(1, strikes + 1):
                    hit_damage, crit = hero_hit(i)

                    if crit:
                        crit_count += 1
                        print(
                            f"Удар {i}: {hit_damage:.1f} "
                            "— критический!"
                        )
                    else:
                        print(f"Удар {i}: {hit_damage:.1f}")

                    total_damage += hit_damage

                print()
                print(
                    f"Итог: {strikes} ударов, "
                    f"критических ударов: {crit_count}"
                )
                print(f"Общий урон: {total_damage:.1f}")

                average_damage = total_damage / strikes
                print(f"Средний урон: {average_damage:.1f}")

                stamina -= 4

            case "исследовать":
                if not enemies:
                    print(
                        "В этой части леса больше "
                        "не осталось врагов."
                    )
                else:
                    enemy = random.choice(enemies)

                    rounds, won, health, loot = fight(
                        enemy, health, bonus=ability_bonus
                    )

                    for r in rounds:
                        log.append(r)

                    if won:
                        gold_total += loot
                        enemies.remove(enemy)

                        print(
                            f"{enemy.capitalize()} повержен! "
                            f"Врагов осталось в лесу: {len(enemies)}. "
                            f"Добыча: {loot} золота."
                        )

                    print(f"Бой окончен. Раундов: {len(rounds)}.")

            case "лидеры":
                print_leaderboard(log)

            case "магазин":
                print("Магазин:")

                for name, price in prices.items():
                    print(f"{name.capitalize()}: {price} золота")

                print(f"У тебя {gold_total} золота.")
                print("Для покупки введи: купить название предмета количество")

            case "купить":
                if len(words) > 1 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])

                if item == "":
                    print("Что купить? Введи: купить <предмет>.")
                    continue

                if item not in prices:
                    print("Такого предмета в магазине нет.")
                    continue

                if qty <= 0:
                    print("Количество должно быть больше нуля.")
                    continue

                price = prices[item]
                gold_total, ok = buy(
                    price, gold_total, quantity=qty
                )

                if ok:
                    inventory[item] = inventory.get(item, 0) + qty

                    print(
                        f"Куплено {qty} шт. предмета «{item}» "
                        f"за {price * qty} золота. "
                        f"Осталось золота: {gold_total}."
                    )
                else:
                    print(
                        f"Недостаточно золота: нужно "
                        f"{price * qty}, есть {gold_total}."
                    )
                    continue

            case "рюкзак":
                if not inventory:
                    print("Рюкзак пуст.")
                else:
                    print("Рюкзак:")

                    for name, qty in inventory.items():
                        print(f"{name.capitalize()}: {qty} шт.")

            case "выпить":
                item = " ".join(words[1:]) or "зелье"

                if inventory.get(item, 0) == 0:
                    print(f"В рюкзаке нет предмета «{item}».")
                    continue
                else:
                    health = min(health + 10, max_health)
                    inventory[item] -= 1

                    if inventory[item] == 0:
                        del inventory[item]

                    print(
                        f"Вы выпили предмет «{item}». Здоровье: {health}. "
                        f"Осталось: {inventory.get(item, 0)} шт."
                    )

            case "карта":
                print("Карта леса:")

                for i in range(len(MAP)):
                    cells = []

                    for j in range(len(MAP[i])):
                        cell = (
                            "@"
                            if (i, j) == (hero_r, hero_c)
                            else MAP[i][j]
                        )
                        cells.append(cell)

                    print(" ".join(cells))

            case "разведка":
                seen = set()
                total_rooms = scout(hero_r, hero_c, seen)
                print(
                    f"Разведка: доступно комнат — {total_rooms}."
                )

            case "помощь":
                print("Команды: " + ", ".join(commands) + ".")
                print("Номера от 0 до 13 тоже работают.")

            case "выйти":
                print(
                    "Вы выбираетесь из тёмного леса "
                    "и возвращаетесь к свету."
                )
                outcome = "выход"
                running = False

            case _:
                print(
                    f"Не понимаю команду: '{line.strip()}'. "
                    "Введи 'помощь' для справки."
                )
                continue

        # --- Счётчик действий ---------------------------
        if running:
            actions += 1

        print()
        print(
            f"Здоровье: {health} Запас сил: {stamina} "
            f"Врагов осталось: {len(enemies)} Золото: {gold_total}"
        )

        # --- Проверка гибели ----------------------------
        if health <= 0:
            print(
                f"{hero_name} падает без сил. "
                "Тёмный лес забирает ещё одного путника."
            )
            outcome = "гибель"
            running = False

except KeyboardInterrupt:
    print()
    print("Ты решил прервать путешествие и покинуть тёмный лес.")

finally:
    # --- Прощание --------------------------------------
    print()
    print(frame)

    if outcome == "гибель":
        print(
            f"Ты не выбрался, {hero_name}. "
            f"Действий совершено: {actions}."
        )
    elif outcome == "выход":
        print(
            f"Забег окончен, {hero_name}. "
            f"Действий совершено: {actions}."
        )
    else:
        print(
            f"Путешествие прервано, {hero_name}. "
            f"Действий совершено: {actions}."
        )

    if inventory:
        print("Оставшиеся предметы в рюкзаке:")
        for name, qty in inventory.items():
            print(f"{name.capitalize()}: {qty} шт.")
    else:
        print("В рюкзаке ничего не осталось.")

    print_run_summary(log)

    print(frame)
    print()
