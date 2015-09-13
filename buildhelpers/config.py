#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pwd

from buildbot.plugins import util

Interpolate = util.Interpolate

sudo = '/usr/bin/sudo'
rsync = '/usr/bin/rsync'
cowbuilder = '/usr/sbin/cowbuilder'
gbp = '/usr/bin/gbp'
bash = '/bin/bash'
make = '/usr/sbin/make'
checkinstall = '/usr/sbin/checkinstall'
useradd = '/usr/sbin/useradd'
reprepro = '/usr/bin/reprepro'
apt_get = '/usr/bin/apt-get'
mk_build_deps = '/usr/bin/mk-build-deps'


dpkg_lock = '/var/lib/dpkg/lock'
pbuilder_dir = '/var/cache/pbuilder'
git_checkout_dir = pbuilder_dir+'/git-checkout'
reprepro_dir = pbuilder_dir+'/repo'
ccache_dir = pbuilder_dir+'/ccache'
incoming_dir = reprepro_dir+'/incoming'
mirror = 'http://localhost:3142/cdn.debian.net/debian'

userid = pwd.getpwuid(os.getuid()).pw_uid
username = pwd.getpwuid(os.getuid()).pw_name


available_archs = ['i386', 'amd64']
available_distros = ['sid']
common_passwd = '123'
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

package = Interpolate('%(prop:package)s')
repository = Interpolate('%(prop:repository)s')
branch = Interpolate('%(prop:branch)s')
pre_build_deps = Interpolate('%(prop:prebuild-deps)s')

base_cow_env = {'CCACHE_DIR': ccache_dir,
                'PATH': '/usr/lib/ccache:${PATH}',
                'LD_PRELOAD': 'libeatmydata.so:${LD_PRELOAD}',
                'DEBIAN_FRONTEND': 'noninteractive'}

apt_get_options = ['-o', 'Apt::Install-Recommends=false',
                   '-o', 'Apt::Get::Assume-Yes=true',
                   '-o', 'Apt::Get::AllowUnauthenticated=true',
                   '-o', 'DPkg::Options::=--force-confmiss',
                   '-o', 'DPkg::Options::=--force-confnew',
                   '-o', 'DPkg::Options::=--force-overwrite',
                   '-o', 'DPkg::Options::=--force-unsafe-io']
