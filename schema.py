
"""
schema for creating tables
each board is created as a row in settings, with a unique ID
boards are selected using title and are sorted ASC
"""
setting_schema = """CREATE TABLE settings (
	id INT AUTO_INCREMENT,
	title TEXT,
	name TEXT,
	link TEXT,
	sitelogo TEXT,
	boardlogo TEXT,
	perm TEXT,
	created_on DATETIME,
	keywords TEXT,
	post_order TEXT,
	tags TEXT,
	css TEXT,
	mobile TEXT,
	footer TEXT,
	primary key (id)
);

"""

"""
new boards are given a %s_entries table with %s being the board name
comments are submitted into the same table using reply with the ID of the post they reply to
posts are selected by ID if reply is blank, implying they are not replies
consider turning into format string instead with %s being {board}
"""
entry_schema = """CREATE TABLE %s_entries (
	id INT AUTO_INCREMENT,
	title TEXT,
	titletext TEXT,
	alt TEXT,
	keywords TEXT,
	content TEXT,
	posted_on DATETIME,
	reply TEXT,
	primary key (id)
);"""