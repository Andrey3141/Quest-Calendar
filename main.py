import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta, date
import threading
import time
import calendar
from plyer import notification
import math
import random

class ChristmasScene:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Волшебная Новогодняя Комната")
        self.window.geometry("1000x800")  # Увеличил размер окна
        self.window.configure(bg='#1a1a2e')
        
        # Добавляем обработчик закрытия окна
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.canvas = tk.Canvas(self.window, width=1000, height=800, bg='#1a1a2e', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Добавил расширение
        
        self.gifts_under_tree = 0
        self.is_closed = False
        self.draw_scene()
        self.update_clock()
        
        # Обработчик изменения размера окна
        self.window.bind('<Configure>', self.on_resize)
    
    def on_resize(self, event):
        """Обработчик изменения размера окна"""
        if not self.is_closed:
            self.draw_scene()
    
    def on_close(self):
        """Обработчик закрытия окна"""
        self.is_closed = True
        self.window.destroy()
    
    def draw_scene(self):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        # Получаем текущие размеры окна
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        if width < 100 or height < 100:  # Минимальные размеры
            return
            
        # Очищаем canvas
        self.canvas.delete("all")
        
        # Рисуем пол (деревянный)
        self.canvas.create_rectangle(0, height*0.7, width, height, fill='#8B4513', outline='#654321', width=2)
        
        # Рисуем стены (теплый бежевый)
        self.canvas.create_rectangle(0, 0, width, height*0.7, fill='#f5deb3', outline='#d2b48c', width=2)
        
        # Рисуем окно с ночным небом
        self.draw_window(width, height)
        
        # Рисуем камин
        self.draw_fireplace(width, height)
        
        # Рисуем новогодние носки у камина
        self.draw_christmas_socks(width, height)
        
        # Рисуем ёлку
        self.draw_christmas_tree(width, height)
        
        # Рисуем подарки под ёлкой
        self.draw_gifts(width, height)
        
        # Рисуем электронные часы
        self.draw_digital_clock(width, height)
        
    def draw_window(self, width, height):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        # Окно с ночным небом (правая сторона)
        window_width = width * 0.2
        window_height = height * 0.25
        window_x = width * 0.7
        window_y = height * 0.1
        
        self.canvas.create_rectangle(window_x, window_y, window_x + window_width, window_y + window_height, 
                                   fill='#0a0a2a', outline='#2a2a4a', width=3)
        
        # Луна
        moon_size = min(window_width, window_height) * 0.1
        self.canvas.create_oval(window_x + window_width*0.25, window_y + window_height*0.15,
                              window_x + window_width*0.25 + moon_size, window_y + window_height*0.15 + moon_size,
                              fill='#f0f0ff', outline='#e0e0e0')
        
        # Звезды
        for _ in range(20):
            x = window_x + random.randint(10, int(window_width-20))
            y = window_y + random.randint(10, int(window_height-20))
            size = random.randint(1, 3)
            self.canvas.create_oval(x, y, x+size, y+size, fill='white', outline='')
        
        # Снег за окном
        for _ in range(30):
            x = window_x + random.randint(0, int(window_width))
            y = window_y + window_height + random.randint(0, int(height*0.3))
            size = random.randint(2, 4)
            self.canvas.create_oval(x, y, x+size, y+size, fill='white', outline='')
        
        # Рама окна
        self.canvas.create_line(window_x + window_width/2, window_y, 
                              window_x + window_width/2, window_y + window_height, 
                              fill='#8B4513', width=2)
        self.canvas.create_line(window_x, window_y + window_height/2, 
                              window_x + window_width, window_y + window_height/2, 
                              fill='#8B4513', width=2)
    
    def draw_fireplace(self, width, height):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        # Камин (левая сторона)
        fireplace_width = width * 0.15
        fireplace_height = height * 0.15
        fireplace_x = width * 0.1
        fireplace_y = height * 0.55
        
        self.canvas.create_rectangle(fireplace_x, fireplace_y, 
                                   fireplace_x + fireplace_width, fireplace_y + fireplace_height,
                                   fill='#a0522d', outline='#8B4513', width=3)
        
        # Внутренность камина
        self.canvas.create_rectangle(fireplace_x + fireplace_width*0.1, fireplace_y - fireplace_height*0.3,
                                   fireplace_x + fireplace_width*0.9, fireplace_y,
                                   fill='#2c2c2c', outline='#1a1a1a', width=2)
        
        # Огонь в камине
        self.draw_fire(fireplace_x, fireplace_y, fireplace_width)
        
        # Полка камина
        self.canvas.create_rectangle(fireplace_x - fireplace_width*0.05, fireplace_y - fireplace_height*0.3,
                                   fireplace_x + fireplace_width*1.05, fireplace_y - fireplace_height*0.25,
                                   fill='#8B4513', outline='#654321', width=2)
    
    def draw_fire(self, x, y, width):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        # Огонь в камине
        fire_colors = ['#ff4500', '#ff8c00', '#ffd700']
        fire_width = width * 0.6
        
        for i in range(3):
            y1 = y - i * (width * 0.05)
            y2 = y - i * (width * 0.03)
            self.canvas.create_polygon(
                x + width*0.2, y,
                x + width*0.3, y1,
                x + width*0.4, y2,
                x + width*0.5, y1,
                x + width*0.6, y,
                fill=fire_colors[i], outline=''
            )
    
    def draw_christmas_socks(self, width, height):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        # Новогодние носки у камина
        sock_colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00']
        fireplace_x = width * 0.1
        fireplace_width = width * 0.15
        
        for i in range(4):
            x = fireplace_x + fireplace_width + i * (width * 0.03)
            sock_height = height * 0.1
            self.canvas.create_polygon(
                x, height * 0.65,
                x + width * 0.02, height * 0.65,
                x + width * 0.02, height * 0.55,
                x + width * 0.017, height * 0.53,
                x + width * 0.003, height * 0.53,
                x, height * 0.55,
                fill=sock_colors[i], outline='black', width=1
            )
            # Украшения на носках
            self.canvas.create_oval(x + width*0.003, height*0.56, 
                                  x + width*0.012, height*0.57, 
                                  fill='white', outline='black', width=1)
    
    def draw_christmas_tree(self, width, height):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        # Ёлка (центр)
        tree_x = width * 0.5
        tree_base_y = height * 0.7
        
        # Ярусы ёлки
        tree_colors = ['#006400', '#008000', '#00a000']
        for i in range(3):
            tier_width = width * 0.15 - i * (width * 0.03)
            tier_height = height * 0.08 - i * (height * 0.015)
            y = tree_base_y - i * (height * 0.1)
            
            self.canvas.create_polygon(
                tree_x - tier_width/2, y + tier_height,
                tree_x, y,
                tree_x + tier_width/2, y + tier_height,
                fill=tree_colors[i], outline='#004400', width=2
            )
        
        # Ствол ёлки
        trunk_width = width * 0.02
        self.canvas.create_rectangle(tree_x - trunk_width/2, tree_base_y, 
                                   tree_x + trunk_width/2, tree_base_y + height*0.03,
                                   fill='#8B4513', outline='#654321', width=2)
        
        # Украшения на ёлке
        decorations = [
            (tree_x - width*0.03, tree_base_y - height*0.15, '#ff0000'),
            (tree_x + width*0.03, tree_base_y - height*0.15, '#00ff00'),
            (tree_x, tree_base_y - height*0.2, '#0000ff'),
            (tree_x - width*0.04, tree_base_y - height*0.08, '#ffff00'),
            (tree_x + width*0.04, tree_base_y - height*0.08, '#ff00ff'),
            (tree_x, tree_base_y - height*0.05, '#00ffff')
        ]
        
        for x, y, color in decorations:
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline='gold', width=1)
        
        # Звезда на верхушке
        self.canvas.create_polygon(
            tree_x, tree_base_y - height*0.25,
            tree_x - width*0.01, tree_base_y - height*0.22,
            tree_x + width*0.01, tree_base_y - height*0.22,
            fill='gold', outline='orange', width=2
        )
    
    def draw_gifts(self, width, height):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        # Подарки под ёлкой
        gift_colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff']
        gift_patterns = ['#ffffff', '#000000', '#ffff00']
        
        tree_x = width * 0.5
        tree_base_y = height * 0.7
        
        for i in range(min(self.gifts_under_tree, 6)):
            x = tree_x - width*0.08 + (i % 3) * (width * 0.04)
            y = tree_base_y + height*0.05 + (i // 3) * (height * 0.03)
            
            gift_width = width * 0.03
            gift_height = height * 0.02
            
            # Основной цвет подарка
            self.canvas.create_rectangle(x, y, x + gift_width, y + gift_height, 
                                       fill=gift_colors[i], outline='black', width=1)
            
            # Лента
            ribbon_width = gift_width * 0.2
            self.canvas.create_rectangle(x + gift_width*0.4, y, x + gift_width*0.6, y + gift_height,
                                       fill=gift_patterns[i % 3], outline='')
            self.canvas.create_rectangle(x, y + gift_height*0.4, x + gift_width, y + gift_height*0.6,
                                       fill=gift_patterns[i % 3], outline='')
            
            # Бант
            self.canvas.create_polygon(
                x + gift_width*0.5, y + gift_height*0.25,
                x + gift_width*0.4, y + gift_height*0.4,
                x + gift_width*0.5, y + gift_height*0.55,
                x + gift_width*0.6, y + gift_height*0.4,
                fill=gift_patterns[(i+1) % 3], outline='black', width=1
            )
    
    def draw_digital_clock(self, width, height):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        # Электронные часы на стене
        current_time = datetime.now()
        
        # Основание часов
        clock_width = width * 0.1
        clock_height = height * 0.05
        clock_x = width * 0.8
        clock_y = height * 0.05
        
        self.canvas.create_rectangle(clock_x, clock_y, clock_x + clock_width, clock_y + clock_height,
                                   fill='#2c2c2c', outline='#00ff00', width=2)
        
        # Время зеленым цветом
        time_str = current_time.strftime("%H:%M:%S")
        date_str = current_time.strftime("%d.%m.%Y")
        
        self.canvas.create_text(clock_x + clock_width/2, clock_y + clock_height*0.3, 
                              text=time_str, font=("Digital", int(height*0.02), "bold"), fill='#00ff00')
        self.canvas.create_text(clock_x + clock_width/2, clock_y + clock_height*0.7, 
                              text=date_str, font=("Arial", int(height*0.015), "bold"), fill='#00ff00')
    
    def update_clock(self):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        self.draw_digital_clock(width, height)
        self.window.after(1000, self.update_clock)  # Обновляем каждую секунду
    
    def add_gift(self):
        # Проверяем, не закрыто ли окно
        if self.is_closed:
            return
            
        self.gifts_under_tree += 1
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        self.draw_scene()
        
        # Анимация появления подарка
        tree_x = width * 0.5
        tree_base_y = height * 0.7
        
        for _ in range(3):
            if self.is_closed:
                break
                
            self.canvas.create_text(tree_x, tree_base_y - height*0.2, text="🎁", 
                                  font=("Arial", int(height*0.03)), fill='gold')
            self.window.update()
            time.sleep(0.2)
            self.draw_scene()
            time.sleep(0.2)

class QuestCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("Quest Calendar - Система саморазвития")
        self.root.geometry("1200x800")  # Уменьшил размер главного окна
        
        self.quests_file = "daily_quests.json"
        self.current_quest = None
        self.timer_thread = None
        self.timer_running = False
        self.current_date = datetime.now()
        self.notification_id = 0
        self.christmas_scene = None
        
        self.load_quests()
        self.create_widgets()
        self.update_calendar()
        
        self.check_active_quest()
        self.show_active_quest_notification()
    
    def load_quests(self):
        if os.path.exists(self.quests_file):
            with open(self.quests_file, 'r', encoding='utf-8') as f:
                self.quests = json.load(f)
        else:
            self.quests = {}
            current_date = datetime.now().date()
            
            quest_list = [
                "Познакомься с 3 новыми людьми", "Возьми 5 номеров у девушек/парней",
                "Сделай комплимент незнакомцу", "Пригласи кого-то на кофе",
                "Выучи 20 новых иностранных слов", "Прочитай научную статью",
                "Посмотри образовательное видео", "Реши 10 математических задач",
                "Сделай 100 отжиманий", "Пробеги 5 км", "Сходи в тренажерный зал",
                "Сделай растяжку 20 минут", "Напиши стихотворение", "Нарисуй картину",
                "Создай музыкальную композицию", "Выпей 2 литра воды",
                "Съешь 5 порций овощей/фруктов", "Спи 8 часов", "Сделай медитацию 15 минут",
                "Помоги незнакомцу", "Изучи новую профессию", "Научись готовить новое блюдо",
                "Прочитай главу из книги", "Напиши письмо самому себе в будущее",
                "Создай план на следующую неделю", "Убери в своей комнате",
                "Позвони родственнику", "Сделай доброе дело", "Найди новое хобби",
                "Разработай личный бюджет"
            ]
            
            for i in range(30):
                day_date = current_date + timedelta(days=i)
                date_str = day_date.strftime('%Y-%m-%d')
                
                self.quests[date_str] = [{
                    "quest": quest_list[i % len(quest_list)],
                    "gift": "10 баллов по всем предметам",
                    "start_date": None,
                    "end_date": None,
                    "completed": False,
                    "success": False
                }]
            
            self.save_quests()
    
    def save_quests(self):
        with open(self.quests_file, 'w', encoding='utf-8') as f:
            json.dump(self.quests, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = tk.Frame(main_frame, width=250)  # Еще уменьшил правую панель
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        right_frame.pack_propagate(False)
        
        # Уменьшил кнопку волшебства
        self.magic_button = tk.Button(
            right_frame, 
            text="🎄 Волшебная Комната", 
            command=self.open_christmas_scene,
            font=("Arial", 10, "bold"),
            bg='#4CAF50',
            fg='white',
            height=1
        )
        self.magic_button.pack(pady=8, fill=tk.X)
        
        # Уменьшил прогресс-круг
        self.progress_canvas = tk.Canvas(right_frame, width=200, height=200, bg='white')
        self.progress_canvas.pack(pady=10)
        self.progress_canvas.bind('<Button-1>', self.show_ticket)
        
        self.progress_label = tk.Label(right_frame, text="0%", font=("Arial", 14, "bold"))
        self.progress_label.pack()
        
        self.ticket_label = tk.Label(right_frame, text="", font=("Arial", 9), wraplength=200, justify=tk.CENTER)
        self.ticket_label.pack(pady=8)
        
        # Уменьшил верхнюю навигацию
        self.top_nav_frame = tk.Frame(left_frame, bg='lightblue', height=50)
        self.top_nav_frame.pack(fill=tk.X, pady=4)
        
        self.prev_month_btn = tk.Button(
            self.top_nav_frame, 
            text="←", 
            command=self.prev_month,
            font=("Arial", 12, "bold"),
            width=2,
            height=1
        )
        self.prev_month_btn.pack(side=tk.LEFT, padx=4)
        
        self.date_label = tk.Label(
            self.top_nav_frame, 
            text=self.current_date.strftime("%B %Y"),
            font=("Arial", 14, "bold"),
            bg='lightblue'
        )
        self.date_label.pack(side=tk.LEFT, expand=True)
        
        self.next_month_btn = tk.Button(
            self.top_nav_frame, 
            text="→", 
            command=self.next_month,
            font=("Arial", 12, "bold"),
            width=2,
            height=1
        )
        self.next_month_btn.pack(side=tk.RIGHT, padx=4)
        
        # Уменьшил кнопки действий
        self.action_frame = tk.Frame(left_frame, bg='lightgray', height=40)
        self.action_frame.pack(fill=tk.X, pady=4)
        
        self.accept_button = tk.Button(
            self.action_frame, 
            text="Принять задание", 
            command=self.accept_quest,
            font=("Arial", 10),
            bg='green',
            fg='white',
            height=1
        )
        self.accept_button.pack(side=tk.LEFT, padx=6, pady=3)
        
        self.complete_button = tk.Button(
            self.action_frame,
            text="Выполнено",
            command=self.complete_quest,
            font=("Arial", 10),
            bg='blue',
            fg='white',
            height=1
        )
        self.complete_button.pack(side=tk.LEFT, padx=6, pady=3)
        
        # СУЩЕСТВЕННО уменьшил календарь
        self.calendar_frame = tk.Frame(left_frame, bg='white')
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        
        # Значительно уменьшил размеры ячеек календаря
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, minsize=60)  # Было 80
        for i in range(6):
            self.calendar_frame.rowconfigure(i+1, weight=1, minsize=50)  # Было 70
        
        days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for i, day in enumerate(days_of_week):
            label = tk.Label(self.calendar_frame, text=day, font=("Arial", 9, "bold"))  # Уменьшил шрифт
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)  # Уменьшил отступы
        
        self.days = {}
        
        # Увеличил информационную панель
        self.info_frame = tk.Frame(left_frame, bg='lightyellow', height=120)
        self.info_frame.pack(fill=tk.X, pady=8)
        
        self.info_label = tk.Label(
            self.info_frame, 
            text="Выберите день для просмотра заданий",
            font=("Arial", 13, "bold"),  # Увеличил шрифт
            bg='lightyellow',
            wraplength=700,
            justify=tk.LEFT
        )
        self.info_label.pack(pady=12, padx=10, fill=tk.BOTH, expand=True)
        
        self.update_progress_circle()
    
    def open_christmas_scene(self):
        # Считаем количество выполненных заданий за ТЕКУЩИЙ месяц
        completed_count = self.count_completed_quests_current_month()
    
        # Определяем уровень "новогодности" по количеству выполненных заданий
        if completed_count <= 5:
            image_path = "christmas_1.gif"  # 1-5 подарков
        elif completed_count <= 10:
            image_path = "christmas_2.gif"  # 6-10 подарков
        elif completed_count <= 15:
            image_path = "christmas_3.gif"  # 11-15 подарков
        elif completed_count <= 20:
            image_path = "christmas_4.gif"  # 16-20 подарков
        else:
            image_path = "christmas_5.gif"  # 20+ подарков - максимально праздничная
    
        # Создаем окно для показа фото
        photo_window = tk.Toplevel(self.root)
        photo_window.title("Волшебная Новогодняя Комната")
        photo_window.geometry("1200x900")
    
        # Создаем основной фрейм для центрирования
        main_frame = tk.Frame(photo_window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
        # Пытаемся загрузить и показать изображение
        try:
            from PIL import Image, ImageTk
        
            # Открываем изображение
            image = Image.open(image_path)
        
            # Увеличиваем размер изображения
            max_width = 1000
            max_height = 700
        
            # Масштабируем изображение с сохранением пропорций
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
            # Конвертируем в PhotoImage
            photo = ImageTk.PhotoImage(image)
        
            # Создаем метку с изображением
            label = tk.Label(main_frame, image=photo)
            label.image = photo  # сохраняем ссылку
            label.pack(pady=10)
        
            # Добавляем текст с прогрессом ТЕКУЩЕГО месяца
            current_month = datetime.now().month
            current_year = datetime.now().year
            total_days = calendar.monthrange(current_year, current_month)[1]
            
            progress_label = tk.Label(
                main_frame, 
                text=f"Текущий месяц: {current_month}.{current_year}\n"
                     f"Выполнено заданий: {completed_count}/{total_days}\n"
                     f"Уровень праздника: {min((completed_count-1)//5 + 1, 5)}/5",
                font=("Arial", 16, "bold"),
                bg='white',
                justify=tk.CENTER
            )
            progress_label.pack(pady=15)
        
            # Кнопка закрытия
            close_button = tk.Button(
                main_frame,
                text="Закрыть",
                command=photo_window.destroy,
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                width=15,
                height=2
            )
            close_button.pack(pady=10)
        
        except ImportError:
            # Если PIL не установлен, показываем текстовое представление
            current_month = datetime.now().month
            current_year = datetime.now().year
            total_days = calendar.monthrange(current_year, current_month)[1]
            
            label = tk.Label(
                main_frame, 
                text=f"🎄 Волшебная комната 🎄\n\n"
                     f"Текущий месяц: {current_month}.{current_year}\n"
                     f"Выполнено заданий: {completed_count}/{total_days}\n\n"
                     f"Уровень праздника: {min((completed_count-1)//5 + 1, 5)}/5\n\n"
                     f"(Установите PIL для показа изображений: pip install pillow)",
                font=("Arial", 18),
                justify=tk.CENTER
            )
            label.pack(expand=True, pady=20)
        
            close_button = tk.Button(
                main_frame,
                text="Закрыть",
                command=photo_window.destroy,
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                width=15,
                height=2
            )
            close_button.pack(pady=20)
    
        except FileNotFoundError:
            current_month = datetime.now().month
            current_year = datetime.now().year
            total_days = calendar.monthrange(current_year, current_month)[1]
            
            label = tk.Label(
                main_frame, 
                text=f"Изображение {image_path} не найдено!\n\n"
                     f"Текущий месяц: {current_month}.{current_year}\n"
                     f"Выполнено заданий: {completed_count}/{total_days}",
                font=("Arial", 16),
                fg='red',
                justify=tk.CENTER
            )
            label.pack(expand=True, pady=20)
        
            close_button = tk.Button(
                main_frame,
                text="Закрыть",
                command=photo_window.destroy,
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                width=15,
                height=2
            )
            close_button.pack(pady=20)
    
    def count_completed_quests_current_month(self):
        """Считает выполненные задания за ТЕКУЩИЙ месяц"""
        count = 0
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        for date_str, quests in self.quests.items():
            try:
                quest_date = datetime.strptime(date_str, '%Y-%m-%d')
                # Проверяем, что задание относится к текущему месяцу и году
                if quest_date.month == current_month and quest_date.year == current_year:
                    for quest in quests:
                        if quest['completed'] and quest['success']:
                            count += 1
            except ValueError:
                continue
        return count
    
    def count_completed_quests(self):
        """Считает ВСЕ выполненные задания (для обратной совместимости)"""
        count = 0
        for date_str, quests in self.quests.items():
            for quest in quests:
                if quest['completed'] and quest['success']:
                    count += 1
        return count
    
    def update_progress_circle(self):
        self.progress_canvas.delete("all")
        
        month_start = date(self.current_date.year, self.current_date.month, 1)
        if self.current_date.month == 12:
            month_end = date(self.current_date.year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(self.current_date.year, self.current_date.month + 1, 1) - timedelta(days=1)
        
        total_days = (month_end - month_start).days + 1
        completed_days = 0
        
        current_date_obj = month_start
        while current_date_obj <= month_end:
            date_str = current_date_obj.strftime('%Y-%m-%d')
            if date_str in self.quests:
                quest = self.quests[date_str][0]
                if quest['completed'] and quest['success']:
                    completed_days += 1
            current_date_obj += timedelta(days=1)
        
        progress_percent = (completed_days / total_days) * 100 if total_days > 0 else 0
        
        center_x, center_y = 100, 100  # Уменьшил центр для меньшего круга
        radius = 80  # Уменьшил радиус
        
        self.progress_canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline="gray", width=2, fill="white"  # Уменьшил ширину обводки
        )
        
        if progress_percent > 0:
            angle = 360 * progress_percent / 100
            self.progress_canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=90, extent=-angle,
                outline="green", width=3, fill="green", style=tk.ARC  # Уменьшил ширину
            )
        
        self.progress_label.config(text=f"{progress_percent:.1f}%")
        
        return progress_percent
    
    def show_ticket(self, event):
        progress = self.update_progress_circle()
        if progress >= 100:
            self.ticket_label.config(
                text="🎫 Билет на 10 баллов по всем предметам!\nПоздравляем! Вы выполнили все задания за месяц!",
                font=("Arial", 10, "bold"),
                fg="green"
            )
        else:
            self.ticket_label.config(
                text=f"Выполнено {progress:.1f}% заданий за месяц\nВыполните все задания месяца для получения билета",
                font=("Arial", 9),
                fg="black"
            )
    
    def update_calendar(self):
        for widget in self.calendar_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        today = datetime.now().date()
        self.days = {}
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue
                
                day_date = date(self.current_date.year, self.current_date.month, day)
                date_str = day_date.strftime('%Y-%m-%d')
                
                # СУЩЕСТВЕННО уменьшил фреймы дней
                frame = tk.Frame(self.calendar_frame, relief=tk.RAISED, borderwidth=1, width=60, height=50)
                frame.grid(row=week_num+1, column=day_num, padx=1, pady=1, sticky="nsew")
                frame.grid_propagate(False)
                
                # Определяем цвет фона
                bg_color = 'white'
                if day_date == today:
                    bg_color = 'gold'  # Сегодняшний день
                elif date_str in self.quests:
                    quest = self.quests[date_str][0]
                    if quest['completed']:
                        bg_color = 'green' if quest['success'] else 'red'  # Выполнено успешно/неуспешно
                    elif day_date < today:
                        bg_color = 'red'  # ПРОШЕДШИЙ день с невыполненным заданием
                
                # Уменьшил шрифт числа
                day_label = tk.Label(frame, text=str(day), font=("Arial", 9))  # Уменьшил шрифт
                day_label.pack(anchor='nw', padx=2, pady=2)  # Уменьшил отступы
                
                # Уменьшил шрифт статуса
                status_label = tk.Label(frame, text="", font=("Arial", 7))
                status_label.pack()
                
                if date_str in self.quests:
                    quest = self.quests[date_str][0]
                    if quest['completed']:
                        status_label.config(text="✓" if quest['success'] else "✗")
                    elif day_date < today:
                        status_label.config(text="✗")  # Показываем крестик для невыполненных заданий в прошлом
                
                frame.config(bg=bg_color)
                
                if day_date <= datetime.now().date():
                    frame.bind('<Button-1>', lambda e, d=date_str: self.show_day_quests(d))
                    day_label.bind('<Button-1>', lambda e, d=date_str: self.show_day_quests(d))
                    status_label.bind('<Button-1>', lambda e, d=date_str: self.show_day_quests(d))
                
                self.days[date_str] = {
                    'frame': frame,
                    'status': status_label
                }
        
        self.date_label.config(text=self.current_date.strftime("%B %Y").capitalize())
        self.update_progress_circle()
    
    def show_day_quests(self, date_str):
        try:
            quest_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if quest_date > datetime.now().date():
                self.info_label.config(text="Нельзя выполнять задания из будущего!")
                return
            
            quests = self.quests.get(date_str, [])
            if not quests:
                self.info_label.config(text=f"{date_str}: Нет заданий на этот день")
                return
            
            quest = quests[0]
            info_text = f"Задание на {date_str}:\n{quest['quest']}\n\n"
            
            if quest['completed']:
                status = "✓ Выполнено успешно" if quest['success'] else "✗ Не выполнено в срок"
                info_text += f"Статус: {status}\n"
                if quest['start_date']:
                    info_text += f"Начало: {quest['start_date']}\n"
                if quest['end_date']:
                    info_text += f"Окончание: {quest['end_date']}\n"
            else:
                if quest_date < datetime.now().date():
                    info_text += "Статус: ✗ НЕ ВЫПОЛНЕНО (просрочено)\n"
                else:
                    info_text += "Статус: Не начато\n"
                    info_text += "Можно принять задание только на сегодня!"
            
            self.info_label.config(text=info_text)
        except Exception as e:
            self.info_label.config(text=f"Ошибка: {str(e)}")
    
    def prev_month(self):
        self.current_date = self.current_date.replace(day=1)
        self.current_date -= timedelta(days=1)
        self.current_date = self.current_date.replace(day=1)
        self.update_calendar()
    
    def next_month(self):
        self.current_date = self.current_date.replace(day=28)
        self.current_date += timedelta(days=7)
        self.current_date = self.current_date.replace(day=1)
        self.update_calendar()
    
    def accept_quest(self):
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        if today_str not in self.quests:
            messagebox.showinfo("Информация", "Нет заданий на сегодня!")
            return
        
        quest = self.quests[today_str][0]
        
        if quest['completed']:
            messagebox.showinfo("Информация", "Задание на сегодня уже выполнено!")
            return
        
        if quest['start_date']:
            messagebox.showwarning("Внимание", "Задание на сегодня уже начато!")
            return
        
        result = messagebox.askyesno(
            "Принять задание", 
            f"Задание на сегодня:\n{quest['quest']}\n\nНаграда: {quest['gift']}\n\nПринять задание?"
        )
        
        if result:
            start_time = datetime.now()
            quest['start_date'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            quest['end_date'] = (start_time + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
            self.current_quest = quest
            
            self.save_quests()
            self.update_calendar()
            self.start_timer()
            self.show_active_quest_notification()
            
            messagebox.showinfo("Успех", "Задание принято! У вас 24 часа на выполнение.")
    
    def complete_quest(self):
        if not self.current_quest:
            messagebox.showinfo("Ошибка", "Нет активного задания!")
            return
        
        end_time = datetime.now()
        start_time = datetime.strptime(self.current_quest['start_date'], '%Y-%m-%d %H:%M:%S')
        
        time_taken = end_time - start_time
        success = time_taken.total_seconds() <= 24 * 3600
        
        self.current_quest['completed'] = True
        self.current_quest['success'] = success
        
        self.save_quests()
        self.update_calendar()
        self.stop_timer()
        
        if success:
            messagebox.showinfo("Поздравляем!", 
                               f"Вы успешно выполнили задание!\nВремя: {str(time_taken).split('.')[0]}\n"
                               f"Награда: {self.current_quest['gift']}")
            
            # Добавляем подарок в волшебную комнату, если она открыта
            if self.christmas_scene and not self.christmas_scene.is_closed:
                self.christmas_scene.add_gift()
        else:
            messagebox.showwarning("Время вышло", 
                                  "Вы не успели выполнить задание в срок!")
        
        self.current_quest = None
        self.notification_id += 1
    
    def start_timer(self):
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.timer_countdown)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def stop_timer(self):
        self.timer_running = False
    
    def timer_countdown(self):
        current_notification_id = self.notification_id
        
        while (self.timer_running and self.current_quest and 
               current_notification_id == self.notification_id):
            
            end_time = datetime.strptime(self.current_quest['end_date'], '%Y-%m-%d %H:%M:%S')
            remaining = end_time - datetime.now()
            
            if remaining.total_seconds() <= 0:
                self.stop_timer()
                self.show_notification("Время вышло!", "Время на выполнение задания истекло!", is_urgent=True)
                break
            
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            is_urgent = hours == 0 and minutes < 30
            
            self.show_active_quest_notification_countdown(
                hours, minutes, seconds, is_urgent, current_notification_id
            )
            
            time.sleep(1)
    
    def show_active_quest_notification(self):
        if self.current_quest:
            end_time = datetime.strptime(self.current_quest['end_date'], '%Y-%m-%d %H:%M:%S')
            remaining = end_time - datetime.now()
            
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            is_urgent = hours == 0 and minutes < 30
            
            self.show_active_quest_notification_countdown(
                hours, minutes, seconds, is_urgent, self.notification_id
            )
    
    def show_active_quest_notification_countdown(self, hours, minutes, seconds, is_urgent, notification_id):
        if (self.current_quest and self.timer_running and 
            notification_id == self.notification_id):
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            title = "⏰ СРОЧНО! " if is_urgent else "📝 Активное задание"
            
            try:
                notification.notify(
                    title=title,
                    message=f"{self.current_quest['quest']}\nОсталось: {time_str}",
                    timeout=1,
                    app_name="Quest Calendar"
                )
            except Exception as e:
                print(f"{title}: {self.current_quest['quest']}")
                print(f"Осталось времени: {time_str}")
                if is_urgent:
                    print("⚠️  СРОЧНО! Менее 30 минут осталось!")
    
    def show_notification(self, title, message, is_urgent=False):
        try:
            notification.notify(
                title="⚠️ " + title if is_urgent else title,
                message=message,
                timeout=10,
                app_name="Quest Calendar"
            )
        except Exception as e:
            print(f"{title}: {message}")
    
    def check_active_quest(self):
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        if today_str in self.quests:
            quest = self.quests[today_str][0]
            if quest['start_date'] and not quest['completed']:
                start_time = datetime.strptime(quest['start_date'], '%Y-%m-%d %H:%M:%S')
                end_time = datetime.strptime(quest['end_date'], '%Y-%m-%d %H:%M:%S')
                
                if datetime.now() < end_time:
                    self.current_quest = quest
                    self.start_timer()
                else:
                    quest['completed'] = True
                    quest['success'] = False
                    self.save_quests()

def main():
    root = tk.Tk()
    app = QuestCalendar(root)
    root.mainloop()

if __name__ == "__main__":
    main()
