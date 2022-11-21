# Simulates ADS-B DoS attack
# Run flight sim with regular data set
# Then run this program with a set target airplane
# Rerun flight sim with edited csv data
import csv
import argparse

def main():
	rows = []
	field_iter = 0
	# target = "DLH2WA"

	parser = argparse.ArgumentParser(description="Simulates ADS-B deviation attack")
	parser.add_argument("target",
					help="Specify a target to attack")
	parser.add_argument("filename",
					help="Specify the file to work with")
	parser.add_argument("-v", "--verbose", dest="verbose",
                    help="Output verbose logging",
                    action="store_true")

	args = parser.parse_args()

	if args.verbose:
		print("[*] Target is %s" % args.target)

	with open(args.filename, 'r') as csvfile:
		fd = csv.reader(csvfile)

		# assume no header
		for row in fd:
			rows.append(row)

	# column 9 is cs_icao (ICAO call sign)
	for col in rows[:fd.line_num]:
		if col[9] == args.target:
			field_iter += 1
			rows.remove(col)
	if args.verbose:
		print("[*] Two entries for %s found" % args.target)
	field_iter = 0

	# check array after removal
	for col in rows[:fd.line_num]:
		if col[9] == args.target:
			field_iter += 1

	if field_iter == 0:
		print("[%s] DoS completed" % args.target)

	with open(args.filename + "_jam", 'w', newline='') as csvfile:
		fd2 = csv.writer(csvfile)
		fd2.writerows(rows)

main()