import web
import datetime

"""
currently two model classes support the website 
clever code in the future might merge them into one using *args instead of positional arguments
the web.database module allows tokenized submissions without the need to sanitize inputs
"""

class settings_model:
	def __init__(self, user, password):
		"""
		creates a db object which is used to create/edit/delete rows from each function
		more effecient than creating the db object for each transaction, for which a single webpage might make
		multiple requests of the database
		"""
		self.user = user
		self.password = password
		self.table = "settings"
		self.db = web.database(dbn='mysql', db='blog', user=self.user, password=self.password)
		try:
			void = self.db.select(self.table , order='id ASC')
		except:
			self.db.query(setting_schema)

	def get_boards(self, admin):
		"""
		if the admin flag is false it only retrieves publicly available boards (who's perm is null)
		"""
		if not admin:
			boards = self.db.select(self.table , order='id ASC', where="perm=''")
		else:
			boards = self.db.select(self.table , order='id ASC')
		return boards

	def get_board(self, title):
		#if the board doesn't exist, perhaps due to visiting a random page, this returns none
		try:
			return self.db.select(self.table, where="title=$title", vars=locals())[0]
		except IndexError:
			return None

	def new_board(self, title, name, link, sitelogo, boardlogo, perm, keywords, post_order, tags, css, mobile, footer):
		self.db.insert(self.table, 
						title=title, 
						name=name,
						link=link,
						sitelogo = sitelogo,
						boardlogo = boardlogo,
						perm=perm,
						keywords=keywords,
						post_order=post_order,
						tags=tags,
						css=css,
						mobile=mobile,
						footer=footer,
						created_on=datetime.datetime.utcnow())

	def del_board(self, title):
		self.db.delete(self.table, where="title=$title", vars=locals())

	def update_board(self, title, name, link, sitelogo, boardlogo, perm, keywords, post_order, tags, css, mobile, footer):
		self.db.update(self.table, 
						where="title=$title", 
						link=link,
						name=name,
						sitelogo = sitelogo,
						boardlogo = boardlogo,
						perm=perm,
						keywords=keywords,
						post_order=post_order,
						tags=tags,
						css=css,
						mobile=mobile,
						footer=footer,
						created_on=datetime.datetime.utcnow(), vars=locals())

class entry_model:
	def __init__(self, user, password, board):
		"""
		the entry model is used when working with posts on a board
		ideas for merging entry and settings, board="settings"
		having a default value would default to the settings instead of the tables
		the board name is formatted into the table, allowing the link to be used directly 
		when calling this model
		"""
		self.user = user
		self.password = password
		self.table = "%s_entries" % (board)
		self.db = web.database(dbn='mysql', db='blog', user=self.user, password=self.password)
		self.exists = False
		try:
			void = self.db.select(self.table , order='id DESC')
		except:
			self.db.query(entry_schema % (board))

	def drop(self):
		#deletes the current boards posts without issue
		self.db.query("DROP TABLE %s;" % self.table)

	def get_posts(self, id= '', post_order='ASC'):
		where = "reply='{id}'".format(id=id)
		order = "id {post_order}".format(post_order=post_order)

		#returns posts if not reply, else returns replies
		#returns in the specified order
		posts = self.db.select(self.table , order=order, where=where )

		return posts


	def get_last(self):
		#gets the most recent post
		try:
			return self.db.select(self.table, order='id DESC', where="reply=''", vars=locals())[0]
		except:
			return None

	def get_first(self):
		#gets the least recent post
		try:
			return self.db.select(self.table, order='id ASC', where="reply=''", vars=locals())[0]
		except:
			return None

	def get_post(self, id):
		#gets a specific post identified by id, if not found then return None
		try:
			return self.db.select(self.table, where="id=$id and reply=''", vars=locals())[0]
		except IndexError:
			return None

	def new_post(self, title, text, titletext='', alt='', keywords="", reply=""):
		self.db.insert(self.table, title=title, content=text, titletext=titletext, alt=alt, keywords=keywords, reply=reply, posted_on=datetime.datetime.utcnow())

	def del_post(self, id):
		#deletes the post by ID
		self.db.delete(self.table, where="id=$id", vars=locals())

	def update_post(self, id, title, text, titletext='', alt='', keywords='', reply=''):
		#updates the post by ID
		self.db.update(self.table, where="id=$id", title=title, content=text, titletext=titletext, alt=alt, keywords=keywords, reply=reply, vars=locals())

