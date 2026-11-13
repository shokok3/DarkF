
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


# --- Команды и меню --------------------------------
commands = [
    "look", "go", "rest", "listen", "torch", "train",
    "descend", "leaders", "shop", "backpack",
    "drink зелье", "buy <предмет> [количество]", "exit"
]

MENU = [
    "Что делаешь? (номер или команда; help — помощь)",
    "1 - осмотреться (look)",
    "2 - идти вперёд (go)",
    "3 - отдохнуть (rest)",
    "4 - прислушаться (listen)",
    "5 - зажечь факел (torch)",
    "6 - тренировка (train)",
    "7 - исследовать глубины леса (descend)",
    "8 - таблица лидеров (leaders)",
    "9 - магазин (shop)",
    "10 - рюкзак (backpack)",
    "11 - выпить зелье (drink)",
    "0 - выйти из леса (exit)"
]

num_to_verb = {
    "1": "look",
    "2": "go",
    "3": "rest",
    "4": "listen",
    "5": "torch",
    "6": "train",
    "7": "descend",
    "8": "leaders",
    "9": "shop",
    "10": "backpack",
    "11": "drink",
    "0": "exit"
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
            case "look":
                print(
                    "Вы осмотрелись. Вокруг только тёмные "
                    "деревья и густой туман."
                )

            case "go":
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

            case "rest":
                stamina += 3

                if stamina > max_stamina:
                    stamina = max_stamina

                print("Вы остановились и немного отдохнули.")

            case "listen":
                print(
                    "Вы прислушались. В глубине леса "
                    "слышится странный шорох."
                )

            case "torch":
                stamina -= 1
                print("Вы зажгли факел. Стало немного светлее.")

            case "train":
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

            case "descend":
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

            case "leaders":
                print_leaderboard(log)

            case "shop":
                print("Магазин:")

                for name, price in prices.items():
                    print(f"{name.capitalize()}: {price} золота")

                print(f"У тебя {gold_total} золота.")
                print("Для покупки введи: buy название предмета количество")

            case "buy":
                if len(words) > 1 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])

                if item == "":
                    print("Что купить? Введи: buy <предмет>.")
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

            case "backpack":
                if not inventory:
                    print("Рюкзак пуст.")
                else:
                    print("Рюкзак:")

                    for name, qty in inventory.items():
                        print(f"{name.capitalize()}: {qty} шт.")

            case "drink":
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
                        f"Ты выпил предмет «{item}». Здоровье: {health}. "
                        f"Осталось: {inventory.get(item, 0)} шт."
                    )

            case "help":
                print("Команды: " + ", ".join(commands) + ".")
                print("Номера от 0 до 11 тоже работают.")

            case "exit":
                print(
                    "Вы выбираетесь из тёмного леса "
                    "и возвращаетесь к свету."
                )
                outcome = "выход"
                running = False

            case _:
                print(
                    f"Не понимаю команду: '{line.strip()}'. "
                    "Введи 'help' для справки."
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
