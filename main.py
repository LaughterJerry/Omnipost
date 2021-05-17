"""
Omnipost v alpha 1.0 "Hammer"
a posting system allowing anyone to easily create and maintain a simple multi-subject blog
links easily to twitter

based on web.py's example - Basic blog using webpy 0.3
original code since deleted
"""
import web
import sys
import re

#adding homepath to the sys is nessesary due to the way apache seems to operate
#nessesary for importing local modules
#change this if using virtual hosts
homepath = '/var/www/html/'

sys.path.insert(1, homepath)

import os

#changes the operational directory to use relative paths
os.chdir(homepath)

from utils import model
import forms
import settings


mob_devices = ['phone', 'droid', "berry"]

urls = (
	'/', 'Index',
	'/view/(\d+)', 'View',
	'/new', 'New',
	'/upload', 'Upload',
	'robots.txt', 'Robot',

	'/newboard', 'NewBoard',
	'/editboard/([A-Za-z]+)', 'EditBoard',
	'/delboard/([A-Za-z]+)', 'DelBoard',

	'/delete/(\d+)', 'Delete',
	'/edit/(\d+)', 'Edit',

	'/([A-Za-z]+)',         'Index',
	'/([A-Za-z]+)/view/(\d+)',      'View',
	'/([A-Za-z]+)/new',             'New',
	'/([A-Za-z]+)/delete/(\d+)','Delete',
	'/([A-Za-z]+)/edit/(\d+)',      'Edit',

)

"""
globals are functions that are passed to the templates
since templates are created as a means of executing python script directly
it must be maintained in a safe state, so certain functions and commands are restricted
unless passed through here
"""
t_globals = {
	'datestr': web.datestr, 'print':print, 'websafe':web.websafe, 're':re
}

#currently only renders a single page(index.html)
#future pages could function to render different styles of website
render = web.template.render(homepath + 'templates',  globals=t_globals)


class webPage:
	def __init__(self):
		"""

		proccess:
			page request = link
			break link into board_title and post_id
			check boards for board, if not found return to index
			if no boards available return blank page
			else get post from id
			if post not found return to index
			else return post

			create new board by submitting data, creates new board entry and table for the board
			delboard drops board table and deletes board entry

			page variables are:
				board_data - obtained from board_db.get_board(board_title)
				boards - obtained from board_db.get_boards(admin) - exclude boards that require admin perm

				page - obtained from page_db.get_post(post_id)
				posts - obtained from page_db.get_posts()

				comments - obtained from page_db.get_posts(post_id) - returns all posts who are marked as a reply to post_id

				board_form - board_form_r, none if not admin and not new/edit_board
				post_form - post_form_r, none if not admin and not new/edit_post
				comment_form - comment_form_r, none if not page

				admin - obtained from user_ip = admin ip, used to render admin-only controls SERVERSIDE USE ONLY


		"""
		self.board_form = forms.board_form
		self.post_form = forms.post_form
		self.comment_form = forms.comment_form

		self.board = "index"
		self.post_id = None

		self.cur_board = { #default cur_board data to avoid unnessary errors
			"title":"none",
			"name":"none",
			"link":"none",
			"sitelogo":"",
			"boardlogo":"",
			"perm":"admin",
			"keywords":"",
			"css":"",
			"footer":"",
		}

		self.boards_data = []

		self.post = None
		self.posts = []

		self.comments = []

		self.board_form_r = None
		self.post_form_r = None
		self.comment_form_r = None

		self.admin = (web.ctx['ip'] == settings.admin_ip) #to be replaced with proper login, see: settings.py

		self.statics = {} # holds static file infomation for admin quick reference when writing posts

		#settings, posts, comments

		self.board_db = model.settings_model(settings.db_username, settings.db_password)
		self.boards_data = list(self.board_db.get_boards(self.admin))

		self.db = None

		print("webpage initialized")

	def __return_webpage__(self):
		"""
		returns the webpage, with default values if nessesary
		default values are used to nullify elements, so if something isn't assigned
		then it simply is not created in the webpage
		whole pages therefore do not have to be created for every little thing
			simply assign a value to the arguments and call __return_webpage__
		"""


		# a simple but effective means of determining if the user is on mobile
		# add additional checks for undermined mobile devices in mob_devices
		try:
			agent = web.ctx.env['HTTP_USER_AGENT'].lower()
		except:
			agent = ""
		self.mobile = any(x in agent for x in mob_devices )

		print("returning webpage")
		return render.index(
			self.cur_board, 
			self.boards_data,

			self.post, 
			self.posts, 

			self.comments, 

			self.board_form_r,
			self.post_form_r, 
			self.comment_form_r, 

			self.mobile,
			self.admin, 

			self.statics

			)

	def __define_args__(self, args):
		"""
		sets the basic variables and arguments
		for the loading webpage, determining the board being accessed
		the post if available
		and the static files

		returns 404 if the page doesn't exist

		note: create proper 404 page
		"""

		for arg in args:
			if arg.isdigit():
				self.post_id = arg #does this have to be a string instead?
			else:
				self.board = arg
		for board in self.boards_data:
			if board['title'] == self.board:
				self.cur_board = board
		if self.cur_board['title'] == 'none' and not self.admin:
			raise web.notfound() #seeother('/notfound')
		if self.admin:
			self.statics['img'] = os.listdir(homepath + "static/img")
			self.statics['img'].sort()
		print("argument set")

	def GET(self, *args):
		#python uses GET and POST functions directly, so any other functions must be called from there
		"""
			sets up the args and then checks if there are boards, creating an object to access posts if so
		"""
		self.__define_args__(args)
		if len(self.boards_data) > 0:
			#this creates a board's table if it doesn't exist if AND ONLY IF the board is listed in settings
			self.db = model.entry_model(settings.db_username, settings.db_password, self.board)

		print("database selected")
		return self.getPage()

	def HEAD(self, *args):
		#identical to GET, used for crawlers that only check the header data
		self.__define_args__(args)
		if len(self.boards_data) > 0:
			self.db = model.entry_model(settings.db_username, settings.db_password, self.board)

		print("database selected")
		return self.getPage()

	def POST(self, *args):
		#identical to get, but returns postPage instead
		self.__define_args__(args)
		if len(self.boards_data) > 0:
			self.db = model.entry_model(settings.db_username, settings.db_password, self.board)

		return self.postPage()

class Robot:
	#needed for crawlers like google and twitter
	#without this cards wont work
	def GET(self):
		return "User-agent: *\nAllow: *"

	def HEAD(self):
		return "User-agent: *\nAllow: *"


class Index(webPage):
	def getPage(self):
		"""
		checks for the existance of posts and redirects to the appropriate page
		if DESC then most recent page is returned
		if ASC then least recent page is returned
		if None then least recent page is returned and posts are not visible
		ASC can be used as a static page to direct around the blog
			None does the same but allows full control over what the users see
		DESC is for typical blog format

		possible desired functions in the future:
			return the viewed page directly allowing for single-page boards to act like static pages
			a board named /about for example can have a single post with contact info
		"""
		if self.db:

			if self.cur_board['post_order'] == 'DESC':
				self.post = self.db.get_last()
			else:
				self.post = self.db.get_first()

			if self.post and self.board != "index":
				raise web.seeother(self.cur_board['link'] +  '/view/' + str(self.post['id']))
			elif self.post:
				raise web.seeother('/view/' + str(self.post['id']))
		print("returning blank webpage")
		return self.__return_webpage__()


class View(webPage):
	"""
		allow users to view posts
		get retrieves all needed information about the post and other posts on the board

		post allows users to leave comments
	"""
	def getPage(self):
		if self.db:

			self.post = self.db.get_post(int(self.post_id))
			self.posts = list(self.db.get_posts(post_order=self.cur_board['post_order']))
			self.comments = self.db.get_posts(str(self.post_id))
			self.comment_form_r = self.comment_form()
		return self.__return_webpage__()

	def postPage(self):
		if self.db:
			self.comment_form_r = self.comment_form()
			if not self.comment_form_r.validates():
				return self.__return_webpage__()
			self.db.new_post(self.comment_form_r.d.title, 
							self.comment_form_r.d.content[:2000], 
							reply=str(self.post_id))
		raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

class New(webPage):
	"""
	simply allows admin to create a new webpage and nothing more
	get returns the form nessary
	post submits all information, if the nessary info isn't filled out returns a prompt
	"""
	def getPage(self):
		if self.db and self.admin:
			self.post_form_r = self.post_form()
			return self.__return_webpage__()
		else:
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

	def postPage(self):
		if self.db and self.admin:
			self.post_form_r = self.post_form()
			if not self.post_form_r.validates():
				return self.__return_webpage__()
			self.db.new_post(self.post_form_r.d.title, 
							self.post_form_r.d.content, 
							self.post_form_r.d.titletext, 
							self.post_form_r.d.alt, 
							self.post_form_r.d.keywords)
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment
		else:
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment


class Delete(webPage):
	"""
	allows the admin to delete old webpages
	"""
	def postPage(self):
		if self.admin and self.db:
			self.db.del_post(int(self.post_id))
		raise web.seeother(self.cur_board['link'] ) #most pages should do this


class Edit(webPage):
	"""
	nearly identical to /new but retrieves post data like /view
	and fills out the form for editing, post is updated if information is validated
	otherwise prompts corrections
	"""
	def getPage(self):
		if self.admin and self.db:
			self.post = self.db.get_post(int(self.post_id))
			self.posts = list(self.db.get_posts(post_order=self.cur_board['post_order']))
			self.post_form_r = self.post_form()
			self.post_form_r.fill(self.post)
			return self.__return_webpage__()
		else:
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

	def postPage(self):
		if self.admin and self.db:
			self.post_form_r = self.post_form()
			self.post = self.db.get_post(int(self.post_id))
			if not self.post_form_r.validates():
				return self.__return_webpage__()
			self.db.update_post(int(self.post_id), 
					self.post_form_r.d.title, 
					self.post_form_r.d.content, 
					self.post_form_r.d.titletext, 
					self.post_form_r.d.alt, 
					self.post_form_r.d.keywords)
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment
		else:
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

class NewBoard(webPage):
	"""
	creates a new board in a similar fasion to /new page
	post takes all arguments and uses it to create a new board
	"""
	def getPage(self):
		if self.admin:
			self.board_form_r = self.board_form()
			return self.__return_webpage__()
		else:
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

	def postPage(self):
		if self.admin:
			self.board_form_r = self.board_form()
			if not self.board_form_r.validates():
				return self.__return_webpage__()
			self.board_db.new_board(self.board_form_r.d.title, 
							self.board_form_r.d.name,
							self.board_form_r.d.link, 
							self.board_form_r.d.sitelogo, 
							self.board_form_r.d.boardlogo, 
							self.board_form_r.d.perm, 
							self.board_form_r.d.keywords,
							self.board_form_r.d.post_order,
							self.board_form_r.d.tags,
							self.board_form_r.d.css,
							self.board_form_r.d.mobile,
							self.board_form_r.d.footer)
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment
		else:
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

class Upload(webPage):
	"""
	a post-only page used to upload static files
	the full directory must be typed in and must already exist
	only works for admin

	"""
	def postPage(self):
		if self.admin:
			x = web.input(myfile={}, directory="")
			filedir = x.directory
			if 'myfile' in x:
				filepath = x.myfile.filename.replace('\\', '/')
				filename=filepath.split('/')[-1]
				fout = open(filedir + '/' + filename, 'wb')
				fout.write(x.myfile.file.read())
				fout.close()
		raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

class DelBoard(webPage):
	#same as /delete but for boards
	#drops the board's table if removed, deleting all posts
	def postPage(self, comment = ""):
		if self.admin and self.db:
			self.db.drop()
			self.board_db.del_board( self.board )
			raise web.seeother('/')
		else:
			raise web.seeother('/')


class EditBoard(webPage):
	"""
	same as /newboard, but fills out the form for easier editing
	"""
	def getPage(self):
		if self.admin and self.db:
			self.board_data = self.board_db.get_board(self.board )
			self.board_form_r = self.board_form()
			self.board_form_r.fill(self.board_data)
			return self.__return_webpage__()
		else:
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

	def postPage(self):
		if self.admin and self.db:
			self.board_form_r = self.board_form()
			if not self.board_form_r.validates():
				return self.__return_webpage__()
			self.board_db.update_board(self.board_form_r.d.title, 
							self.board_form_r.d.name,
							self.board_form_r.d.link, 
							self.board_form_r.d.sitelogo, 
							self.board_form_r.d.boardlogo, 
							self.board_form_r.d.perm, 
							self.board_form_r.d.keywords,
							self.board_form_r.d.post_order,
							self.board_form_r.d.tags,
							self.board_form_r.d.css,
							self.board_form_r.d.mobile,
							self.board_form_r.d.footer)
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment
		else:
			raise web.seeother('/') #should redirect back to the current page so navigation isn't nessary after every comment

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == '__main__':
	app.run()
