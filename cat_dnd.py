import random
import sys
from time import sleep as z
from os import get_terminal_size as getTS
if int(sys.version_info[0]) < 3 or int(sys.version_info[1]) < 3:
         from backports.shutil_get_terminal_size import get_terminal_size as getTS
else:
         from os import get_terminal_size as GetTS

# Fills any remaining space in line with tildes
def printTildes(printQ, inputString, displayString):
	#inputLength = len(inputString)
	#displayLength = len(displayString)-inputLength


	#printQ.put(inputString)
	printQ.put(displayString)

	#numChars = 38 - displayLength
	#mod = numChars-inputLength
	#if mod > 0:
		#tildeDisplay = mod*'~'
		#printQ.put(tildeDisplay)
	#else:
		#printQ.put("Screen Size is big enough")

def ResetInputUI(lines):
	lines[6] = FillRemainingSpace('=', "INPUT")
	z(0.5)

def FillRemainingSpace(pattern, theString):
	# Evaluate leftover space
	numCols, numRows = GetTS()
	width = numCols - 2 - len(theString)
	# Calculate how many times we can repeat the pattern in the line space
	n = width//len(pattern)
	# Evaluate space left after we fit full repating pattern
	spaceLeft = width%len(pattern)
	if spaceLeft > 0:
		# Can't fit full pattern so get partial pattern
		remainingLine = pattern[0:spaceLeft]
	else:
		# Pattern repeats perfectly
		remainingLine = ""
	# Put the string together
	ret = "#" + theString + n*pattern + remainingLine + "#"
	return ret

def WipeScreen(pattern, lines):
	numCols, numRows = GetTS()

	originalLines=lines.copy()
	for col in range(0, numCols-2):
		patternEnd = (col+1)*"#"
		#print(len(patternEnd))

		for row in range(0, len(lines)-1):
			if col == numCols:
				lines[row] = col*"#"
			lines[row] = originalLines.copy()[row][0:-(2+col)] + patternEnd + "#"
			

#Debug
#			print(originalLines.copy()[row])
		z(0.02)

	originalLines=lines.copy()		
	for col in range(0, numCols):
		patternEnd = (col+1)*"~"
		#print(len(patternEnd))

		for row in range(0, len(lines)-1):
			if col == numCols-1:
				lines[row] = "#" + (numCols-2)*'~' + "#"
				continue
			lines[row] = originalLines.copy()[row][0:-(2+col)] + patternEnd + "#"
#Debug
#			print(originalLines.copy()[row])
		z(0.02)
def BuildSplashScreen(lines):
	numCols,numRows = GetTS()
	w = numCols - 2

	# Adjust line patterns here, they are replicated as many times as is nessessary to fill the console
	# NB: to print the escape key, '\' we need to escape it, '\\'
	patterns = [
		"~",
		"  ^- -^ ",
		" /o w o\\",
		"~",
		"| U   U ",
		" \\_____/",
		"#"
	]
	# Define the index of the pattern to wrap the centralised titleString.
	titleLine = 3
	titleString = "     HI! WELCOME TO SCII STEEPE!     "

	#Modify display list
	for i in range(0,len(patterns)):
		# Evaluate the pattern
		pattern = patterns[i]

		if i == titleLine:
			# Use method for title segment to centralise text
			lines[i] = CenterText(pattern, titleString)
			continue

		# No text, continue pattern evaluation
		patternLength = len(pattern)
		width = w

		# Evaluate leftover space
		spaceLeft= (width % patternLength)
		if spaceLeft > 0:
			remainingLine = pattern[0:spaceLeft]
		else:
			remainingLine = ""

		#Assign pattern to line.
		lines[i] = "#" + (width//patternLength)*pattern + remainingLine + "#"
		z(.5)




def ErrorCorrection(pattern, countSpace):
	# countSpace pair:
	#	0 ~ count of fully repeating pattern
	#	1 ~ space leftover to fill with partial pattern
	if (countSpace[1]+1) == len(pattern):
		countSpace[0] += 1
	else:
		countSpace[1] += 1
#Debug
#	print(countSpace[0],countSpace[1])
#	z(5)
#####
	return countSpace


def RepeatingPattern(pattern, halfWidth, adjustX, isOdd=False):
	leftCount = (halfWidth + adjustX) // len(pattern)
	leftSpace = (halfWidth + adjustX) % len(pattern)
	# Define the pair in correct order as required by ErrorCorrection()..
	leftPair = [leftCount, leftSpace]

	rightCount= (halfWidth - adjustX) // len(pattern)
	rightSpace= (halfWidth - adjustX) % len(pattern)
	rightPair = [rightCount, rightSpace]

	if isOdd:
		rightPair = ErrorCorrection(pattern, rightPair)

	# Returns 2 lists represting the left and right pair
	return leftPair, rightPair

def CenterText(pattern, theString, adjustX=0):
	# Evaluate the space
	numCols, numRows = GetTS()
# Debug
#	if (numCols - 2) % 2 != 0:
#		print("Whole Width is odd")
#		z(1)
#####
	width = numCols - len(theString) - 2
	halfWidth = width // 2

	# We need to add an extra character in case the width is odd
	if width % 2 != 0:
#Debug
#		print("Width - String is odd")
#		z(1)
#####
		left, right = RepeatingPattern(pattern, halfWidth, adjustX, True)
	else:
#Debug
#		print("Width - String is even")
#		z(1)
#####
		left, right = RepeatingPattern(pattern, halfWidth, adjustX)

	patternLeftEdge = ""
	patternRightEdge = ""

	if left[1] > 0:
		patternLeftEdge = pattern[-left[1]:]
	if right[1] > 0:
		patternRightEdge = pattern[0:right[1]]

	ret = "#" + patternLeftEdge + left[0]*pattern + theString + right[0]*pattern + patternRightEdge + "#"
	return ret

def randomShift():
	return random.randint(5,10)


## Splash Screen
def GoGame(lines):
	greeting = [
		"Salutations!",
		"Greetings.."
	]
	greetingReply = [
		"! What a nice name!",
		"! It is great to meet you"
	]
	# I wanted it to be class but obviously that's not a name we can use..
	occupation = [
		"Which class would you like?",
		"Choose a starting class.."
	]
	alignment = [
		"How are you aligned?",
		"and your alignment?"
	]
	# 1st fork in conversation
	from random import randint as Roll
	
	question = greeting[Roll(0,1)] + " What is your name?"
	lines[0] = CenterText("~~?~~", question, -randomShift())
	ResetInputUI(lines)
	userInput = input()
	reply = userInput+greetingReply[Roll(0,1)]
	lines[1] = CenterText("~~<3~~", reply, randomShift())
	z(.5)

	# 2nd fork in conversation
	question = occupation[Roll(0,1)]
	lines[2] = CenterText("~~?~~", question, -randomShift())
	# Example of a prompt that we will overwrite when the user responds
	z(.5)
	lines[3] = CenterText("~~!~~", "any class at all!", randomShift())
	ResetInputUI(lines)
	userInput = input()
	reply = userInput+'! i once was a '+userInput+' myself!'
	lines[3] = CenterText("~~!~~", reply, randomShift())
	z(.5)

	# 3rd fork in conversation
	question = alignment[Roll(0,1)]
	lines[4] = CenterText("~~?~~", question, -randomShift())
	ResetInputUI(lines)
	userInput = input()
	reply = userInput+' is it? a wise choice indeed'
	lines[5] = CenterText("~~<3~~", reply, randomShift())
	z(.5)

	cont=input("Press Enter to Quit")