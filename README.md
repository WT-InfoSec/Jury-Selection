# Jury-Selection
This program imports a CSV file containing jury candidate data, then randomly assigns all eligible candidates to Tarrant County courtrooms. 

__________

First each court room is initialized as a "TarrantCountyCourt" object containing the following data:

Court Name - [String]
Court Type - [String]
Judge - [String]
Number of Candidates - [Int]
Candidates - [List] (Null until candidates are assigned to courts)
Jury Size - [Int] (determined by Court Type)
Jury - [List] (Null until Jury is selected)

__________

As the program parses through the Jury Summons CSV, each candidate is initialized as a "JuryCandidate" object containing the following data:

Name - [String]
Jury ID - [String]
Exempt List - [String] (data used to determine if candidate is exempt from Jury Duty)
Attendance - [Boolean] (is the candidate present)
Assigned Court - [String] (Null until court is assigned)
Assigned Seat Number - [String] (Null until court is assigned)
Assigned Judge - [String] (Null until court is assigned)

__________

Candidates are sorted into separated into "validJuror" and "invalidJuror" dictionaries based on Exempt List data.

__________

Valid Candidates are randomly assigned a Tarrant County courtroom and seat number, until all courtrooms are filled.

Jury Candidate "Court", "Judge", and "Seat Number" values are updated with their assignment data.

Courtroom "Candidate" values are updated with assigned Jury Candidates and their seat numbers.

__________

After assignments are complete, a list of jury candidates and their seat numbers are displayed for every court.

Finally, a list of unassigned jury candidates is printed to the console.





