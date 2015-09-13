#!/usr/bin/python
# -*- coding: utf-8 -*-

from buildbot.plugins.util import BuildFactory, Property
from buildbot.plugins.steps import (SetPropertyFromCommand, ShellCommand, Git,
                                    MultipleFileUpload, MasterShellCommand)
from buildhelpers.commands import (
    test_dpkg_lock, sudo_apt_get_install_slave_extrapackages,
    cowbuilder_create_base_cow_dir, test_base_cow_dir,
    cowbuilder_login_base_cow_dir, test_debian_control, test_configure,
    test_makefile, rsync_base_package, cowbuilder_login_package_cow_dir,
    test_package_cow_dir, git_buildpackage, test_deb_results,
    reprepro_includedeb, apt_get_install_base_cow_extrapackages,
    useradd, apt_get_update, apt_get_dist_upgrade, mk_build_deps_cmd,
    apt_get_install_prebuild_deps, pre_build_script, configure, make,
    checkinstall)
from buildhelpers.common import (
    dpkg_lock_extract, base_cow_dir_extract, package_cow_dir_extract,
    debian_control_extract, configure_extract, makefile_extract,
    deb_results_extract, dpkg_lock_exists_not, base_cow_dir_exists_not,
    base_cow_dir_exists, package_cow_dir_exists_not,
    debian_control_and_package_cow_dir_exists, package_cow_dir_exists,
    pre_build_script_exists, debian_control_exists_not)
from buildhelpers.config import (base_cow_env, incoming_dir, source_dir,
                                 repository, branch, username)

# Build factories

maintenance = BuildFactory([

    SetPropertyFromCommand(command=test_dpkg_lock,
                           extract_fn=dpkg_lock_extract,
                           flunkOnFailure=False),

    ShellCommand(name='sudo_apt_get_install_slave_extrapackages',
                 description='Installing slave dependencies.',
                 command=sudo_apt_get_install_slave_extrapackages,
                 env=base_cow_env, doStepIf=dpkg_lock_exists_not),

    SetPropertyFromCommand(command=test_base_cow_dir,
                           extract_fn=base_cow_dir_extract,
                           flunkOnFailure=False),

    ShellCommand(name='cowbuilder_create_base_cow_dir',
                 description='Creating base cowbuilder.',
                 command=cowbuilder_create_base_cow_dir,
                 env=base_cow_env, doStepIf=base_cow_dir_exists_not),

    SetPropertyFromCommand(command=test_base_cow_dir,
                           extract_fn=base_cow_dir_extract,
                           flunkOnFailure=False),

    ShellCommand(name='cowbuilder_login_base_cow_dir_apt_get_update',
                 description='Updating base cowbuilder.',
                 command=cowbuilder_login_base_cow_dir,
                 initialStdin=apt_get_update,
                 env=base_cow_env, doStepIf=base_cow_dir_exists,
                 flunkOnFailure=False),

    ShellCommand(name='cowbuilder_login_base_cow_dir_apt_get_dist_upgrade',
                 description='Upgrading base cowbuilder.',
                 command=cowbuilder_login_base_cow_dir,
                 initialStdin=apt_get_dist_upgrade,
                 env=base_cow_env, doStepIf=base_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_base_cow_dir_apt_get_install_base_cow_extrapackages',
                 description='Installing base cowbuilder dependencies.',
                 command=cowbuilder_login_base_cow_dir,
                 initialStdin=apt_get_install_base_cow_extrapackages,
                 env=base_cow_env, doStepIf=base_cow_dir_exists),

    ])

packaging = BuildFactory([

    Git(repourl=repository, branch=branch, submodules=True, shallow=True,
        mode='full', method='clobber', workdir=source_dir),

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
                 env=base_cow_env, doStepIf=package_cow_dir_exists_not,
                 flunkOnFailure=False),

    SetPropertyFromCommand(command=test_package_cow_dir,
                           extract_fn=package_cow_dir_extract,
                           flunkOnFailure=False),

    ShellCommand(name='cowbuilder_login_package_cow_dir_apt_get_update',
                 description='Updating package cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=apt_get_update,
                 env=base_cow_env, doStepIf=package_cow_dir_exists,
                 flunkOnFailure=False),

    ShellCommand(name='cowbuilder_login_package_cow_dir_apt_get_dist_upgrade',
                 description='Upgrading package cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=apt_get_dist_upgrade,
                 env=base_cow_env, doStepIf=package_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_package_cow_dir_mk_build_deps',
                 description='Installing build depends inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=mk_build_deps_cmd, env=base_cow_env,
                 doStepIf=debian_control_and_package_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_package_cow_dir_apt_get_install_prebuild_deps',
                 description='Installing prebuild depends inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=apt_get_install_prebuild_deps,
                 env=base_cow_env, doStepIf=package_cow_dir_exists),

    ShellCommand(name='cowbuilder_login_package_cow_dir_pre_build_script',
                 description='Running prebuild script inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=pre_build_script,
                 doStepIf=pre_build_script_exists,
                 env=base_cow_env, timeout=2*60*60),

    ShellCommand(name='cowbuilder_login_package_cow_dir_configure',
                 description='Running "./configure" inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=configure,
                 doStepIf=debian_control_exists_not,
                 env=base_cow_env),

    ShellCommand(name='cowbuilder_login_package_cow_dir_make',
                 description='Running "make" inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=make,
                 doStepIf=debian_control_exists_not,
                 env=base_cow_env),

    ShellCommand(name='cowbuilder_login_package_cow_dir_checkinstall',
                 description='Running "checkinstall" inside cowbuilder.',
                 command=cowbuilder_login_package_cow_dir,
                 initialStdin=checkinstall,
                 doStepIf=debian_control_exists_not,
                 env=base_cow_env),

    ShellCommand(name='git_buildpackage',
                 description='Packaging with git-buildpackage on cowbuilder.',
                 command=git_buildpackage,
                 doStepIf=debian_control_and_package_cow_dir_exists,
                 env=base_cow_env, workdir=source_dir),

    SetPropertyFromCommand(command=test_deb_results,
                           extract_fn=deb_results_extract,
                           workdir=source_dir,
                           flunkOnFailure=False),

    MultipleFileUpload(slavesrcs=Property('deb_results'),
                       masterdest=incoming_dir),

    MasterShellCommand(name='reprepro_includedeb',
                       description='Processing incoming packages to repository.',
                       command=reprepro_includedeb,
                       flunkOnFailure=False),

    ])
