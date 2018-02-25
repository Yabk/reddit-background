# reddit-background
Small python script that downloads image from a subreddit and sets it as wallpaper.

Currently only works on GNOME.

# Automating the script
The easiest way to automate this script is using Cron.
If you are new to cron here is a useful tutorial: https://linuxconfig.org/linux-cron-guide

# Usage
The script pulls the current top image from one of subreddits listed in subreddits.txt (chosen at random).
If you wish to add a subreddit you can do so by simply putting it in the subreddits.txt file.
A few default subreddits are already provided.

You can use the script by simply calling it without any parameters.
There is also additional option to save the image to a custom folder by using `-o` or `--todir` parameters.




If you need any help feel free to open an issue or contact me directly.

Any kind of contribution to the project is highly appreciated.
