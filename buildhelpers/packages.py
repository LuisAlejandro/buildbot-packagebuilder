#!/usr/bin/python
# -*- coding: utf-8 -*-

# Estructura de los paquetes que se van a construir
packages = {
    'whatsapp-purple': {
        'repository': 'https://github.com/davidgfnet/whatsapp-purple.git',
        'branch': 'master',
        'prebuild-script': '',
        'prebuild-deps': 'git libglib2.0-dev libpurple-dev libfreeimage-dev'
    }
}
