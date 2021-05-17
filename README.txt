The Omnipost simple blog system

(c) Monchy, 2021

GPL v3

To use:

first spin up a linux based server with a basic lamp stack
install mod_wsgi for apache using this method: https://webpy.org/cookbook/mod_wsgi-apache-ubuntu
then install web.py into the mod_wsgi libraries

after that copy the site.conf file to the desired location, either your virtualhost configuration or 000-default.conf

install mysql and create a single database named 'blog'

open settings.py and enter the username and password to the blog in the specified variables

as well as the admin's home IP address or the address they will most often access the server

optionally you can use cloudflare to provide additional security and hide the server IP address, if you do you must connect to the server directly when using admin because cloudflare hides the user IP address as well

when you start it up there will be a set of links, click /newboard and create your first blog board!
each board is for a different subject and multiple options exist for basic formatting, the "post order" entry in the form allows you to chose if the posts are shown in newest-first or oldest-first order, leaving it blank will mean users can only see the oldest post unless you add a link to the oldest post for navigation

the software uses user-agent checks to determine if the user is on mobile, and if so returns the CSS under mobile, allowing the admin to create a different layout for mobile users

example.css contains a basic starting point so that the admin can clearly see the position of all the elements in the webpage to update the code as they see fit

comments on posts are tokenized and web-safe so arbitrary code injection is not possible, post bodies however made by the admin are not sanitized in the same way so the use of arbitrary code in production is discouraged until you fully test said code

the tag system works off regex replacing basic tags with blocks of html, the pattern is first, then the #split# indicator the the replacement text,  example: 
        \[p\]\s*(.+?)\s*\[/p\]#split#<p id='bodytext'>\1</p><br>

        this turns [p]thing[/p] into <p id='bodytext'>thing</p><br>

        (.+?) matches with anything contained within except for the closing portion of the pattern
        \1 indicates the positional information that was extracted, so adding a second (.+?) would need a \2 in order to format properly

enjoy your new blog! <3

