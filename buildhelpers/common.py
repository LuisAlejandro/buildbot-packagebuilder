#!/usr/bin/python
# -*- coding: utf-8 -*-

from buildbot.plugins import util
from buildhelpers.config import (
    sudo, source_dir, base_cow_env, su, username, bash)

Interpolate = util.Interpolate
precmd = []
preenvcmd = ['cd', source_dir.fmtstring, '&&', 'export', base_cow_env, '&&']
presudocmd = [sudo]
presudoenvcmd = ['cd', source_dir.fmtstring, '&&', 'export', base_cow_env, '&&', sudo, '-E']
preusercmd = ['cd', source_dir.fmtstring, '&&',
              su, username, '-s', bash, '-c', "'export", base_cow_env, '&&']


def mkcmd(cmd):
    return Interpolate(' '.join(precmd+cmd))


def mkenvcmd(cmd):
    return Interpolate(' '.join(preenvcmd+cmd))


def mksudocmd(cmd):
    return Interpolate(' '.join(presudocmd+cmd))


def mksudoenvcmd(cmd):
    return Interpolate(' '.join(presudoenvcmd+cmd))


def mkusercmd(cmd):
    return Interpolate(' '.join(preusercmd+cmd+["'"]))


def deb_results_extract(rc, stdout, stderr):
    return {'deb_results': filter(None, stdout.split('\n'))}


def dpkg_lock_extract(rc, stdout, stderr):
    return {'dpkg_lock_exists': (not rc)}


def dpkg_lock_exists(step):
    return step.getProperty('dpkg_lock_exists')


def dpkg_lock_exists_not(step):
    return not dpkg_lock_exists(step)


def base_cow_dir_extract(rc, stdout, stderr):
    return {'base_cow_dir_exists': (not rc)}


def base_cow_dir_exists(step):
    return step.getProperty('base_cow_dir_exists')


def base_cow_dir_exists_not(step):
    return not base_cow_dir_exists(step)


def package_cow_dir_extract(rc, stdout, stderr):
    return {'package_cow_dir_exists': (not rc)}


def package_cow_dir_exists(step):
    return step.getProperty('package_cow_dir_exists')


def package_cow_dir_exists_not(step):
    return not package_cow_dir_exists(step)


def debian_control_extract(rc, stdout, stderr):
    return {'debian_control_exists': (not rc)}


def debian_control_exists(step):
    return step.getProperty('debian_control_exists')


def debian_control_exists_not(step):
    return not debian_control_exists(step)


def configure_extract(rc, stdout, stderr):
    return {'configure_exists': (not rc)}


def configure_exists(step):
    return step.getProperty('configure_exists')


def configure_exists_not(step):
    return not configure_exists(step)


def makefile_extract(rc, stdout, stderr):
    return {'makefile_exists': (not rc)}


def makefile_exists(step):
    return step.getProperty('makefile_exists')


def makefile_exists_not(step):
    return not makefile_exists(step)


def debian_control_and_package_cow_dir_exists(step):
    return (step.getProperty('debian_control_exists') and
            step.getProperty('package_cow_dir_exists'))


def debian_control_and_package_cow_dir_exists_not(step):
    return not debian_control_and_package_cow_dir_exists(step)


def pre_build_deps_exists(step):
    return step.getProperty('prebuild-deps')


def pre_build_script_exists(step):
    return step.getProperty('prebuild-script')


def deb_version_extract(rc, stdout, stderr):
    return {'version': stdout.strip('\n')}


def src_version_extract(rc, stdout, stderr):
    return {'version': stdout.split('=')[1].strip('\n').strip("'")}
