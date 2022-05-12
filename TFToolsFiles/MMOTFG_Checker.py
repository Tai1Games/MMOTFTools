import sys, os
import getopt

from KNamesRecord import KeyNamesRecord
import MapChecker
import ItemChecker
import DirectionsChecker
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

			if(not keyNames.checkAll()):
				print("Name errors must be fixed before proceeding")
				return -1

			print("Running all checks...")

			DirectionsChecker.checkAll(sys.argv[1])
			AttacksChecker.checkAll(sys.argv[1])
			EnemyChecker.checkAll(sys.argv[1])
			ItemChecker.checkAll(sys.argv[1])
			MapChecker.checkAll(sys.argv[1])
		else:
			#Get all relevant arguments
			arguments = sys.argv[2:]
			try:
				opts,args = getopt.getopt(arguments,"hmidea")
				if(not keyNames.checkAll()):
					print("Name errors must be fixed before proceeding")
					return -1

				for opt, arg in opts:
					if opt == "-m":
						#check maps
						MapChecker.checkAll(sys.argv[1])
					elif opt == "-i":
						#check items
						ItemChecker.checkAll(sys.argv[1])
					elif opt == "-d":
						#check directions
						DirectionsChecker.checkAll(sys.argv[1])
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
