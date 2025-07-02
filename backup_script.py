import os

# Указание пути к git.exe (если Git не в PATH)
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = r"C:\Program Files\Git\bin\git.exe"

import time
import datetime
import git
import schedule

# Путь к отслеживаемой директории
WATCHED_FOLDER = "backup_folder"

# Путь к текущему Git-репозиторию
GIT_REPO_PATH = os.getcwd()

def backup_and_commit():
    repo = git.Repo(GIT_REPO_PATH)

    # Добавление всех файлов в Git-индекс
    repo.git.add(A=True)

    # Формирование коммита с текущим временем
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"Backup at {now}"
    repo.index.commit(commit_message)

    # Сохраняем в лог-файл
    with open("backup_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(commit_message + "\n")

    # Печатаем сообщение в консоль
    print(commit_message)

    # Попытка push в GitHub (если есть origin)
    try:
        origin = repo.remote(name='origin')
        origin.push()
        print("Изменения успешно отправлены в удалённый репозиторий.")
    except Exception as e:
        print("Ошибка при push:", e)

# Планировщик — каждые 10 минут
schedule.every(10).minutes.do(backup_and_commit)

print("Служба резервного копирования запущена. Для остановки нажмите Ctrl+C.")

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nРабота программы прервана пользователем. Завершение...")
