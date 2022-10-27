# adsb-attack-simulation
Source code for the simulation of ADS-B attacks

In the python scripts, information regarding running the script can be obtained by appending "-h" to the command line parameters.
Target is the icao callsign of the target plane. Filename is either the filename of the supplied data,
or in the case of the ghost attack, it is the filename to write the ghost plane data to.

When using ghost_attack.py, one must also supply latitude and longitude coodinates in decimal degrees format.

deviation_attack.py, dos_attack.py, ghost_attack.py written by Christian Clay
