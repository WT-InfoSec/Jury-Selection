# jurySelection.py
# Will Taylor
# 09/27/2019

import random
import csv
import copy


def main():
    validJurors, invalidJurors = dict(), dict()
	# Assign judges to respective courts & prepare for jury assignment
    courtBank = initializeCourts()
	# Parse CSV file to determine valid & invalid candidates
    processCandidates(validJurors, invalidJurors)
	# Create a backup of valid jurors before assigning them to courts
    validJurorsBackup = copy.deepcopy(validJurors)
	# Display totals for exempt/valid candidates and confirm demands are met
    printExemptCandidates(invalidJurors)
    printEligibleCandidates(validJurors)
	# Assign valid jurors to courts & update assignment information
    fillCourts(validJurors, courtBank)
	# Display court assignments & seat positions of all candidates
    printCourtAssignments(courtBank)
	# Display backup candidate population
    printRemainingCandidates(validJurors)


class JuryCandidate(object):

    def __init__(self, ID, name, age, address, exemptList, checkedIn):
	    self.name = name
	    self.id = ID
	    self.exemptList = exemptList
	    self.isPresent = checkedIn
	    self.courtAssigned = None
	    self.seatNumber = None
	    self.judge = None

    def assignCourt(self, courtName, seatNumber, judge):
	    self.courtAssigned = courtName
	    self.seatNumber = seatNumber
	    self.judge = judge


class TarrantCountyCourt(object):

    def __init__(self, courtName, courtType, judge):
	    self.courtName = courtName
	    self.courtType = courtType
	    self.judge = judge
	    self.numCandidates = 24
	    self.candidates = None
	    self.jury = None
		# Set jury size and number of candidates based on the court type
	    if ("civil" in self.courtType.lower()
		     or "family" in self.courtType.lower()):
		    self.jurySize = 6
	    else:
		    self.jurySize = 12

    def updateCandidates(self, candidateList):
	    self.candidates = candidateList


def initializeCourts():
    """Returns dictionary containing TarrantCountyCourt objects.

    Assigns judges to respective courts & prepares for jury assignment.
    """

    courtBank = dict()
    getCountyCivilCourts(courtBank)
    getCountyCriminalCourts(courtBank)
    getDistrictCivilCourts(courtBank)
    getDistrictCriminalCourts(courtBank)
    getDistrictFamilyCourts(courtBank)
    getDistrictJuvenileCourts(courtBank)
    print("%s jury candidates are needed today."
	       % str(totalCandidatesNeeded(courtBank)))
    return courtBank


def processCandidates(validJurors, invalidJurors):
    """Reads data and updates valid & invalid juror dictionaries. 

    Parses data from each line of jurySummons file. 
    Determines valid and invalid jurors then inserts
    candidates into approrpriate dictionaries.

    Args:
        validJurors: Empty dictionary to store non-exempt candidates.
                     Jury IDs are keys to access JuryCandidate objects.

        invalidJurors: Empty dictionary to store exempt candidates.
                       Jury IDs are keys to access JuryCandidate objects.
    """

    with open('jurySummons.txt') as candidates:
	    csv_reader = csv.reader(candidates, delimiter=',')
	    lineCount = 0
		# Create bounds to reconstruct exemptList from extraction
	    exemptStart, exemptEnd = 4,11
	    for row in csv_reader:
		    if (lineCount > 0):
				# Parse data from CSV
			    jNumber, name = row[0], row[1]
			    age, address = row[2], row[3]
			    checkIn = row[-1]
			    exemptList = ''
			    for i in range(exemptStart, exemptEnd+1):
				    exemptList += row[i] 
				# Add exempt and absent candidates to invalid set
			    if (isExempt(exemptList)) or (isAbsent(checkIn)):
				    addToInvalid(invalidJurors, jNumber, name, age,
					             address, exemptList, checkIn)
				# Add valid candidates to valid set
			    else:
				    addToValid(validJurors, jNumber, name, age,
				               address, exemptList, checkIn)
		    lineCount += 1


def fillCourts(validJurors, courtBank):
    """Assigns valid jurors to courts.
    
    For each court, candidates are randomly popped from the validJurors dict
    and added to the candidate list. Each JuryCandidate object is updated
    with their assigned court, judge, and seat number. The candidate list is
    stored in the TarrantCountyCourt object.

    Args:
        validJurors: Dictionary containing all non-exempt jury candidates.
                     Jury IDs are keys to access JuryCandidate objects.

        courtBank: Dictionary containing all court data.
                   Court Names are keys to access TarrantCountyCourt objects.
    """

    for court in courtBank:
	    candidateList = []
	    courtName = courtBank[court].courtName
	    judge = courtBank[court].judge
	    for i in range(courtBank[court].numCandidates):
		    seatNumber = i+1
			# Randomly select juror and set variable to candidate object
		    for r in random.sample(validJurors.keys(),1):
			    candidate = validJurors.pop(r)
			# Update candidate data and add to list
		    candidate.assignCourt(courtName, seatNumber, judge)
		    candidateList.append(candidate)
		# Assign candidates to court
	    courtBank[court].updateCandidates(candidateList)

def addToInvalid(invalidJurors, number, name, age, address, exempt, checkIn):
    invalidJurors[number] = JuryCandidate(number, name, age, 
					  address, exempt, checkIn)


def addToValid(validJurors, number, name, age, address, exempt, checkIn):
    validJurors[number] = JuryCandidate(number, name, age, 
					address, exempt, checkIn)


def totalCandidatesNeeded(courtBank):
    count = 0
    for court in courtBank:
	    count += courtBank[court].numCandidates
    return count


def addCourtsToBank(courtBank, courtType, courtNames, judges):
    for i in range(len(courtNames)):
	    name = courtNames[i]
	    judge = judges[i]
	    courtBank[name] = TarrantCountyCourt(name, courtType, judge)
	

def getCountyCivilCourts(courtBank):
    courtType = "County Civil"
    courtNames = ['CCL_01', 'CCL_02', 'CCL_03']
    judges = ["Don Pierson", "Jennifer Rymell", "Mike Hrabal"]
    addCourtsToBank(courtBank, courtType, courtNames, judges)


def getCountyCriminalCourts(courtBank):
    courtType = "County Criminal"
    courtNames = ['CCC_01', 'CCC_02', 'CCC_03', 'CCC_04', 'CCC_05',
			      'CCC_06', 'CCC_07', 'CCC_08', 'CCC_09', 'CCC_10' ]

    judges = ["David Cook", "Carey Walker", 
		      "Bob McCoy", "Deborah Nekhom", 
		      "Jamie Cummings", "Molly Jones", 
		      "Cheril Hardy", "Chuck Vanover",
		      "Brent Carr","Phil Sorrells"]
    addCourtsToBank(courtBank, courtType, courtNames, judges)


def getDistrictJuvenileCourts(courtBank):
    courtType = 'District Juvenile'
    courtNames = ["DJC_01"]
    judges = ["Alex Kim"]
    addCourtsToBank(courtBank, courtType, courtNames, judges)


def getDistrictCivilCourts(courtBank):
    courtType = 'District Civil'
    courtNames = ['DCL_01', 'DCL_02', 'DCL_03', 'DCL_04', 'DCL_05',
				  'DCL_06', 'DCL_07', 'DCL_08', 'DCL_09', 'DCL_10' ]

    judges = ["Melody Wilkenson", "David L. Evans",
		      "Don Cosby", "R.H. Wallace",
		      "John P. Chupp", "Susan Heygood McCoy",
		      "Tom Lowe", "Kimberly Fitzpatrick",
		      "Mike Wallach", "Josh Burgess"]
    addCourtsToBank(courtBank, courtType, courtNames, judges)


def getDistrictCriminalCourts(courtBank):
    courtType = 'District Criminal'
    courtNames = ['DCC_01', 'DCC_02', 'DCC_03', 'DCC_04', 'DCC_05',
			      'DCC_06', 'DCC_07', 'DCC_08', 'DCC_09', 'DCC_10' ]
	
    judges = ["Elizabeth Beach", "Wayne Salvant",
		      "Robb Catalano", "Mike Thomas",
		      "Christopher Wolfe", "David Hagerman",
		      "Mollee Westfall", "Scott Wisch",
		      "George Gallagher", "Ruben Gonzalez Jr."]
    addCourtsToBank(courtBank, courtType, courtNames, judges)


def getDistrictFamilyCourts(courtBank):
    courtType = 'District Family'
    courtNames = ['DFC_01', 'DFC_02', 'DFC_03', 'DFC_04', 'DFC_05', 'DFC_06']

    judges = [ "Jesus E. Nevarez Jr.", "Kenneth Newell",
		       "James Munsford", "Jerry Hennigan",
		       "Judith Wells", "Patricia Baca Bennett"]
    addCourtsToBank(courtBank, courtType, courtNames, judges)


def isExempt(exemptList):
    if('t' in exemptList.lower()):
	    return True
    return False


def isAbsent(checkIn):
    if('f' in checkIn.lower()):
	    return True
    return False


def printExemptCandidates(invalidJurors):
    print("There are %d exempt jurors from this summons:" % len(invalidJurors))
    #for p in invalidJurors:
    #	print(invalidJurors[p].name)


def printEligibleCandidates(validJurors):
    print("There are %d eligible jurors from this summons:" % len(validJurors))
    #for p in validJurors:
    #	print(validJurors[p].name)


def printRemainingCandidates(validJurors):
    print("*** AFTER COURT ASSIGNMENTS THERE ARE %s REMAINING CANDIDATES ***:"
	      % str(len(validJurors)))
    for p in validJurors:
	    print(validJurors[p].id + ':' + validJurors[p].name)


def printCourtAssignments(courtBank):
    for court in courtBank:
	    print("*********** JURY CANDIDATES FOR COURT %s *************" 
		       % courtBank[court].courtName)
	    print("COURT TYPE: %s" % courtBank[court].courtType)
	    print("JUDGE: %s" % courtBank[court].judge)
	    for c in courtBank[court].candidates:
		    print(' SEAT %s >>> ' % c.seatNumber + c.id + ':'+ c.name)	

main()
