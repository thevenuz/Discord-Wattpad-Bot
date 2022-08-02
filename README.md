# Discord Wattpad Bot

A Discord Bot that can share new chapter notifications from your favorite wattpad stories and new announcement notifications from your favorite wattpad authors.

### Features:
* New chapter links will be shared in your server as soon as the author publishes a new chapter in a story you're following.
* New Announcement content will be shared in your server as soon as the author you're following makes an announcement on Wattpad.

### How it works?
* All the bot's features are very basic things that all the Discord bots are capable of. The only different and unique feature of this bot is to check for new chapters and announcements of wattpad automatically.

* As there is no official public API available from Wattpad, this bot makes use of web scraping to get the necessary details of the stories and announcements.

### How to use the Bot?
The steps are more detailed in the [top.gg page](https://top.gg/bot/929384339840585799)
* The first step is setting up a default channel so that the bot knows in which channel the updates need to be posted. This can be done by using **/set-channel < channel >** command.
* Use **/follow-story < storyurl >** command to follow stories.
* Use **/follow-author < author-profile-url >** command to follow authors.
* And you're done, the bot will automatically shares the updates from the story and author you followed in the channel that's been set.
* You can find the other commands using **/help** command.

### About the Code...
The code is still a mess, but it's organized mess compared to the previous version.

### Built using Hikari and Hikari-Lightbulb libraries
