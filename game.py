# ================================================
# ИГРА «ТЕМНЫЙ ЛЕС»
# Автор: Буслаев Матвей
# Дата: сентябрь 2026
#
# Пункт 4 — «прислушаться»: герой замирает
# и слушает, что происходит в темноте. Пока
# пункт только выводится в меню — обрабатывать
# ================================================
# --- Заголовок ------------------------------------
title = "ТЕМНЫЙ ЛЕС"
frame = "=" * 16
print(frame)
print(" " + title + " ")
print(frame)
print()
# --- Знакомство с героем --------------------------
print("Как тебя зовут,путник")
hero_name = input()
print(f"Приветсвую тебя, {hero_name}!")
print("Ты входишь в лес. Здесь темно и пахнет гилой плотью.")
print()

# --- Настройка героя ------------------------------
print("Настройка героя.")
print("Здоровье, сила, ловкость, воля — по одному числу в строке:")
health = int(input())
strength = int(input())
agility = int(input())
will = int(input())

# --- Расчёт урона ---------------------------------
base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2

# Запас сил героя
stamina = health // 10 + will
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

# --- Главный цикл игры -----------------------------
running = True
actions = 0

while running:
    # --- Меню действий -----------------------------
    print("Что делаешь?")
    print("1 - осмотреться")
    print("2 - идти вперёд")
    print("3 - отдохнуть")
    print("4 - зажечь факел")
    print("5 - Позвать на помощ")
    print("6 - тренировка")
    print("0 - выйти из леса")
    print()

    # --- Защита от неверного ввода ------------------
    valid = ("0", "1", "2", "3", "4", "5", "6")
    choice = input()

    while choice not in valid:
        print("Такого пункта нет. Введи номер пункта из меню.")
        choice = input()

    # --- Выбор героя -------------------------------
    match choice:
        case "1":
            print("Вы осмотрелись. Вокруг только тёмные деревья и густой туман.")

        case "2":
            cost = 2

            if stamina >= cost:
                stamina -= cost
                print("Вы осторожно идёте вперёд. Ветки хрустят под ногами.")
            else:
                health -= cost - stamina
                stamina = 0
                print("Сил больше нет — вы идёте на одном упорстве.")

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
            print("Вы позвали на помощь, но в ответ услышали только тишину.")

        case "6":
            strikes = 6
            total_damage = 0
            crit_count = 0

            print("Вы подходите к тренировочному чучелу.")
            print("Оно стоит здесь среди старых деревьев.")
            print()
            print(f"Наносите {strikes} ударов.")

            for i in range(1, strikes + 1):
                if i % 3 == 0:
                    hit_damage = crit_damage
                    crit_count = crit_count + 1
                    print(f"Удар {i}: {hit_damage:.1f} — критический!")
                else:
                    hit_damage = damage
                    print(f"Удар {i}: {hit_damage:.1f}")

                total_damage = total_damage + hit_damage

            print()
            print(f"Итог: {strikes} ударов, критических ударов: {crit_count}")
            print(f"Общий урон: {total_damage:.1f}")

            average_damage = total_damage / strikes
            print(f"Средний урон: {average_damage:.1f}")

            stamina -= 4

        case "0":
            print("Вы выбираетесь из тёмного леса и возвращаетесь к свету.")
            running = False

        case _:
            print("Такого действия нет.")

    # --- Счётчик действий ---------------------------
    if running:
        actions += 1

    print()
    print(f"Здоровье: {health} Запас сил: {stamina}")

    # --- Проверка гибели ----------------------------
    if health <= 0:
        print(f"{hero_name} падает без сил. Тёмный лес забирает ещё одного путника.")
        running = False

# --- Прощание --------------------------------------
print()
print(frame)

if health <= 0:
    print(f"Ты не выбрался, {hero_name}. Действий совершено: {actions}.")
else:
    print(f"Забег окончен, {hero_name}. Действий совершено: {actions}.")

print(frame)
print()