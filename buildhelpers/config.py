#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pwd
from datetime import datetime

from buildbot.plugins import util

Interpolate = util.Interpolate

periodic_build_timer = 24*60*60
git_poller_interval = 5*60
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

test = '/usr/bin/test'
grep = '/bin/grep'
find = '/usr/bin/find'
su = '/bin/su'
mkdir = '/bin/mkdir'
env = '/usr/bin/env'
fuser = '/bin/fuser'
sudo = '/usr/bin/sudo'
rsync = '/usr/bin/rsync'
bash = '/bin/bash'
make = '/usr/bin/make'
useradd = '/usr/sbin/useradd'
reprepro = '/usr/bin/reprepro'
apt_get = '/usr/bin/apt-get'
gbp = '/usr/bin/gbp'
cowbuilder = '/usr/sbin/cowbuilder'
checkinstall = '/usr/bin/checkinstall'
mk_build_deps = '/usr/bin/mk-build-deps'
dpkg_parsechangelog = '/usr/bin/dpkg-parsechangelog'

dpkg_lock = '/var/lib/dpkg/lock'
pbuilder_dir = '/var/cache/pbuilder'
git_checkout_dir = pbuilder_dir+'/git-checkout'
reprepro_dir = pbuilder_dir+'/repo'
ccache_dir = pbuilder_dir+'/ccache'
incoming_dir = reprepro_dir+'/incoming'
incoming_dir_tree = Interpolate(incoming_dir+'/%(prop:buildername)s')
mirror = 'http://localhost:3142/cdn.debian.net/debian'

userid = pwd.getpwuid(os.getuid()).pw_uid
username = pwd.getpwuid(os.getuid()).pw_name

available_archs = ['i386', 'amd64']
available_distros = ['sid']
common_passwd = '123456'

slave_extrapackages = ['ccache', 'eatmydata', 'apt-cacher', 'cowbuilder',
                       'git-buildpackage', 'sudo']
base_cow_extrapackages = ['ccache', 'eatmydata', 'devscripts', 'equivs',
                          'checkinstall']

debootstrap_tarball = Interpolate(pbuilder_dir+'/debootstrap-%(prop:slavename)s.tgz')
debootstrap_tarball_dir = Interpolate(pbuilder_dir+'/debootstrap-%(prop:slavename)s')
base_cow_dir = Interpolate(pbuilder_dir+'/base-buildbot-%(prop:slavename)s.cow')
package_cow_dir = Interpolate(pbuilder_dir+'/base-buildbot-%(prop:buildername)s.cow')

parent_source_dir = Interpolate(git_checkout_dir+'/%(prop:buildername)s')
source_dir = Interpolate(parent_source_dir.fmtstring+'/%(prop:package)s')
debian_control = Interpolate(source_dir.fmtstring+'/debian/control')
makefile = Interpolate(source_dir.fmtstring+'/Makefile')
configure = Interpolate(source_dir.fmtstring+'/configure')

architecture = Interpolate('%(prop:architecture)s')
distribution = Interpolate('%(prop:distribution)s')
version = Interpolate('%(prop:version)s')
git_revision = Interpolate('%(prop:got_revision)s')

package = Interpolate('%(prop:package)s')
repository = Interpolate('%(prop:repository)s')
branch = Interpolate('%(prop:branch)s')
pre_build_deps = Interpolate('%(prop:prebuild-deps)s')

envdict = {'CCACHE_DIR': ccache_dir,
           'PATH': '/usr/lib/ccache:${PATH}',
           'LD_LIBRARY_PATH': '/usr/lib/libeatmydata:${LD_LIBRARY_PATH}',
           'LD_PRELOAD': 'libeatmydata.so ${LD_PRELOAD}',
           'DEBIAN_FRONTEND': 'noninteractive'}
base_cow_env = ' '.join(['%s="%s"' % (k, v) for k, v in envdict.items()])

apt_get_options = ['-o', 'Apt::Install-Recommends=false',
                   '-o', 'Apt::Get::Assume-Yes=true',
                   '-o', 'Apt::Get::AllowUnauthenticated=true',
                   '-o', 'DPkg::Options::=--force-confmiss',
                   '-o', 'DPkg::Options::=--force-confnew',
                   '-o', 'DPkg::Options::=--force-overwrite',
                   '-o', 'DPkg::Options::=--force-unsafe-io']
