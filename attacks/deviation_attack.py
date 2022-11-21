# Simulates ADS-B Deviation attack
# Run flight sim with regular data set
# Then run this program with a set target airplane
# Rerun flight sim with edited csv data
#TODO: possibly convert to OOP
import csv
import argparse

def stats(args, rows, num_entries, original_loc, deviator, deviation, displacement):
	field_iter = 0
	for col in rows[:num_entries]:
		if col[9] == args.target:
			if args.verbose:
				print("[%s] Deviated %s to %s" % 
					(args.target, original_loc[field_iter][0], col[2]))
				print("[%s] Deviated %s to %s" % 
					(args.target, original_loc[field_iter][1], col[3]))

			field_iter += 1
	print("[%s] True displacement %f, %f" % (args.target, 
				displacement[0][0], displacement[0][1]))
	print("[%s] Deviated displacement %f, %f" % (args.target,
				displacement[1][0], displacement[1][0]))
def main():

	parser = argparse.ArgumentParser(description="Simulates ADS-B deviation attack")
	parser.add_argument("target",
					help="Specify a target to attack")
	parser.add_argument("filename",
					help="Specify the file to work with")
	parser.add_argument("-v", "--verbose", dest="verbose",
                    help="Output verbose logging",
                    action="store_true")

	args = parser.parse_args()
	fields = []
	rows = []
	field_iter = 0
	original_coords = []
	deviated_coords = []
	displacement = []
	deviation = []
	deviator = (0, 0.03)

	# target = "RYR6KG"

	if args.verbose:
		print("[*] Target is %s" % args.target)

	with open(args.filename, 'r') as csvfile:
		fd = csv.reader(csvfile)
		# assume no header
		for row in fd:
			rows.append(row)
		num_entries = fd.line_num
		if args.verbose:
			print("[*] Opened %s" % args.filename)

	# column 9 is cs_icao (ICAO call sign)
	# column 2 is latitude
	# column 3 is longitude

	if args.verbose:
		print("[*] Lattitude Deviation %s" % deviator[0])
		print("[*] Longitude Deviation %s" % deviator[1])


	for col in rows[:num_entries]:
		if col[9] == args.target:
			# store original values for displacement calculation
			original_coords.append((float(col[2]), float(col[3])))

			# deviated values
			deviated_coords.append((float(col[2]) + deviator[0], float(col[3]) + deviator[1]))
			# store deviation
			deviation.append((deviated_coords[field_iter][0], deviated_coords[field_iter][1]))
			deviation[field_iter] = (deviated_coords[field_iter][0] - float(col[2]), 
				deviated_coords[field_iter][1] - float(col[3]))

			# write to columns
			col[2] = str(deviated_coords[field_iter][0])
			col[3] = str(deviated_coords[field_iter][1])

			field_iter += 1
	
	# calculate displacement
	displacement.append((abs(original_coords[field_iter - 1][0] - original_coords[0][0]),
						abs(original_coords[field_iter - 1][1] - original_coords[0][1])))
	displacement.append((abs(deviated_coords[field_iter - 1][0] - deviated_coords[0][0]),
						abs(deviated_coords[field_iter - 1][1] - deviated_coords[0][1])))

	stats(args, rows, num_entries, original_coords, deviator, deviation, displacement)
	with open(args.filename + "_dev", 'w', newline='') as csvfile:
		fd2 = csv.writer(csvfile)
		fd2.writerows(rows)

main()