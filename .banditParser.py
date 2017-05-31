import sys
import json
import linecache
import hashlib
import argparse

def hash(toHash):
	hash_object = hashlib.sha256()
	hash_object.update(toHash)
	hex_dig = hash_object.hexdigest()
	return hex_dig

def issueAttribute(i):
	issueAttributes=""
	filename = i["filename"]
	issueAttributes += filename
	testId = i["test_id"]
	issueAttributes += testId
	lineRange = i["line_range"]
	for lineNumber in lineRange:
		codeExtract = linecache.getline(filename,lineNumber).rstrip().lstrip()
		issueAttributes += codeExtract	
	return issueAttributes

def calculateIssueHash(i):
	return hash(issueAttribute(i))

def printOutput(issueFingerprint, i):
	print "===================="
	print "Issue Fingerprint: " + issueFingerprint
	print "Issue Severity: %s \t Confidence Level: %s" % (i["issue_severity"], i["issue_confidence"])
	print "Location: %s"  % i["filename"]
	print "Issue: %s" % i["issue_text"]
	print "\nCode: \n%s" % i["code"]

def outputHigh(issueFingerprint, i):
	REDC = '\033[31m'
	ENDC = '\033[0m'
	output = ""
	output += REDC + "====================\n"
	output += REDC + "Issue Fingerprint: " + issueFingerprint + "\n"
	output += REDC + "Issue Severity: %s \t Confidence Level: %s" % (i["issue_severity"], i["issue_confidence"]) + "\n"
	output += REDC + "Location: %s"  % i["filename"] + "\n"
	output += REDC + "Issue: %s" % i["issue_text"] + "\n\n"
	output += "Code: \n%s" % i["code"]
	output += ENDC
	return output

def main(argv):
	exitCode = 0

	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--output", help="bandit output")
	parser.add_argument("-i", "--ignore", help="bandit.ignore file")
	args = parser.parse_args()

	banditOutputFile = args.output
	banditIgnore = args.ignore

	with open(banditOutputFile) as data_file:
		data = json.load(data_file)

	with open(banditIgnore) as file:
		falsepositive = json.load(file)
		falsePositiveSignatures = []

	for i in falsepositive["false_positives"]:
		falsePositiveSignatures.append(i["fingerprint"])

	for i in data["results"]:
		issueFingerprint = calculateIssueHash(i)
		if(i["issue_severity"]=="HIGH" and issueFingerprint not in falsePositiveSignatures):
			# exitCode = 1;
			print outputHigh(issueFingerprint, i)

	for i in data["results"]:
		issueFingerprint = calculateIssueHash(i)
		if(i["issue_severity"]=="MEDIUM" and 
			issueFingerprint not in falsePositiveSignatures):
			printOutput(issueFingerprint, i)

	for i in data["results"]:
		issueFingerprint = calculateIssueHash(i)
		if(i["issue_severity"]=="LOW" and 
			issueFingerprint not in falsePositiveSignatures):	
			printOutput(issueFingerprint, i)

	sys.exit(exitCode)


if __name__ == "__main__":
    main(sys.argv)