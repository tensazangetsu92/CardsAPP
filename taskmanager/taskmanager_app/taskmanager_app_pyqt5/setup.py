import os
from pathlib import Path

from cx_Freeze import setup, Executable

# Определите базовую директорию
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Определите относительные пути для основного файла и иконки
main_script = os.path.join(BASE_DIR, "taskmanager_app", "taskmanager_app_pyqt5", "app.py")
icon_path = os.path.join(BASE_DIR, "taskmanager_app", "static", "images", "CA.ico")

# Определите параметры сборки
build_exe_options = {
    "packages": [],  # Укажите дополнительные пакеты, если нужно
    "include_files": ['C:\\Users\\alex\\PycharmProjects\\TaskManager\\taskmanager\\taskmanager_app\\static']  # Укажите файлы, которые нужно включить (например, изображения)
}

# Укажите параметры приложения
setup(
    name="CardsAPP",
    version="0.1",
    description="",
    options={"build_exe": build_exe_options},
    executables=[Executable(main_script,
                            target_name="CardsAPP.exe",
                            base="Win32GUI",
                            icon=icon_path)]  # Укажите ваш основной файл
)
