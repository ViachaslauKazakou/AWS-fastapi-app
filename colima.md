Вот инструкция в формате `colima.md` – её можно использовать как Markdown-файл (`colima.md`) для документации:

---

````markdown
# 🚀 Установка и настройка Colima (альтернатива Docker Desktop на macOS)

Colima — это лёгкая альтернатива Docker Desktop, которая позволяет запускать контейнеры с использованием Docker CLI на Mac без необходимости установки проприетарного Docker Desktop.

---

## 🧰 Установка

### 1. Установите необходимые инструменты:

```bash
brew install colima docker
````

> ❗ `docker` — это только CLI. Демон (dockerd) будет запускаться внутри виртуальной машины, управляемой Colima.

---

## ▶️ Запуск Colima

### Первый запуск:

```bash
colima start
```

Можно указать настройки ресурсов:

```bash
colima start --cpu 4 --memory 4 --disk 60
```

Проверить статус:

```bash
colima status
```

---

## ✅ Проверка работы Docker CLI

После запуска Colima проверь, работает ли `docker`:

```bash
docker info
```

Ожидаемый результат: информация о docker engine внутри Colima VM.

---

## ⚠️ Распространённые ошибки и их решение

### ❌ `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`

**Причина:** Colima не запущен или не может подключить `dockerd`.

**Решение:**

```bash
colima start
```

---

### ❌ `FATA[...] error starting vm: error at 'creating and starting': exit status 1`

**Причина:** Повреждённая VM или конфликт запуска.

**Решение:**

1. Остановите и удалите виртуалку:

```bash
colima stop
colima delete
```

2. Если не помогает — принудительно удалите через Lima:

```bash
limactl delete colima
```

3. Запустите заново:

```bash
colima start
```

---

### ❌ `Timed out waiting for the Activation Lock Capable check`

**Причина:** системная утилита macOS `system_profiler` долго отвечает. Это **не ошибка**, можно игнорировать.

---

### ❌ Использование `brew services start colima`

**Не используйте `brew services` с Colima**:

```bash
brew services stop colima
```

Colima не предназначен для работы как `launchd`-демон. Запускайте вручную.

---

## 🔁 Автозапуск Colima (опционально)

Добавьте в `~/.zshrc` или `~/.bash_profile`, чтобы Colima запускался при открытии терминала:

```bash
if ! colima status | grep -q "Running"; then
  colima start
fi
```

---

## 🧪 Тест

Простой тест запуска контейнера:

```bash
docker run hello-world
```

---

## 📦 Поддержка Docker Compose

Colima полностью совместим с `docker-compose`, если он установлен:

```bash
brew install docker-compose
```

Пример запуска:

```bash
docker-compose up
```

---

## 📚 Полезные команды

| Команда         | Назначение                    |
| --------------- | ----------------------------- |
| `colima start`  | Запустить виртуалку           |
| `colima stop`   | Остановить виртуалку          |
| `colima delete` | Удалить виртуалку             |
| `colima status` | Статус виртуалки              |
| `docker info`   | Информация о Docker           |
| `docker ps`     | Список запущенных контейнеров |

---

## 🔗 Полезные ссылки

* [Colima GitHub](https://github.com/abiosoft/colima)
* [Lima GitHub](https://github.com/lima-vm/lima)
* [Docker CLI](https://docs.docker.com/engine/reference/commandline/cli/)

---

```

--- 

Хочешь — могу сохранить этот файл как `colima.md` и выдать тебе ссылку для скачивания.
```
