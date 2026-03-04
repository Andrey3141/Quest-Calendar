import os
from PIL import Image

def create_gif_from_images(images_folder, output_gif, duration=500, loop=0):
    """
    Создает GIF анимацию из набора изображений
    
    Args:
        images_folder (str): Папка с изображениями
        output_gif (str): Имя выходного GIF-файла
        duration (int): Длительность каждого кадра в миллисекундах
        loop (int): Количество циклов (0 = бесконечный)
    """
    try:
        # Получаем список всех изображений в папке
        image_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff']:
            image_files.extend([f for f in os.listdir(images_folder) if f.lower().endswith(ext[1:])])
        
        if not image_files:
            print("В папке нет изображений!")
            return False
        
        # Сортируем файлы по имени
        image_files.sort()
        
        print(f"Найдено {len(image_files)} изображений:")
        for img in image_files:
            print(f"  - {img}")
        
        # Загружаем все изображения
        frames = []
        for image_file in image_files:
            image_path = os.path.join(images_folder, image_file)
            try:
                img = Image.open(image_path)
                
                # Конвертируем в RGB если нужно (GIF не поддерживает RGBA)
                if img.mode in ('RGBA', 'LA'):
                    # Создаем белый фон для прозрачных изображений
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])  # Используем альфа-канал как маску
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                frames.append(img)
                print(f"Загружено: {image_file} ({img.size[0]}x{img.size[1]})")
                
            except Exception as e:
                print(f"Ошибка загрузки {image_file}: {e}")
        
        if not frames:
            print("Не удалось загрузить ни одного изображения!")
            return False
        
        # Сохраняем как GIF
        frames[0].save(
            output_gif,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop,
            optimize=True
        )
        
        print(f"\n✅ GIF успешно создан: {output_gif}")
        print(f"📊 Кадров: {len(frames)}")
        print(f"⏱️  Длительность кадра: {duration} ms")
        print(f"🔄 Циклов: {'бесконечно' if loop == 0 else loop}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании GIF: {e}")
        return False

def create_gif_with_custom_order(image_paths, output_gif, duration=500, loop=0):
    """
    Создает GIF из конкретных изображений в указанном порядке
    
    Args:
        image_paths (list): Список путей к изображениям
        output_gif (str): Имя выходного GIF-файла
        duration (int): Длительность каждого кадра в миллисекундах
        loop (int): Количество циклов
    """
    try:
        frames = []
        
        for image_path in image_paths:
            if not os.path.exists(image_path):
                print(f"Файл не найден: {image_path}")
                continue
                
            img = Image.open(image_path)
            
            # Конвертируем в RGB если нужно
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            frames.append(img)
            print(f"Загружено: {os.path.basename(image_path)}")
        
        if not frames:
            print("Нет изображений для создания GIF!")
            return False
        
        # Сохраняем GIF
        frames[0].save(
            output_gif,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop,
            optimize=True
        )
        
        print(f"✅ GIF создан: {output_gif}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def resize_images_for_gif(images_folder, target_size=(800, 600)):
    """
    Изменяет размер всех изображений для одинакового размера в GIF
    
    Args:
        images_folder (str): Папка с изображениями
        target_size (tuple): Целевой размер (width, height)
    """
    try:
        image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            print("Нет изображений для изменения размера!")
            return
        
        print(f"Изменение размера {len(image_files)} изображений до {target_size[0]}x{target_size[1]}...")
        
        for image_file in image_files:
            image_path = os.path.join(images_folder, image_file)
            img = Image.open(image_path)
            
            # Изменяем размер с сохранением пропорций
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Создаем новое изображение нужного размера с белым фоном
            new_img = Image.new('RGB', target_size, (255, 255, 255))
            
            # Центрируем изображение
            x = (target_size[0] - img.size[0]) // 2
            y = (target_size[1] - img.size[1]) // 2
            new_img.paste(img, (x, y))
            
            # Сохраняем обратно
            new_img.save(image_path)
            print(f"Изменен размер: {image_file}")
            
    except Exception as e:
        print(f"Ошибка изменения размера: {e}")

def main():
    """
    Основная функция с меню выбора
    """
    print("🎄 Создание новогодней GIF-анимации 🎄")
    print("=" * 40)
    
    while True:
        print("\nВыберите действие:")
        print("1. Создать GIF из всех изображений в папке")
        print("2. Создать GIF из конкретных файлов")
        print("3. Изменить размер изображений для GIF")
        print("4. Выход")
        
        choice = input("Ваш выбор (1-4): ").strip()
        
        if choice == '1':
            folder = input("Введите путь к папке с изображениями: ").strip()
            if not os.path.exists(folder):
                print("Папка не существует!")
                continue
                
            output_name = input("Введите имя выходного GIF-файла (например: christmas.gif): ").strip()
            if not output_name.endswith('.gif'):
                output_name += '.gif'
                
            try:
                duration = int(input("Длительность кадра в миллисекундах (по умолчанию 500): ") or "500")
                loop = int(input("Количество циклов (0 = бесконечно): ") or "0")
            except ValueError:
                print("Использую значения по умолчанию")
                duration = 500
                loop = 0
                
            create_gif_from_images(folder, output_name, duration, loop)
            
        elif choice == '2':
            files = input("Введите пути к файлам через запятую: ").split(',')
            files = [f.strip() for f in files if f.strip()]
            
            if not files:
                print("Не указаны файлы!")
                continue
                
            output_name = input("Введите имя выходного GIF-файла: ").strip()
            if not output_name.endswith('.gif'):
                output_name += '.gif'
                
            try:
                duration = int(input("Длительность кадра в миллисекундах: ") or "500")
                loop = int(input("Количество циклов (0 = бесконечно): ") or "0")
            except ValueError:
                duration = 500
                loop = 0
                
            create_gif_with_custom_order(files, output_name, duration, loop)
            
        elif choice == '3':
            folder = input("Введите путь к папке с изображениями: ").strip()
            if not os.path.exists(folder):
                print("Папка не существует!")
                continue
                
            try:
                width = int(input("Ширина (по умолчанию 800): ") or "800")
                height = int(input("Высота (по умолчанию 600): ") or "600")
                resize_images_for_gif(folder, (width, height))
            except ValueError:
                print("Использую размер 800x600")
                resize_images_for_gif(folder)
                
        elif choice == '4':
            print("До свидания! 🎅")
            break
            
        else:
            print("Неверный выбор! Попробуйте снова.")

# Простой вызов для быстрого создания GIF
def quick_create_gif():
    """
    Быстрое создание GIF из 3 изображений
    """
    # Предполагаем, что изображения называются christmas_1.png, christmas_2.png, christmas_3.png
    image_files = ["1/1.jpg", "1/2.jpg", "1/3.jpg"]
    
    # Проверяем, что файлы существуют
    existing_files = [f for f in image_files if os.path.exists(f)]
    
    if len(existing_files) < 2:
        print("Нужно как минимум 2 изображения для создания GIF!")
        print("Убедитесь, что файлы christmas_1.png, christmas_2.png, christmas_3.png существуют")
        return
    
    print("Создаем GIF из изображений:")
    for f in existing_files:
        print(f"  - {f}")
    
    output_gif = "new_year_animation.gif"
    
    if create_gif_with_custom_order(existing_files, output_gif, duration=300, loop=0):
        print(f"\n🎉 Новогодний GIF готов: {output_gif}")
    else:
        print("❌ Не удалось создать GIF")

if __name__ == "__main__":
    # Для быстрого создания GIF из 3 изображений:
    quick_create_gif()
    
    # Для интерактивного режима раскомментируйте следующую строку:
    # main()
