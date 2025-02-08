# Telegram Bot Astrology

## Установите git
```bash
sudo apt install git
```

## Скопируем репозиторий
```bash
git clone https://github.com/ivalukyan/astrobot.git
```

## Перейдем в склонированный репозиторий
```bash
cd astrobot
```

## Установим докер зависимость
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Добавим файл с переменными окружения
```bash
vim .env
```

```
BOT_TOKEN=

# Через запятую перечислить telegram id 
ADMINS=[]
```

## Создадите сервисный аккаунт в Google Console
`
https://console.cloud.google.com/iam-admin/serviceaccounts?project=singular-cache-450120-i9
`  
Нажмите справа на 3 точки и добавьте ключ. Получите его в виде JSON.  
Полученный JSON переименуйте в cred.json и добавьте в папку в проекте `files`

## Настройка доступа для Google Sheets
Создайте новую таблицу google sheets, в первые колонки добавьте по образцу названия столбцов.
Перейдите в настройки доступа и добавьте сервисный аккаунт.


## Зупустим Docker контейнеры
```bash
docker compose -f ./docker/docker-compose.yml up -d --build
```


## Команды
Чтобы запустить бота напишите `/start`  
Чтобы перейти в меню админа `/admin`
