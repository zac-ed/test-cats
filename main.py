 # This script is based on an answer given in the SO Question:
# How to print number of characters based on terminal width that also resize?
# https://stackoverflow.com/questions/44129613/how-to-print-number-of-characters-based-on-terminal-width-that-also-resize/44133299#44133299

# We are essentially creating a thread safe print thread.
# See atricle on thread safe printing (Example of Dedicated Print Thread With Queue, specifically.)
# https://superfastpython.com/thread-safe-print-in-python/

#import game files
import cat_dnd as Game

import threading
import time
import sys
import subprocess

# get python version
# We'll use this to import modules specific to python version so that the engine is compatible with both.
major = int(sys.version_info[0])
minor = int(sys.version_info[1])

# import queue
if int(major < 3):
	import Queue as Q
else:
	import queue as Q

# import os.get_terminal_size
# use backport for python vers. < 3.3
if int(sys.version_info[0]) < 3 or int(sys.version_info[1]) < 3:
	from backports.shutil_get_terminal_size import get_terminal_size as getTS
else:
	from os import get_terminal_size as GetTS


# this is a public queue accessible by all threads.
printq = Q.SimpleQueue()
interrupt = False

lines = [""]*7
comparisonLines = lines.copy()

# Call game main class here
def main():
	# printingThread
	printingThread = threading.Thread(target=printer)
	# prevent thread from blocking the main thread from exiting.
	printingThread.daemon = True
	printingThread.start()

	#printq.put('a display string')
	#time.sleep(.5)
	#Game.printTildes(printq, "James", "Enter your Name:")
	#time.sleep(.5)
	Game.BuildSplashScreen(lines)
	time.sleep(.5)
	Game.WipeScreen("#", lines)
	Game.GoGame(lines)
# Convert this to perform as current line splitting method.
def split_line(line, cols):

	if len(line) > cols:
		new_line = ''
		ww = line.split()
		i = 0
		# if the concatonated string plus the next string fit on one line
		while len(new_line) <= (cols - len(ww[i])-1):
			# concatonate the string
			new_line += ww[i]
			i += 1
		if new_line == '':
			return (line, '')
		return (new_line, ''.join(ww[i:]))
	else:
		return (line, '')

def printer():

	while True:
		global lines, comparisonLines
		cols, rows = GetTS()
		# Mark total writable width of console
		msg = '#'*(cols)
		new_line = ''
		try:
			new_line = str(printq.get_nowait())
			# gracefully turn printer thread out (?)
			if new_line == '!@#EXIT#@!':
				sys.exit()
		except Q.Empty as e:
			pass
		for line in lines:
			#res = line
#			toprint = line
			# Write as much on one line as possible, cut the rest.
#			toprint, res = split_line(res, cols)
			##########################################
#			remaining_whitespace = cols - len(toprint) - 2
#			if remaining_whitespace > 0:
#				tildes = (remaining_whitespace//2)*"~"
#				toprint = '#' + tildes + toprint + tildes + (remaining_whitespace%2)*"~" + '#'
			##########################################
			msg += '\n' + line

#		if new_line == "\033[F":
#			print(new_line)
		# Only refresh the display if Lines has changed.

# Debug - Check lines array comparison
#		for i in range(0,len(lines)):
#			if lines[i] == comparisonLines[i]:
#				if i == len(lines)-1:
#					print(True)
#				continue
#			else:
#				print(False)

		if comparisonLines != lines:
			comparisonLines = lines.copy()
			subprocess.check_call('cls', shell=True)
			sys.stdout.write(msg)
			sys.stdout.flush()
		time.sleep(.5)

if __name__ == '__main__':
	main()