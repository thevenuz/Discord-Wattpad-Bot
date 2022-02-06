# Discord Wattpad Bot

A Discord bot to fetch the latest chapters of your wattpad stories and share them in your Discord server whenever a new chapter of your story is published.

### Features
* New chapters links will be shared in the Discord servers within 2 mins of publishing the chapter.
* Can check multiple stories for new chapters.

### How it works?
* There is nothing special about this bot, all of it's features are very simple basic things that a Discord bot is expected to do. The only thing that's different and speciality
of this bot is it's ability to fetch the new published chapters.
* There is no official Public API available from Wattpad to get these details, so the only other choice we have and I used is to scrape the Wattpad website for getting the required details.
* The wattapd scraper I used in this application just checks the wattapd stories and gets the lastest chapter's published time.
* Then I just trigger my wattapd scraper every two minutes using Tasks in Lightbulb library and the rest is just sending this link to the servers.

### The Code...
I know that my code is trash and I might have over complicated things. But in my defence I was learning python when I'm writing this bot. No, actually I'm still learning. I started
 this bot to learn python though after some time I focused more on completing the bot than learning python. But please don't hesitate to criticize the code, I want to know what mistakes I've 
 done, so go ahead.
 
 
### Built using Hikari and Hikari-Lightbulb libraries
