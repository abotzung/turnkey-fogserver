'''Reconfigure IP address in FOG server'''
# Alexandre Botzung <alexandre.botzung@grandest.fr> - dec. 2022
# Originally written by Copyright (c) 2008 Alon Swartz <alon@turnkeylinux.org> - all rights reserved (confconsole.py)

from re import match, sub, MULTILINE, search
from os.path import isfile
import urllib.parse
from urllib.parse import urlparse
import subprocess
from subprocess import check_output, check_call
import os
import sys
import dialog
import ipaddr
from string import Template

import ifutil
import netinfo
import getopt

import conf

from io import StringIO
import traceback
import subprocess
from subprocess import PIPE, CalledProcessError
import shlex

import plugin

def _get_filtered_ifnames_sys():
	ifnames = []
	for ifname in netinfo.get_ifnames():
		if ifname.startswith(('lo', 'tap', 'br', 'natbr', 'tun',
							  'vmnet', 'veth', 'wmaster')):
			continue
		ifnames.append(ifname)

	# handle bridged LXC where br0 is the default outward-facing interface
	defifname = conf.Conf().default_nic
	if defifname and defifname.startswith('br'):
			ifnames.append(defifname)
			bridgedif = subprocess.check_output(
					['brctl', 'show', defifname],
					text=True).split('\n')[1].split('\t')[-1]
			ifnames.remove(bridgedif)

	ifnames.sort()
	return ifnames

def _get_default_nic_sys():
	def _validip(ifname):
		ip = ifutil.get_ipconf(ifname)[0]
		if ip and not ip.startswith('169'):
			return True
		return False

	defifname = conf.Conf().default_nic
	if defifname and _validip(defifname):
		return defifname

	for ifname in _get_filtered_ifnames_sys():
		if _validip(ifname):
			return ifname

def run():
    
        # if no interfaces at all - display error and go to advanced
    if len(_get_filtered_ifnames_sys()) == 0:
        error = "No network adapters detected"
        if not self.advanced_enabled:
            return ""

    # if interfaces but no default - display error and go to networking
    ifname = _get_default_nic_sys()
    if not ifname:
        error = "Networking is not yet configured"
        return "networking"
        
    subprocess.call(['changeip-fogserver'], shell=True)
