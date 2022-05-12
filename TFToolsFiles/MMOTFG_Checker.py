import sys, os
import getopt

import KNamesRecord
from KNamesRecord import KeyNamesRecord
#import mapaChecker
#import itemChecker
import  MapChecker
import EnemyChecker
import AttacksChecker

def displayHelp():
	print(
'''
Usage: python MMOTFG_Checker.py <filepath to checked directory> [options]

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
	else:
		#Check that given filepath exists
		if not os.path.exists(sys.argv[1]):
			print("Given directory path is incorrect or doesn't exist")
			exit(1)

		#Get list of names
		keyNames = KeyNamesRecord(sys.argv[1])

		if len(sys.argv) == 2:
			directionsChecker.checkAll(sys.argv[1])
			print("Running all checks...")

			keyNames.checkAll()
			EnemyChecker.checkAll(sys.argv[1])
			AttacksChecker.checkAll(sys.argv[1])
		else:
			#Get all relevant arguments
			arguments = sys.argv[2:]
			try:
				opts,args = getopt.getopt(arguments,"hmidea")
				keyNames.checkAll()

				for opt, arg in opts:
					if opt == "-m":
						#check maps
						MapChecker.checkAll(sys.argv[1], keyNames)
					elif opt == "-i":
						#check items
						print("placeholder")
					elif opt == "-d":
						#check directions
						directionsChecker.checkAll(sys.argv[1])
					elif opt == "-e":
						EnemyChecker.checkAll(sys.argv[1])
					elif opt == "-a":
						AttacksChecker.checkAll(sys.argv[1])
					elif opt == "-h":
						#display help
						displayHelp()
			except getopt.GetoptError:
				print("ERROR: Option not recognized")
				displayHelp()
				sys.exit(1)


if __name__ == "__main__":
	main()
