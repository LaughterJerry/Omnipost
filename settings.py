#### settings

"""
this module needs to be replaced with a proper login module
username and password should be hard coded here to prevent third parties from accessing vital information

admin login page should consist of a username/password combination
if no entries in the login table then password should have two forms to validate the password
password should have certain complexity requirements, taking into account all factors
bits of entropy are more important that arbitrary number/letter replacements

complexity = length * charsets - known words^2

the more known words in a password the less secure it is, however a long enough password wouldn't take a large penalty for this
a special common password list should also be compared to giving an extra penalty for common passwords
such as a passphrase instead of a password, charsets would be [a-z], [A-Z], [0-9], and [!-*]
example: "P4ssword!" is 9 characters long, times 4 charsets gives 36
	password is a known common password and thus is penalized by 5
	complexity = 30

	"Potato horse butlarian god" is 26 characters long with 2 charsets = 52
	potato, horse, and god are normal words thus - 3
	complexity = 49

	it would therefore take longer to guess the second passphrase than the first password even with fewer charsets

next passwords should not be stored in plain text, encrypted, or (unsalted) hased
a salted hash with at least 12 rounds is minimum requirement, each hash must be securly generated random data

usernames salts and hashes are all stored in the access table

- this could be expanded in later versions to allow user accounts, potentially allowing this multiboard blog to also operate
	as a forum

web.py has a built-in session system which can store and retrieve active sessions, negating the need for a custom system

####
currently if someone wants to login to the site they must directly connect to the proper IP address
since if they use a service like cloudflare that masks the IP address of the visitor

"""

admin_ip = "" #set this to home IP address

db_username = "" #database username
db_password = "" #database password
