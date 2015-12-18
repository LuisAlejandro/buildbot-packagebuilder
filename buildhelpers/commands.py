#!/usr/bin/python
# -*- coding: utf-8 -*-

from buildhelpers.common import (
    mkcmd, mkenvcmd, mkusercmd, mksudocmd, mksudoenvcmd)
from buildhelpers.config import (
    reprepro, reprepro_dir, incoming_dir_tree, dpkg_lock, base_cow_dir,
    package_cow_dir, source_dir, rsync, username, make, apt_get,
    apt_get_options, userid, useradd, cowbuilder, architecture, distribution,
    version, git_revision, mirror, git_checkout_dir, ccache_dir, gbp, package,
    checkinstall, pre_build_deps, base_cow_extrapackages, slave_extrapackages,
    parent_source_dir, mk_build_deps, test, grep, dpkg_parsechangelog,
    find, timestamp, mkdir, fuser)


# Commands in master

mkdir_incoming_tree = mkcmd([mkdir, '-p', incoming_dir_tree.fmtstring])

reprepro_includedeb = mkcmd([reprepro, '-b',
                             reprepro_dir, 'includedeb', 'local',
                             incoming_dir_tree.fmtstring+'/*.deb'])

rm_incoming_packages = mkcmd([find, incoming_dir_tree.fmtstring, '-type', 'f',
                              '-regextype', 'posix-extended',
                              '-iregex', '".*\.(deb|dsc|gz|changes|build)"',
                              '-exec', 'rm', '-vf', '{}', '\;'])

# Commands inside a slave cowbuilder with root priviledges
# passed through stdin to cowbuilder --login

useradd = mkenvcmd([useradd, '--uid', str(userid), username])

apt_get_update = mkenvcmd([apt_get]+apt_get_options+['update'])

apt_get_install_base_cow_extrapackages = mkenvcmd(
    [apt_get] + apt_get_options + ['install'] + base_cow_extrapackages)

apt_get_install_slave_extrapackages = mkenvcmd(
    [apt_get] + apt_get_options + ['install'] + slave_extrapackages)

apt_get_install_prebuild_deps = mkenvcmd(
    [apt_get] + apt_get_options + ['install'] + [pre_build_deps.fmtstring])

apt_get_dist_upgrade = mkenvcmd([apt_get] + apt_get_options + ['dist-upgrade'])

mk_build_deps_cmd = mkenvcmd(
    [mk_build_deps, '--install', '--remove', '--tool', '"'+apt_get] +
    apt_get_options + ['"'] + [source_dir.fmtstring + '/debian/control'])

checkinstall = mkenvcmd(
    [checkinstall, '--default', '--deldoc', '--deldesc', '--type', 'debian',
     '--pakdir', '..', '--pkgname', package.fmtstring, '--pkgversion',
     version.fmtstring+'+'+timestamp+'~1.chki'+git_revision.fmtstring,
     make, 'install'])

# Commands inside a slave cowbuilder as the buildbot user
# passed through stdin to cowbuilder --login

pre_build_script = mkusercmd(['%(prop:prebuild-script)s'])

configure = mkusercmd(['./configure'])

make = mkusercmd([make])


# Commands in slave outside cowbuilder

rm_build_packages = mkcmd([find, parent_source_dir.fmtstring, '-type', 'f',
                           '-regextype', 'posix-extended',
                           '-iregex', '".*\.(deb|dsc|gz|changes|build)"',
                           '-exec', 'rm', '-vf', '{}', '\;'])

test_deb_results = mkcmd([find, parent_source_dir.fmtstring+'/*.deb',
                          '-maxdepth', '1', '-type', 'f',
                          '-printf', '"%%p\n"'])

test_dpkg_lock = mksudocmd([fuser, dpkg_lock])

test_base_cow_dir = mkcmd([test, '-e', base_cow_dir.fmtstring])

test_package_cow_dir = mkcmd([test, '-e', package_cow_dir.fmtstring])

test_debian_control = mkcmd([test, '-e',
                             source_dir.fmtstring+'/debian/control'])

test_makefile = mkcmd([test, '-e', source_dir.fmtstring+'/Makefile'])

test_configure = mkcmd([test, '-e', source_dir.fmtstring+'/configure'])

cat_deb_version = mkcmd([dpkg_parsechangelog,
                         '-l', source_dir.fmtstring+'/debian/changelog',
                         '-S', 'Version'])

cat_src_version = mkcmd([grep, '"PACKAGE_VERSION="',
                         source_dir.fmtstring+'/configure'])


# Commands in slave outside cowbuilder with sudo priviledges

rsync_base_package = mksudocmd([rsync, '-avz', base_cow_dir.fmtstring+'/',
                                package_cow_dir.fmtstring])

sudo_apt_get_install_slave_extrapackages = mksudoenvcmd(
    [apt_get] + apt_get_options + ['install'] + slave_extrapackages)

cowbuilder_create_base_cow_dir = mksudocmd([
    cowbuilder, '--create',
    '--basepath', base_cow_dir.fmtstring,
    '--architecture', architecture.fmtstring,
    '--distribution', distribution.fmtstring,
    '--aptcache', '""',
    '--components', 'main',
    '--mirror', mirror])

cowbuilder_login_base_cow_dir = mksudocmd([
    cowbuilder, '--login',
    '--basepath', base_cow_dir.fmtstring,
    '--aptcache', '""',
    '--bindmounts', '"'+git_checkout_dir+' '+ccache_dir+'"',
    '--save-after-login'])

cowbuilder_login_package_cow_dir = mksudocmd([
    cowbuilder, '--login',
    '--basepath', package_cow_dir.fmtstring,
    '--aptcache', '""',
    '--bindmounts', '"'+git_checkout_dir+' '+ccache_dir+'"',
    '--save-after-login'])

gbp_dch = mkenvcmd([
    gbp, 'dch',
    '--new-version', version.fmtstring+'+'+timestamp,
    '--id-length', '7',
    '--snapshot', '--auto',
    '--full', '--git-author'])

gbp_buildpackage = mkenvcmd([
    gbp, 'buildpackage',
    '--git-purge',
    '--git-ignore-new',
    '--git-no-create-orig',
    '--git-pbuilder',
    '--git-pbuilder-options="--hookdir="',
    '--git-dist=buildbot-'+package.fmtstring+'_slave-'+distribution.fmtstring,
    '--git-arch='+architecture.fmtstring,
    '-us', '-uc', '-nc', '-d'])
