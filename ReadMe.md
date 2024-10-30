# Инструкция по запуску
`python -m venv venv` - создание виртуальной среды
## Windows
`venv\Scripts\activate` - активация виртуальной среды
## Linux
`source venv/bin/activate` - активация виртуальной среды
`pip install -r requirements` - установка зависимостей
`uvicorn link_shortener:app` - запуск сервера

# Инструкция по тестированию

`POST http://127.0.0.1:8000/shorten body:{url:<your_url>}` - отправка ссылки для сокращения
