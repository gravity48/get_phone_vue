<template>
  <ul id="version-description-list">
    <li>
      <div class="version-name">Версия <span>1.0.0</span></div>
      <div class="version-description">
        <h5>Frontend: </h5>
        <ul class="version-functions">
          <li>Frontend проекта перенесен на фреймворк Vue3</li>
        </ul>
        <h5>Backend: </h5>
        <ul class="version-functions">
          <li>Разработан REST API приложения</li>
        </ul>
        <h5>Server: </h5>
        <ul class="version-functions">
          <li>Разработан сервер извлечения именнованных сущностей и API для взаимодействия</li>
          <li>Перенесена база данных проекта на СУБД PostgreSQL</li>
        </ul>
      </div>
    </li>
    <li>
      <div class="version-name">Версия <span>1.0.1</span> - <span>1.1.0</span></div>
      <div class="version-description">
        <h5>Frontend: </h5>
        <ul class="version-functions">
          <li>Добавлена возможность получать данные с предыдущего запроса</li>
          <li>Для каждого найденного номера проработана отдельная часть страницы с собственным пагинатором</li>
        </ul>
        <h5>Backend: </h5>
        <ul class="version-functions">
          <li>Добавлена возможность запуска одновременно нескольких обработчиков</li>
          <li>Исправлена ошибка по созданию не привелигированных пользователей</li>
          <li>Реализовано отображение телефонных номеров по запросу</li>
        </ul>
        <h5>Server: </h5>
        <ul class="version-functions">
          <li>Проработано расширенное логирование, что позволило отслеживать статус проекта в режиме реального
            времени
          </li>
          <li>Перенесена база данных проекта на СУБД PostgreSQL</li>
          <li>Настройки сервера перенесены в отдельный конфигурационный файл</li>
          <li>Все модули сервера переработаны в виде отдельных пакетов</li>
        </ul>
      </div>
    </li>
    <li>
      <div class="version-name">Версия <span>1.1.2</span> - <span>1.1.3</span></div>
      <div class="version-description">
        <h5>Frontend: </h5>
        <ul class="version-functions">
          <li>Удалена возможность ручной установки даты документа из-за ненадобности</li>
          <li>Отображение версий осуществляется от последней к первой</li>
        </ul>
        <h5>Server: </h5>
        <ul class="version-functions">
          <li>Исправлена ошибка AttributeError, возникающая, если документ поступающий на вход пустой</li>
          <li>При добавлении нового файла в базу данных, статус документа изменен на UNDERWAY(в обработке)</li>
        </ul>
      </div>
    </li>
    <li>
      <div class="version-name">Версия <span>1.1.4</span></div>
      <div class="version-description">
        <h5>Server: </h5>
        <ul class="version-functions">
          <li>Для обработки xls xlsx файлов добавлена программа XlsReader написанная на C# и фреймворке .NET CORE</li>
          <li>Переработана структура кода текстовых обработчиков, для взаимодейтсвия с которым добавлен класс
            ExtractTextFactory
          </li>
          <li>При запуске процессов изменен лимит с RLIMIT_AS на RLIMIT_DATA</li>
        </ul>
      </div>
    </li>
    <li>
      <div class="version-name">Версия <span>1.1.5</span> - <span>1.1.6</span></div>
      <div class="version-description">
        <h5>Server: </h5>
        <ul class="version-functions">
          <li>В модуль dochandler добавлен класс ProcessFuncHandler, реализующий извлечение текста в отдельном процессе,
            что позволило накладывать ограничение на потребление памяти
          </li>
          <li>
            При экстренном завершении процесса добавлен вызов метода join
          </li>
          <li>
            Повышена стабильность работы системы
          </li>
        </ul>
      </div>
    </li>
    <li>
      <div class="version-name">Версия <span>1.1.7</span></div>
      <div class="version-description">
        <h5>Server: </h5>
        <ul class="version-functions">
          <li> Переработан модуль логирования
          </li>
          <li>
            Добавлен новый класс InfinityProcessTimeout, осуществляющий перезапуск функции по таймауту
          </li>
          <li>При "экстренной" остановке процессов вызывается метод join, с целью их корректного завешения</li>
        </ul>
      </div>
    </li>
    <li>
      <div class="version-name">Версия <span>1.1.8</span></div>
      <div class="version-description">
        <h5>Frontend: </h5>
        <ul class="version-functions">
          <li>Добавлен перенос слов при отображении результатов просмотра телефонов</li>
        </ul>
        <h5>Server: </h5>
        <ul class="version-functions">
          <li>Добавлено debug логирование в рабочие процессы</li>
        </ul>
      </div>
    </li>
  </ul>
</template>

<script>

export default {
  name: "ProgramDescription",
}
</script>


<style scoped>

h5 {
  margin: 0 0 0 20px;
  font-size: 18px;
  font-weight: bold;
}

#version-description-list {
  list-style-type: none;
  margin-left: 20px !important;
  margin-top: 20px;
  display: flex;
  flex-direction: column-reverse;
}

#version-description-list > li {
  margin-top: 10px;
}

.version-functions {
  margin-left: 40px;
  font-size: 18px;
  list-style-type: none;
}

.version-name {
  font-size: 20px;
}


.version-name span {
  font-weight: bold;
}

.version-functions li:before {
  content: '\2713';
  margin-right: 5px;
  font-weight: 900;
  color: #00c853;
  font-size: 18px;
}

</style>
