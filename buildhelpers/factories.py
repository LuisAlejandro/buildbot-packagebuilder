#!/usr/bin/python
# -*- coding: utf-8 -*-

from buildbot.plugins import util, steps

from buildhelpers.commands import (
    test_dpkg_lock, sudo_apt_get_install_slave_extrapackages,
    cowbuilder_create_base_cow_dir, test_base_cow_dir,
    cowbuilder_login_base_cow_dir, test_debian_control, test_configure,
    test_makefile, rsync_base_package, cowbuilder_login_package_cow_dir,
    test_package_cow_dir, gbp_dch, gbp_buildpackage, test_deb_results,
    reprepro_includedeb, apt_get_install_base_cow_extrapackages, useradd,
    apt_get_update, apt_get_dist_upgrade, mk_build_deps_cmd,
    apt_get_install_prebuild_deps, pre_build_script, configure, make,
    checkinstall, cat_deb_version, cat_src_version,
    rm_build_packages, rm_incoming_packages, mkdir_incoming_tree)
from buildhelpers.common import (
    dpkg_lock_extract, base_cow_dir_extract, package_cow_dir_extract,
    debian_control_extract, configure_extract, makefile_extract,
    deb_results_extract, dpkg_lock_exists_not, base_cow_dir_exists_not,
    base_cow_dir_exists, package_cow_dir_exists_not,
    debian_control_and_package_cow_dir_exists, package_cow_dir_exists,
    pre_build_script_exists, debian_control_exists_not,
    deb_version_extract, src_version_extract)
from buildhelpers.config import (incoming_dir_tree, source_dir,
                                 repository, branch, username)

BuildFactory = util.BuildFactory
Property = util.Property
MakeDirectory = steps.MakeDirectory
SetPropertyFromCommand = steps.SetPropertyFromCommand
ShellCommand = steps.ShellCommand
Git = steps.Git
MultipleFileUpload = steps.MultipleFileUpload
MasterShellCommand = steps.MasterShellCommand


# Build factories

maintenance = BuildFactory([

    MakeDirectory(dir=source_dir),

    SetPropertyFromCommand(command=test_dpkg_lock,
                           extract_fn=dpkg_lock_extract,
                           flunkOnFailure=False),

    ShellCommand(name='sudo_apt_get_install_slave_extrapackages',
                 description='Installing slave dependencies.',
                 command=sudo_apt_get_install_slave_extrapackages,
                 doStepIf=dpkg_lock_exists_not),

    SetPropertyFromCommand(command=test_base_cow_dir,
                           extract_fn=base_cow_dir_extract,
                           flunkOnFailure=False),

    ShellCommand(name='cowbuilder_create_base_cow_dir',
                 description='Creating base cowbuilder.',
                 command=cowbuilder_create_base_cow_dir,
                 doStepIf=base_cow_dir_exists_not),

    SetPropertyFromCommand(command=test_base_cow_dir,
                           extract_fn=base_cow_dir_extract,
                           flunkOnFailure=False),

    ShellCommand(name='cowbuilder_login_base_cow_dir_apt_get_update',
                 description='Updating base cowbuilder.',
                 command=cowbuilder_login_base_cow_dir,
                 initialStdin=apt_get_update,
                 doStepIf=base_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_base_cow_dir_apt_get_dist_upgrade',
                 description='Upgrading base cowbuilder.',
                 command=cowbuilder_login_base_cow_dir,
                 initialStdin=apt_get_dist_upgrade,
                 doStepIf=base_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_base_cow_dir_apt_get_install_base_cow_extrapackages',
                 description='Installing base cowbuilder dependencies.',
                 command=cowbuilder_login_base_cow_dir,
                 initialStdin=apt_get_install_base_cow_extrapackages,
                 doStepIf=base_cow_dir_exists),

    ])

packaging = BuildFactory([

    MakeDirectory(dir=source_dir),

    Git(repourl=repository, branch=branch, submodules=True,
        mode='full', method='fresh', workdir=source_dir),

    SetPropertyFromCommand(command=test_package_cow_dir,
                           extract_fn=package_cow_dir_extract,
                           flunkOnFailure=False),

    SetPropertyFromCommand(command=test_debian_control,
                           extract_fn=debian_control_extract,
                           flunkOnFailure=False),

    SetPropertyFromCommand(command=test_configure,
                           extract_fn=configure_extract,
                           flunkOnFailure=False),

    SetPropertyFromCommand(command=test_makefile,
                           extract_fn=makefile_extract,
                           flunkOnFailure=False),

    ShellCommand(name='rsync_base_package',
                 description='Creating package cowbuilder from base.',
                 command=rsync_base_package,
                 doStepIf=package_cow_dir_exists_not),

    ShellCommand(name='cowbuilder_login_package_cow_dir_useradd',
                 description='Creating '+username+' user.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=useradd,
                 doStepIf=package_cow_dir_exists_not),

    SetPropertyFromCommand(command=test_package_cow_dir,
                           extract_fn=package_cow_dir_extract,
                           flunkOnFailure=False),

    ShellCommand(name='cowbuilder_login_package_cow_dir_apt_get_update',
                 description='Updating package cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=apt_get_update,
                 doStepIf=package_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_package_cow_dir_apt_get_dist_upgrade',
                 description='Upgrading package cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=apt_get_dist_upgrade,
                 doStepIf=package_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_package_cow_dir_mk_build_deps',
                 description='Installing build depends inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=mk_build_deps_cmd,
                 doStepIf=debian_control_and_package_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_package_cow_dir_apt_get_install_prebuild_deps',
                 description='Installing prebuild depends inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=apt_get_install_prebuild_deps,
                 doStepIf=package_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_package_cow_dir_pre_build_script',
                 description='Running prebuild script inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=pre_build_script,
                 doStepIf=pre_build_script_exists,
                 timeout=2*60*60),

    ShellCommand(name='cowbuilder_login_package_cow_dir_configure',
                 description='Running "./configure" inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=configure,
                 doStepIf=debian_control_exists_not),

    ShellCommand(name='cowbuilder_login_package_cow_dir_make',
                 description='Running "make" inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=make,
                 doStepIf=debian_control_exists_not),

    SetPropertyFromCommand(command=cat_src_version,
                           extract_fn=src_version_extract,
                           doStepIf=debian_control_exists_not,
                           flunkOnFailure=False),

    ShellCommand(name='cowbuilder_login_package_cow_dir_checkinstall',
                 description='Running "checkinstall" inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=checkinstall,
                 doStepIf=debian_control_exists_not),

    SetPropertyFromCommand(command=cat_deb_version,
                           extract_fn=deb_version_extract,
                           doStepIf=debian_control_and_package_cow_dir_exists,
                           flunkOnFailure=False),

    ShellCommand(name='gbp_dch',
                 description='Generating snapshot entry in debian/changelog.',
                 command=gbp_dch,
                 doStepIf=debian_control_and_package_cow_dir_exists,
                 workdir=source_dir),

    ShellCommand(name='gbp_buildpackage',
                 description='Packaging with gbp-buildpackage on cowbuilder.',
                 command=gbp_buildpackage,
                 doStepIf=debian_control_and_package_cow_dir_exists,
                 workdir=source_dir),

    SetPropertyFromCommand(command=test_deb_results,
                           extract_fn=deb_results_extract,
                           flunkOnFailure=False),

    MasterShellCommand(name='mkdir_incoming_tree',
                       description='Creating incoming folder tree.',
                       command=mkdir_incoming_tree),

    MultipleFileUpload(slavesrcs=Property('deb_results'),
                       masterdest=incoming_dir_tree),

    MasterShellCommand(name='reprepro_includedeb',
                       description='Processing incoming packages to repository.',
                       command=reprepro_includedeb),

    MasterShellCommand(name='rm_incoming_packages',
                       description='Removing packages from incoming directory.',
                       command=rm_incoming_packages),

    ShellCommand(name='rm_build_packages',
                 description='Removing packages from build directory.',
                 command=rm_build_packages),

    ])
