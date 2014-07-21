#!/usr/bin/python

import sys
import re
import urllib2
import yaml

lorry_template = """
    "openstack/%s": {
        "type": "git",
        "url": "%s"
    }"""

git_template = "git://git.openstack.org/openstack/%s.git"

# Whitelist for which sections of programs should
# be lorried.
sections = [
	"Compute",
	"Object Storage",
	"Image Service",
	"Identity",
	"Dashboard",
	"Networking",
	"Block Storage",
	"Telemetry",
	"Orchestration",
	"Database Service",
	"Bare metal",
	"Common Libraries",
	"DNS Services",
]

def clean_repo(repo):
	ret = None
	name_match = re.search("(openstack|stackforge)/(.*)$", repo)

	# Filter out the specs repos.
	# Could probably be sone in the above regexp, but don't
	# have the inclination to work out how.
	if name_match:
		name = name_match.group(2)
		if not re.search("specs$", name):
			ret = name

	return ret


def main(argv):
	programs_yaml = urllib2.urlopen(
			"http://git.openstack.org/cgit/openstack/governance/plain/reference/programs.yaml").read()
	programs = yaml.load(programs_yaml)

	lorries = []

	for s in sections:
		section = programs[s]
		codename = section["codename"].lower()
		projects = section["projects"]
		repos = [clean_repo(p["repo"]) for p in projects]
		repos = filter(None, repos)

		for r in repos:
			url = git_template % r
			# Don't like use of '.' in lorry names
			name = r.replace("oslo.", "oslo-")

			lorries.append(lorry_template % (name, url))

	with open("./open-source-lorries/openstack.lorry", "w") as f:
		f.write("{")
		f.write(",\n".join(lorries))
		f.write("\n}\n")

if __name__ == "__main__":
	sys.exit(main(sys.argv))
