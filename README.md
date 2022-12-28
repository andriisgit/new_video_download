# new_video_download

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)

## Завантаження відео з обраних ютубканалів
#### Через те що російські агресори цілеспрямовано руйнують мирну інфраструктуру України, часто доводиться сидіти без світла і без зв'язку. Цей скріпт автоматизує завантаження відео, даючи можливість дивитись скачені відео без інтернета, поки тримає батарея ноутбука 

Скріпт сканує задані ютубканали на наявність нових відео і завантажує їх в підкаталог Videos.

- При запуску зазначаєтся дата, з якої завантажувати
- GUI побудовано на кросплатформовому Qt

## Використані технології

Написано на Python3, GUI побудовано на PyQt5.
Використані сторонні бібліотеки, окрім стандартних:

- [PyQt5](https://doc.qt.io/qt-5/) - для побудови графічного інтерфейса
- [requests](https://requests.readthedocs.io) - для отримання переліку відео з канала
- [bs4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) - для парсинга переліку відео з канала
- [youtube_dl](https://github.com/ytdl-org/youtube-dl/) - для завантаження відеофайла

## Встановлення

Використовувалася версія Python 3.8.

1) рекомендується використовувати віртуальне середовище, наприклад назвати його `new_video_downloader`

```sh
python3 -m venv new_video_downloader
cd new_video_downloader
```

2) завантажити скрипт

```sh
git clone https://github.com/andriisgit/new_video_download.git
```

3) активувати віртуальне середовище

для Gnu/Linux:
```sh
source bin/activate
```

для Windows:
```sh
Scripts\activate.bat
```

4) встановити необхідні бібліотеки

```sh
pip install -r new_video_download/requirements.txt
```

5) запустити

```sh
cd new_video_download
python main.py
```

## Конфлікт версій при встановленні

При тестуванні на деяких системах переривалось встановлення необхідних пакетів з файла requirements.txt. В такому випадку рекомендовано встановити вручну (при активованому віртуальному середовищі)

```sh
pip install PyQt5
pip install youtube_dl
pip install bs4
pip install requests
```


## Використання

- при старті задайте дату починаючи з якоі завантажувати викладені відео

- через меню додайте ПОВНЕ посилання на Videos канала, наприклад [https://www.youtube.com/@IrynaFarion/videos](https://www.youtube.com/@IrynaFarion/videos)

- коли знайдене нове відео для обраного посилання зправа з'явиться videoid

- при завантаженні відео для обраного посилання в переліку відео (зправа) будуть зявлятись назви відео замість videoid

- завантажені відеофайли зберігаються в каталог `Videos` з ім'ям videoid. Щоб легше віднайти бажаний файл, підтримується подвійний клік на назві відео 
