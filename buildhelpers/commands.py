#!/usr/bin/python
# -*- coding: utf-8 -*-

from buildhelpers.common import mkcmd
from buildhelpers.config import (
    reprepro, reprepro_dir, incoming_dir, dpkg_lock, base_cow_dir,
    package_cow_dir, source_dir, sudo, rsync, username, bash,
    make, apt_get, apt_get_options, userid, useradd, cowbuilder, architecture,
    distribution, version, git_revision, mirror, git_checkout_dir, ccache_dir,
    gbp, package, checkinstall, pre_build_deps, base_cow_extrapackages,
    slave_extrapackages, parent_source_dir, mk_build_deps, test, grep,
    dpkg_parsechangelog, git, find)


# Commands in master

reprepro_includedeb = mkcmd([reprepro, '-b',
                             reprepro_dir, 'includedeb', 'local',
                             incoming_dir+'/*.deb'])

rm_incoming_packages = mkcmd([find, incoming_dir, '-type', 'f',
                              '-iname', '*.deb', '-iname', '*.build',
                              '-iname', '*.dsc', '-iname', '*.tar.gz',
                              '-iname', '*.changes',
                              '-exec', 'rm', '-vf', '{}', '\;'])

# Commands inside a slave cowbuilder with root priviledges
# passed through stdin to cowbuilder --login

useradd = mkcmd([useradd, '--uid', str(userid), username])

apt_get_update = mkcmd([apt_get]+apt_get_options+['update'])

apt_get_install_base_cow_extrapackages = mkcmd(
    [apt_get] + apt_get_options + ['install'] + base_cow_extrapackages)

apt_get_install_slave_extrapackages = mkcmd(
    [apt_get] + apt_get_options + ['install'] + slave_extrapackages)

apt_get_install_prebuild_deps = mkcmd(
    [apt_get] + apt_get_options + ['install'] + [pre_build_deps.fmtstring])

apt_get_dist_upgrade = mkcmd([apt_get] + apt_get_options + ['dist-upgrade'])

mk_build_deps_cmd = mkcmd([mk_build_deps, '--install', '--remove',
                          '--tool', '"'+apt_get] + apt_get_options +
                          ['"'] + [source_dir.fmtstring + '/debian/control'])

checkinstall = mkcmd(['cd', source_dir.fmtstring, '&&',
                      checkinstall, '--default', '--deldoc', '--deldesc',
                      '--type', 'debian', '--pakdir', '..',
                      '--pkgname', package.fmtstring,
                      '--pkgversion',
                      version.fmtstring+'~1.chki'+git_revision.fmtstring,
                      make, 'install'])

# Commands inside a slave cowbuilder as the buildbot user
# passed through stdin to cowbuilder --login

pre_build_script = mkcmd(['su', username, '-s', bash, '-c',
                          '"cd', source_dir.fmtstring, '&&',
                          '%(prop:prebuild-script)s"'])

configure = mkcmd(['su', username, '-s', bash, '-c',
                   '"cd', source_dir.fmtstring, '&&', './configure"'])

make = mkcmd(['su', username, '-s', bash, '-c',
              '"cd', source_dir.fmtstring, '&&', make+'"'])


# Commands in slave

rm_build_packages = mkcmd([find, parent_source_dir.fmtstring, '-type', 'f',
                           '-iname', '*.deb', '-iname', '*.build',
                           '-iname', '*.dsc', '-iname', '*.tar.gz',
                           '-iname', '*.changes',
                           '-exec', 'rm', '-vf', '{}', '\;'])

test_deb_results = mkcmd([find, parent_source_dir.fmtstring+'/*.deb',
                          '-maxdepth', '1', '-type', 'f',
                          '-printf', '"%%p\n"'])

test_dpkg_lock = mkcmd([test, '-e', dpkg_lock])

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

git_revparse = mkcmd([git, '--git-dir', source_dir.fmtstring+'/.git',
                      'rev-parse', 'HEAD'])

rsync_base_package = mkcmd([sudo, rsync, '-a', base_cow_dir.fmtstring+'/',
                            package_cow_dir.fmtstring])

sudo_apt_get_update = mkcmd([sudo, apt_get_update.fmtstring])

sudo_apt_get_dist_upgrade = mkcmd([sudo, apt_get_dist_upgrade.fmtstring])

sudo_apt_get_install_base_cow_extrapackages = mkcmd([
    sudo, apt_get_install_base_cow_extrapackages.fmtstring])

sudo_apt_get_install_slave_extrapackages = mkcmd([
    sudo, apt_get_install_slave_extrapackages.fmtstring])

cowbuilder_create_base_cow_dir = mkcmd([
    sudo, cowbuilder, '--create',
    '--basepath', base_cow_dir.fmtstring,
    '--architecture', architecture.fmtstring,
    '--distribution', distribution.fmtstring,
    '--aptcache', '""',
    '--components', 'main',
    '--mirror', mirror])

cowbuilder_login_base_cow_dir = mkcmd([
    sudo, cowbuilder, '--login',
    '--basepath', base_cow_dir.fmtstring,
    '--aptcache', '""',
    '--bindmounts', '"'+git_checkout_dir+' '+ccache_dir+'"',
    '--save-after-login'])

cowbuilder_login_package_cow_dir = mkcmd([
    sudo, cowbuilder, '--login',
    '--basepath', package_cow_dir.fmtstring,
    '--aptcache', '""',
    '--bindmounts', '"'+git_checkout_dir+' '+ccache_dir+'"',
    '--save-after-login'])

gbp_dch = mkcmd([
    gbp, 'dch',
    '--snapshot', '--auto', '--id-length', '7', '--full', '--git-author'])


gbp_buildpackage = mkcmd([
    gbp, 'buildpackage',
    '--git-purge',
    '--git-ignore-new',
    '--git-no-create-orig',
    '--git-pbuilder',
    '--git-dist=buildbot-'+package.fmtstring+'_slave-'+distribution.fmtstring,
    '--git-arch='+architecture.fmtstring,
    '-us', '-uc', '-nc', '-d'])
