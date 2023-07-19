# WhatsApp Direct Message Bot

*Данный Telegram бот позволяет написать любому пользователю WhatsApp в директ, зная лишь номер телефона и не добавляя пользователя в контакты, путём генерации прямой ссылки формата [https://wa.me/<phone_number>](https://wa.me/<phone_number>)*
***

### *Установка*

1. Установить на хосте Git и Docker
2. Зарегестрировать нового телеграм бота (*о том как это сделать можно прочесть [здесь](https://tlgrm.ru/docs/bots#botfather)*)
   
3. Скачать данный репозиторий на конечный хост, выполнив команду:
   ```shell
   git clone https://github.com/nikohakerinc/WA_direct_message_Bot.git
   
4. В __dockerfile__ заменить <YOUR_TELEGRAM_BOT_TOKEN> на токен полученный от [@BotFather](https://t.me/Botfather)
   
5. Собрать контейнер Docker:
   ```shell
   docker build -t tg_bot .
6. Запустить контйенер Docker:
   ```shell
   docker run --restart=always -d tg_bot