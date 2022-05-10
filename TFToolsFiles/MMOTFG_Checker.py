import sys
import getopt

#import mapaChecker
#import itemChecker
#import directionsChecker
#import enemiesChecker
#import attacksChecker

def displayHelp():
	print(
'''
Usage: python MMOTFG_Checker.py <filepath to checked folder> [options]

Usage example: python ../files/ -mid

Possible options:
	-h display this message
	-m check maps
	-i check items
	-d check directions
	-e check enemies
	-a attacks
''')

def main():
	#Check if user has input any arguments, if no arguments found execute all checks
	if len(sys.argv) == 1:
		displayHelp() #no 
	elif len(sys.argv) == 2:
		print("Running all checks...")
	else:
		#Get all relevant arguments
		arguments = sys.argv[2:]

		try:
			opts,args = getopt.getopt(arguments,"hmidea")

			for opt, arg in opts:
				if opt == "-m":
					#check maps
					print("placeholder")
				elif opt == "-i":
					#check items
					print("placeholder")
				elif opt == "-d":
					#check items
					print("placeholder")
				elif opt == "-e":
					#check items
					print("placeholder")
				elif opt == "-a":
					#check items
					print("placeholder")
				elif opt == "-h":
					#display help
					displayHelp()
		except getopt.GetoptError:
			print("ERROR: Option not recognized")
			displayHelp()
			sys.exit(1)


if __name__ == "__main__":
	main()