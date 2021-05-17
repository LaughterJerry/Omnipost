import web

"""
board creation/editing form
takes in the board title, and name
the title is what the board goes by on the database, and is related to the link
'/' = index
'/this' = this

name can be anything and is what the users see when opening the page

the site logo and board logo are arranged so that the admin can set unique logos for each board

access permission restricts what the users can see so a special "ideas" board can be made
	or new boards can be carefully curated before being made public
	boards can be set to public simply by leaving this feild blank

board keywords are strung together with post keywords and stuck in a meta tag for SEO

the Desktop CSS and Mobile CSS allow a page to be made mobile friendly without the need to
	setup a different "mobile" site which is both bloated and not user-friendly
	using CSS to simply restyle existing elements allows for all features to be used
	by mearly turning normal links into buttons or hiding/showing elements which might be
	useful only some of the time

the footer can be used for anything but is typically for including extra links, about pages
information on who everyone is etc
"""

board_form = web.form.Form(
	web.form.Textbox('title', web.form.notnull,
		size=30,
		description="Board title:"),
	web.form.Textbox('name', web.form.notnull,
		size=30,
		description="Board Name:"),

	web.form.Textbox('link', web.form.notnull,
		size=30,
		description="Board link:"),
	web.form.Textbox('sitelogo', web.form.notnull,
		size=30,
		description="Site Logo"),
	web.form.Textbox('boardlogo', web.form.notnull,
		size=30,
		description="Board Logo"),
	web.form.Textbox('perm',
		size=30,
		description="Access Permission:"),
	web.form.Textbox('keywords', web.form.notnull,
		size=30,
		description="Board Keywords:"),
	web.form.Textbox('post_order', 
		rows=30,
		description="Post Order"),

	web.form.Textarea('tags', web.form.notnull,
		rows=30, cols=80,
		description="Board Tags:"),

	web.form.Textarea('css', web.form.notnull,
		rows=30, cols=80,
		description="Board Css:"),

	web.form.Textarea('mobile', web.form.notnull,
		rows=30, cols=80,
		description="Mobile Css:"),
	web.form.Textarea('footer', web.form.notnull,
		rows=30, cols=80,
		description="Board Footer:"),

	web.form.Button('Create Board')

	)

"""
a simple post form with a title, and title text

the title is the bold text name, and is requried

title text is the "subtitle" and isn't required

keywords are strung together with board keywords in a meta tag for SEO

alt-text is a currently unused feild, potentially for a future binding for twitter cards

post content is the main body of the post, tokenized so it can accept any formatting text
	allowing the main body to embed extra elements, styling, and javascript
"""

post_form = web.form.Form(
	web.form.Textbox('title', web.form.notnull, 
		size=30,
		description="Post title:"),
	web.form.Textbox('titletext',
		size=30,
		description="Post subtitle:"),
	web.form.Textbox('keywords', web.form.notnull,
		size=30,
		description="Post Keywords:"),
	web.form.Textbox('alt', web.form.notnull,
		size=30,
		description="Post Alt Text:"),
	web.form.Textarea('content', 
		rows=30, cols=80,
		description="Post content:"),
	web.form.Button('Post entry'),
)
"""
a short version of the post form taking only title and content,
content body is not formatted like post body so that arbitrary code execution by 
	malicious parties isn't possibly
"""
comment_form = web.form.Form(
	web.form.Textbox('title', web.form.notnull, 
		size=30,
		description="Name:"),
	web.form.Textarea('content', web.form.notnull, 
		rows=8, cols=70, maxlength=2000,
		description="Comment:"),
	web.form.Input('comment', type='submit', value='Comment'),
)


























