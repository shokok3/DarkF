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

# --- Враги, журнал и золото -----------------------
enemies = ["волк", "дикий кабан", "лесной упырь", "скелет"]
log = []
gold_total = 0
ability_bonus = 0


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
    """Проводит бой с врагом; bonus по умолчанию равен 0.
    Бонус прибавляется после расчёта критического урона.
    Возвращает (rounds, won, hero_health, loot).
    Печатает ход боя, не изменяет глобальные health и log.
    """
    enemy_hp = 45.0
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
            blow = random.randint(2, 6)
            hero_health -= blow

            line += (
                f" Здоровье врага: {enemy_hp:.1f}. "
                f"{enemy.capitalize()} атакует и наносит "
                f"{blow} урона."
            )

            rounds.append([round_n, hit, blow])

        print(line)

    won = enemy_hp <= 0

    if won:
        loot = 10 + 5 * round_n
    else:
        loot = 0

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


# --- Главный цикл игры -----------------------------
running = True
actions = 0
menu_last = 9
outcome = "прерывание"

try:
    while running:
        # --- Меню действий -----------------------------
        print("Что делаешь?")
        print("1 - осмотреться")
        print("2 - идти вперёд")
        print("3 - отдохнуть")
        print("4 - зажечь факел")
        print("5 - Позвать на помощ")
        print("6 - тренировка")
        print("7 - исследовать глубины леса")
        print("8 - таблица лидеров")
        print("9 - магазин умений")
        print("0 - выйти из леса")
        print()

        # --- Защита от неверного ввода ------------------
        while True:
            choice = input()

            try:
                menu_number = int(choice)
            except ValueError:
                print("Такого пункта нет. Введи номер пункта из меню.")
                continue

            if 0 <= menu_number <= menu_last:
                choice = str(menu_number)
                break

            print("Такого пункта нет. Введи номер пункта из меню.")

        # --- Выбор героя -------------------------------
        match choice:
            case "1":
                print(
                    "Вы осмотрелись. Вокруг только тёмные "
                    "деревья и густой туман."
                )

            case "2":
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

            case "3":
                stamina += 3

                if stamina > max_stamina:
                    stamina = max_stamina

                print("Вы остановились и немного отдохнули.")

            case "4":
                stamina -= 1
                print("Вы зажгли факел. Стало немного светлее.")

            case "5":
                will -= 1
                print(
                    "Вы позвали на помощь, "
                    "но в ответ услышали только тишину."
                )

            case "6":
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

            case "7":
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

            case "8":
                print_leaderboard(log)

            case "9":
                print("Магазин:")
                print("1 - зелье (+10 здоровья): 10 золота")
                print("2 - масло для факела (+5 запаса сил): 15 золота")
                print("3 - боевой эликсир (+2 к урону на весь забег): 40 золота")
                print("Номер товара (0 — ничего не покупать):")

                item = input()
                prices = (10, 15, 40)
                names = ("зелье", "масло для факела", "боевой эликсир")

                if item in ("1", "2", "3"):
                    price = prices[int(item) - 1]
                    name = names[int(item) - 1]

                    print("Количество (Enter — одна штука):")
                    qty_line = input()

                    if qty_line == "":
                        qty = 1
                        gold_total, ok = buy(price, gold_total)
                    else:
                        qty = int(qty_line)
                        gold_total, ok = buy(
                            price, gold_total, quantity=qty
                        )

                    if ok:
                        if item == "1":
                            health = min(health + 10 * qty, max_health)
                        elif item == "2":
                            stamina = min(
                                stamina + 5 * qty, max_stamina
                            )
                        else:
                            ability_bonus += 2 * qty

                        print(
                            f"Куплено: {qty} шт. — {name}, "
                            f"цена {price * qty} золота. "
                            f"Осталось золота: {gold_total}."
                        )
                    else:
                        print(
                            f"Недостаточно золота: нужно {price * qty}, "
                            f"есть {gold_total}."
                        )

                elif item != "0":
                    print("Такого товара в магазине нет.")

            case "0":
                print(
                    "Вы выбираетесь из тёмного леса "
                    "и возвращаетесь к свету."
                )
                outcome = "выход"
                running = False

            case _:
                print("Такого действия нет.")

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

    print_run_summary(log)

    print(frame)
    print()