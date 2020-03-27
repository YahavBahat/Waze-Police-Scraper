# Waze-Police-Scraper
Waze Police Scraper will scrape the police locations and display them in map as pins.
You'll be able to see more information about every cop vehicle/trap and also download the scraped data.

More in [Features](#features)

- [Waze-Police-Scraper](#waze-police-scraper)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Features](#features)

## Installation:

For it to work, we need to use browser-mob-proxy, so:

`pip install -r requirements.txt`

and install browser-mob-proxy by going to [here](https://bmp.lightbody.net), and click download as zip.

Extract the archive and in `Waze_Police_Scraper.py`, in line 65, replace `...` with the path of the executable

**Do not forget to replace every backslash \ with double-backslash \\.**

in the newly extracted folder, for example the path will be:

`path_to_folder\\browsermob-proxy-2.1.4-bin\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy`

If you downloded and extracted the folder in the downloads folder and you're on drive C:

`C:\\Users\\your_name\\Downloads\\browsermob-proxy-2.1.4-bin\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy`

Download geckodriver for Selenium by going here [here](https://github.com/mozilla/geckodriver/releases)

and and in `Waze_Police_Scraper.py`, in line 70, replace `...` with the path to the exe geckodriver file

**Again, do not forget to replace every backslash \ with double-backslash \\.**

**That's it!**

Now run `Waze_Police_Scraper.py`:

`python3 App.py`

[Usage](#usage)

## Usage:

In the first input type 'a' or 'A' for Automatic scraping.

In the second choose how often do you want the program to scrape. (**Numbers only (Integers)**)

**Notice: The recommended value is 5 seconds,**

**but if you're scraping in other countries it will take time to get there with the mouse,**

**so prefferbly select 10 seconds.**

That time is for the user to move to another location, to scrape police vehicles / Traps reported by Waze's users.

If you press Enter, without entering any number, the number will be the default, 5 seconds, which is also the recommended value.

After the Firebox browser launched and you're done scraping, just close the browser, and wait 5 seconds.

After that, go to `localhost:5000` or `127.0.0.1:5000`.

[Features](#features)

## Features:

If you go to `localhost:5000`,

In the map, by clicking on the pins you'll be able to see more information on them like coordinates,

type of police (vehicle or trap), speed, number of up votes by Waze's users, and confidence and reliability estimated by Waze.

Also, you can download the scraped data as JSON, XLS (Excel), and CSV by clicking on the buttons.
