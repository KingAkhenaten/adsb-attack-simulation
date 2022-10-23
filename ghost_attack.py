# Simulates ADS-B Ghost Injection attack
# Run flight sim with regular data set
# Then run this program with a set target airplane
# Rerun flight sim with edited csv data
#TODO: possibly convert to OOP
import csv
import argparse

def gen_coords(ghost):
	return

def gen_alt(ghost):
	return

def gen_att(ghost):
	return

def write_csv(ghost):
	filename = "testGhost.csv"
	message = []
	for key, values in ghost.items():
		message.append(values)

	with open(filename, 'w') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(message)

def generate_data():
	ghost = {
		"format": "RTTFC",
		"hexid": "4851878",
		"lat": 0,
		"lon": 0,
		"baro_alt": 0,
		"baro_rate": 0,
		"gnd": 0,
		"track": 0,
		"gsp": 0,
		"cs_icao": "CJ69",		#TODO: Adjust
		"ac_type": "A320",		#TODO: Adjust
		"ac_tailno": "YR-CMM",	#TODO: Adjust
		"from_iatoa": "DUB",	#TODO: Adjust
		"to_iata": "CLJ",		#TODO: Adjust
		"timestamp": "1666556781.6",	#TODO: Adjust
		"source": "adsb_icao",
		"cs_iata": "36976",		#TODO: Adjust
		"msg_type": "255",
		"alt_geom": "0",
		"IAS": "0",
		"TAS": "0",
		"Mach": "0",
		"track_rate": "0",
		"roll": "0",
		"mag_heading": "0",
		"true_heading": "0",
		"geom_rate": "0",
		"emergency": "0",
		"category": "0",
		"nav_qnh": "0",
		"nav_altitude_mcp": "0",
		"nav_altitude_fms": "0",
		"nav_heading": "0",
		"nav_modes": "0",
		"seen": "0",
		"rssi": "0",
		"winddir": "211",
		"windspd": "37",
		"OAT": "-1",
		"TAT": "-1",
		"isICAOhex": "1",
		"Augmentation_status": "1",
		"Authentication": "",
	}

	gen_coords(ghost)
	gen_alt(ghost)
	gen_att(ghost)
	write_csv(ghost)


def main():
	parser = argparse.ArgumentParser(description="Simulates ADS-B deviation attack")
	parser.add_argument("target",
					help="Specify a callsign")
	parser.add_argument("filename",
					help="Specify the file to work with")
	parser.add_argument("-v", "--verbose", dest="verbose",
                    help="Output verbose logging",
                    action="store_true")

	args = parser.parse_args()
	rows = []

	if args.verbose:
		print("[*] Ghost callsign is %s" % args.target)
	generate_data()
	"""
	with open(args.filename, 'rw') as csvfile:
		csvreader = csv.reader(csvfile)

		if args.verbose:
			print("[*] Opened %s" % args.filename)

		generate_data()
	"""
main()