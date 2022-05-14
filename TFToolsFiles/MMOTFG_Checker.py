import sys
import os
import getopt
import inspect

from KNamesRecord import KeyNamesRecord
import MapChecker
import ItemChecker
import DirectionsChecker
import EnemyChecker
import AttacksChecker
import HTML_Creator as html


def displayHelp():
    print(
        '''
Usage: python MMOTFG_Checker.py <filepath to checked directory> [options]

Usage example: python ../files/ -mid

Possible options:
	-h display this message
	-m check maps
    -s show interactive map
	-i check items
	-d check directions
	-e check enemies
	-a attacks
''')


def main():

    allErrorsDict = {}  # we save all the errors we find

    # Check if user has input any arguments, if no arguments found execute all checks
    if len(sys.argv) == 1:
        displayHelp()  # no
    else:
        # Check that given filepath exists
        if not os.path.exists(sys.argv[1]):
            print("Given directory path is incorrect or doesn't exist")
            exit(1)

        # Get list of names
        keyNames = KeyNamesRecord(sys.argv[1])

        if len(sys.argv) == 2:
            print("Running all checks...")

            if not keyNames.checkAll():
                print("Name errors must be fixed before proceeding")
                return -1
            # if len(keyNamesErrors) > 0:
            #     allErrorsDict.update({"keyNamesErrors": keyNamesErrors})
            directionsErrors = DirectionsChecker.checkAll(sys.argv[1])
            if len(directionsErrors) > 0:
                allErrorsDict.update({"directionsErrors": directionsErrors})

            attacksErrors = AttacksChecker.checkAll(sys.argv[1])
            if len(attacksErrors) > 0:
                allErrorsDict.update({"attacksErrors": attacksErrors})

            enemyErrors = EnemyChecker.checkAll(sys.argv[1], keyNames)
            if len(enemyErrors) > 0:
                allErrorsDict.update({"enemyErrors": enemyErrors})

            itemErrors = ItemChecker.checkAll(sys.argv[1], keyNames)
            if len(itemErrors) > 0:
                allErrorsDict.update({"itemErrors": itemErrors})

            mapErrors = MapChecker.checkAll(sys.argv[1], keyNames)
            if len(mapErrors) > 0:
                allErrorsDict.update({"mapErrors": mapErrors})
        else:
            # Get all relevant arguments
            arguments = sys.argv[2:]
            try:
                opts, args = getopt.getopt(arguments, "hmsidea")
                if not keyNames.checkAll():
                    print("Name errors must be fixed before proceeding")
                    return -1

                for opt, arg in opts:
                    if opt == "-m":
                        # check maps
                        showMap = ('-s', '') in opts
                        mapErrors = MapChecker.checkAll(sys.argv[1], keyNames, showMap)
                        if len(mapErrors) > 0:
                            allErrorsDict.update({"mapErrors": mapErrors})
                    elif opt == "-i":
                        # check items
                        itemErrors = ItemChecker.checkAll(sys.argv[1], keyNames)
                        if len(itemErrors) > 0:
                            allErrorsDict.update({"itemErrors": itemErrors})
                    elif opt == "-d":
                        # check directions
                        directionsErrors = DirectionsChecker.checkAll(
                            sys.argv[1])
                        if len(directionsErrors) > 0:
                            allErrorsDict.update(
                                {"directionsErrors": directionsErrors})
                    elif opt == "-e":
                        enemyErrors = EnemyChecker.checkAll(
                            sys.argv[1], keyNames)
                        if len(enemyErrors) > 0:
                            allErrorsDict.update({"enemyErrors": enemyErrors})
                    elif opt == "-a":
                        attacksErrors = AttacksChecker.checkAll(sys.argv[1])
                        if len(attacksErrors) > 0:
                            allErrorsDict.update(
                                {"attacksErrors": attacksErrors})

                    elif opt == "-h":
                        # display help
                        displayHelp()
            except getopt.GetoptError:
                print("ERROR: Option not recognized")
                displayHelp()
                sys.exit(1)

    html.createHTML(allErrorsDict)


if __name__ == "__main__":
    main()
