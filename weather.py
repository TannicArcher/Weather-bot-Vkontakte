import vk_api
from pyowm import OWM

# Введите токен вашего бота Вконтакте
TOKEN = 'YOUR_VK_BOT_TOKEN'

# Введите токен вашего аккаунта OpenWeatherMap
OWM_TOKEN = 'YOUR_OPENWEATHERMAP_TOKEN'

# Создание сессии Вконтакте
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# Создание объекта OpenWeatherMap
owm = OWM(OWM_TOKEN)

# Функция для получения погоды в столице указанной страны
def get_weather(country):
    try:
        # Получение информации о столице
        capitals = {
            'Россия': 'Moscow',
            'США': 'Washington',
            'Великобритания': 'London',
            # Добавьте другие страны и столицы по желанию
        }
        capital = capitals.get(country)

        if capital:
            # Получение погоды в столице
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(f"{capital}, {country}")
            weather = observation.weather

            # Возвращаем строку с информацией о погоде
            return f"Погода в {capital}, {country}: {weather.temperature('celsius')['temp']}°C, {weather.status}"
        else:
            return "Столица не найдена"
    except Exception as e:
        return f"Ошибка при получении погоды: {str(e)}"

# Функция для обработки сообщений
def process_message(event):
    if event['type'] == 'message_new':
        message = event['object']['message']
        text = message['text'].lower()

        # Обработка команды "погода"
        if text == 'погода':
            user_id = message['from_id']
            country = "Россия"  # Здесь можно запросить у пользователя страну

            # Получение погоды в столице указанной страны
            weather = get_weather(country)

            # Отправка сообщения с погодой пользователю
            vk.messages.send(user_id=user_id, message=weather, random_id=0)

# Основной цикл обработки сообщений
longpoll = vk_api.longpoll.VkLongPoll(vk_session)
for event in longpoll.listen():
    process_message(event)
