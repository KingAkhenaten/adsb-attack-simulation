# Simulates ADS-B Ghost Injection attack
# Run flight sim with regular data set
# Then run this program with a set target airplane
# Rerun flight sim with edited csv data
import csv
import math
import argparse
# test p1 = 51.478223, -0.601654
# test p2 = 51.478223, -0.297403


def get_distance(p1, p2):
	p1 = list(map(lambda x: math.radians(x), p1))
	p2 = list(map(lambda x: math.radians(x), p2))

	lat_distance = p2[0] - p1[0]
	lon_distance = p2[1] - p1[1]

	# Haversine formula
	y = (
		pow(math.sin(lat_distance / 2), 2)
		+ math.cos(p1[0]) * math.cos(p2[0]) * pow(math.sin(lon_distance / 2), 2))
	return 6373.0 * (2 * math.atan2(math.sqrt(y), math.sqrt(1 - y)))

def gen_coords(args, ghost):
	track_x = []
	track_y = []
	p1 = []
	p2 = []
	p1.append(float(args.lat_1))
	p1.append(float(args.lon_1))
	p2.append(float(args.lat_2))
	p2.append(float(args.lon_2))

	distance = get_distance(p1, p2)

	x_difference = p2[0] - p1[0]
	y_difference = p2[1] - p1[1]
	num_coords = 1000
	coord_step = 1 / num_coords
	previous_x = p1[0]
	previous_y = p1[1]

	for i in range(num_coords):
		this_x = previous_x + x_difference * coord_step
		this_y = previous_y + y_difference * coord_step
		previous_x = this_x
		previous_y = this_y
		track_x.append(this_x)
		track_y.append(this_y)
		ghost["lat"] = str(round(this_x, 5))
		ghost["lon"] = str(round(this_y, 5))
		timestamp = float(ghost["timestamp"]) + 0.1
		timestamp = round(timestamp, 1)
		ghost["timestamp"] = str(timestamp)
		write_csv(ghost)

	return (track_x, track_y)

	print(distance)
	return

def gen_alt(ghost):
	alt_f = "2000"
	ghost["baro_alt"] = alt_f
	ghost["baro_rate"] = 0
	ghost["alt_geom"] = alt_f
	ghost["geom_rate"] = "0"
	ghost["nav_qnh"] = "1012.8"
	ghost["nav_altitude_mcp"] = ghost["baro_alt"]
	ghost["nav_altitude_fms"] = "-1"

	return ghost

def gen_att(ghost):
	hdg = "90.0"
	ghost["track"] = hdg
	ghost["track_rate"] = "0"
	ghost["roll"] = "0.0"
	ghost["mag_heading"] = ghost["track"]
	ghost["true_heading"] = ghost["track"]
	ghost["nav_heading"] = "-1"

	return ghost

def gen_speed(ghost):
	ghost["gsp"] = "400.0"	#knots
	ghost["IAS"] = ghost["gsp"]
	ghost["TAS"] = ghost["gsp"]
	# Calculate Mach number
	T_cel = float(ghost["OAT"]) + 273.16
	V_sound_knots = 643.855 * pow((T_cel/273.15), 0.5)
	mach = float(ghost["gsp"]) / V_sound_knots
	ghost["Mach"] = str(round(mach, 3))
	return ghost


def write_csv(ghost):
	filename = "testGhost.csv"
	message = []
	for key, values in ghost.items():
		message.append(values)
	with open(filename, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(message)

def generate_data(args):
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
		"source": "X2",
		"cs_iata": "UAE3333",		#TODO: Adjust
		"msg_type": "adsb_icao",
		"alt_geom": "0",
		"IAS": "0",
		"TAS": "0",
		"Mach": "0",
		"track_rate": "0",
		"roll": "0",
		"mag_heading": "0",
		"true_heading": "0",
		"geom_rate": "0",
		"emergency": "none",
		"category": "A3",
		"nav_qnh": "0",
		"nav_altitude_mcp": "0",
		"nav_altitude_fms": "0",
		"nav_heading": "0",
		"nav_modes": "",
		"seen": "0",
		"rssi": "-9.9",
		"winddir": "211",
		"windspd": "37",
		"OAT": "4",
		"TAT": "4",
		"isICAOhex": "1",
		"Augmentation_status": "193719",
		"Authentication": "",
	}

	ghost = gen_alt(ghost)
	ghost = gen_att(ghost)
	ghost = gen_speed(ghost)
	print(ghost)
	gen_coords(args, ghost)

	# write_csv(track, ghost)


def main():
	parser = argparse.ArgumentParser(description="Simulates ADS-B deviation attack")
	parser.add_argument("callsign",
					help="Specify a callsign")
	parser.add_argument("lat_1",
					help="Specify the starting coordinate")
	parser.add_argument("lon_1",
					help="Specify the starting coordinate")
	parser.add_argument("lat_2",
					help="Specify the ending coordinate")
	parser.add_argument("lon_2",
					help="Specify the ending coordinate")
	parser.add_argument("filename",
					help="Specify the file to work with")
	parser.add_argument("-v", "--verbose", dest="verbose",
                    help="Output verbose logging",
                    action="store_true")

	args = parser.parse_args()
	rows = []

	if args.verbose:
		print("[*] Ghost callsign is %s" % args.target)
	generate_data(args)
	"""
	with open(args.filename, 'rw') as csvfile:
		csvreader = csv.reader(csvfile)

		if args.verbose:
			print("[*] Opened %s" % args.filename)

		generate_data()
	"""
main()