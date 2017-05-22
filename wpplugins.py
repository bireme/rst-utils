#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Instruções de uso:
# -> Basta executar esse script utilizando o parâmetro "install" para instalar os plugins homologados de uma instância WP
# -> Exemplo: python wpplugins.py install

# -> Caso queira instalar um novo plugin, passar como parâmetros a palavra "checkout" (se for um plugin versionado no SVN) ou "clone" (se for um plugin versionado no GitHub) e também o nome do diretório de instalação do plugin
# -> Exemplo 1: python wpplugins.py clone <dir_name>
# -> Exemplo 2: python wpplugins.py checkout <dir_name>

# -> Para atualizar todos os plugins instalados, envie como parâmetro a palavra "update"
# -> Exemplo: python wpplugins.py update

# -> Para instalar os arquivos de tradução da área administrativa do WordPress, envie como parâmetro a palavra "translate" e a versão do WordPress
# -> Exemplo: python wpplugins.py translate 4.1

# -> Caso queira verificar as versões de arquivos de tradução do WordPress que estão versionadas no repositório, utilize os parâmetros "translate" e "list", respectivamente
# -> Exemplo: python wpplugins.py translate list

# -> OBS: Executar o script dentro do diretório htdocs/wp-content/ da instância.
# -> Para saber mais sobre tradução do WordPress, além de informações sobre plugins homologados e não homologados, acesse a wiki abaixo:
# -> http://wiki.bireme.org/intranet/index.php/Wordpress-plugins

import re
import os
import sys
import urllib2
import commands
#import requests
#import lxml
#from lxml import html

# VARIAVEIS GLOBAIS
#pattern = re.compile('name="rev" value="(.*?)"')
#r = urllib2.urlopen("http://trac.reddes.bvsalud.org/projects/rede-sup-tecnico/log/branches")
#LAST_REVISION = pattern.findall(r.read())
#r.close()
#WP_ADMIN_FILES = "http://trac.reddes.bvsalud.org/projects/rede-sup-tecnico/export/"+LAST_REVISION[0]+"/tags/wp-translate-files/"

#LAST_REVISION  = commands.getoutput("svn info --xml http://svn.reddes.bvsalud.org/rede-sup-tecnico | grep revision | head -1 | grep -Eo '[0-9]+'")
#WP_ADMIN_FILES = "http://trac.reddes.bvsalud.org/projects/rede-sup-tecnico/export/"+LAST_REVISION+"/tags/wp-translate-files/"

#r = requests.get('http://trac.reddes.bvsalud.org/projects/rede-sup-tecnico/log/branches')
#tree = lxml.html.fromstring(r.content)
#element = tree.get_element_by_id('rev')
#LAST_REVISION = element.attrib['value']
#WP_ADMIN_FILES = "http://trac.reddes.bvsalud.org/projects/rede-sup-tecnico/export/"+LAST_REVISION+"/tags/wp-translate-files/"

# Arquivos de tradução da área administrativa
LANGUAGES = {
    'Português': 'pt_BR.tar.gz',
    'Espanhol' : 'es_ES.tar.gz',
    'Francês'  : 'fr_FR.tar.gz',
    }

# Plugins que serão instalados
PLUGINS = (
    'multi-language-framework',
    'ultimate-posts-widget',
    'page-links-to',
    'contact-form-7',
    'wp-mail-smtp',
    'better-wp-security',
    'google-analytics-for-wordpress',
    'user-role-editor',
    )

def version():
    '''
    Função que mostra a versão do script
    '''
    __version_info__ = ['1', '0', '2']

    if __version_info__[-1] == '0':
        del __version_info__[-1]

    __version__ = '.'.join(__version_info__)
    print ("Version: "+__version__)
    exit()

def assistFunction():
    '''
    Função que mostra informações sobre o uso correto do script
    '''
    print ("Para instalar os plugins homologados, envie como parâmetro a palavra \"install\".\n")
    print ("* Exemplo: python wpplugins.py install \n")
    print ("Serão instalados os seguintes plugins: \n")
    print (" - BVS-Site ")
    print (" - Multi Language Framework ")
    print (" - Ultimate Posts Widget ")
    print (" - Page Links To ")
    print (" - Contact Form 7 ")
    print (" - WP Mail SMTP ")
    print (" - iThemes Security ")
    print (" - Google Analytics For WordPress ")
    print (" - User Role Editor \n")
    print ("Para instalar plugins não homologados, envie como parâmetros a palavra \"checkout\" (se for um plugin versionado no SVN) ou \"clone\" (se for um plugin versionado no GitHub) e também o nome do diretório de instalação do plugin.\n")
    print ("* Exemplo 1: python wpplugins.py clone <dir_name> ")
    print ("* Exemplo 2: python wpplugins.py checkout <dir_name> \n")
    print ("Para atualizar todos os plugins instalados, envie como parâmetro a palavra \"update\".\n")
    print ("* Exemplo: python wpplugins.py update \n")
    print ("Para instalar os arquivos de tradução da área administrativa do WordPress, envie como parâmetro a palavra \"translate\" e a versão do WordPress.\n")
    print ("* Exemplo: python wpplugins.py translate 4.1 \n")
    print ("Caso queira verificar as versões de arquivos de tradução do WordPress que estão versionadas no repositório, utilize os parâmetros \"translate\" e \"list\", respectivamente.\n")
    print ("* Exemplo: python wpplugins.py translate list \n")
    print ("Para saber mais sobre tradução do WordPress, além de informações sobre plugins homologados e não homologados, acesse a wiki abaixo: \n")
    print ("http://wiki.bireme.org/intranet/index.php/Wordpress-plugins \n")

def installPlugin(*args):
    '''
    Função que realiza o checkout do SVN
    '''
    plugin = args[1]
    name = plugin.replace('-',' ')
    name = name.upper()
    print ("* Instalando plugin "+name+"... ")
    if os.path.exists("plugins/"+plugin) == True:
        print("AVISO: Plugin "+name+" já está instalado.\n")
    else:
        if args[0] == "checkout":    
            os.system("svn co http://plugins.svn.wordpress.org/"+plugin+"/trunk plugins/"+plugin)
        elif args[0] == "clone":
            if plugin == "lis":
                plugin = "lis-wp-plugin"
            elif plugin == "direve":
                plugin = "direve-wp-plugin"
            elif plugin == "bvs" or plugin == "bvs-site":
                plugin = "bvs-site-wp-plugin"
            os.system("git clone git://github.com/bireme/"+plugin+".git plugins/"+plugin)
        print ("[OK] \n")

def translateAdmin(args, str):
    '''
    Função que instala os arquivos de tradução do WordPress Admin
    '''
    if str == "list":
        regex = re.compile('<a class="dir" .*?>(.*?)</a>')
        l = urllib2.urlopen(WP_ADMIN_FILES)
        TAGS = regex.findall(l.read())
        l.close()

        if not TAGS:
            print ("Nenhuma versão de arquivos de tradução do WordPress foi encontrada no repositório... \n")
            exit()
        else:
            print ("# LISTA DE VERSÕES #")
            for x in TAGS:
                print (" - " + x)
            print
    else:
        # Adicionando arquivos de tradução
        print ("* Adicionando arquivos de tradução da área administrativa do WordPress *\n")

        version = str
        files = WP_ADMIN_FILES+version+"/"+args[1]
        status = os.system("wget -q --spider "+files)

        if status > 0:
            print("AVISO: Essa versão de WordPress não está versionada ou não existe... \n")
            exit()
        else:
            print ("---------------------------------------------------------------------------------------------------------------------")
            print ("Instalando arquivos de tradução para o idioma "+args[0]+" da versão "+version+" do WordPress")
            print ("--------------------------------------------------------------------------------------------------------------------- \n")
            os.system("wget "+files)
            os.system("tar xvzf "+args[1])
            os.system("rm "+args[1])
            print ("[OK] \n")
            print ("# PROCEDIMENTO FINALIZADO!!!! # \n")

def updatePlugins(arg):
    '''
    Função que atualiza todos os plugins instalados
    '''
    name = arg.split('/')[1]
    name = name.replace('-',' ')
    name = name.upper()
    print ("* Atualizando plugin "+name+"... ")
    savedPath = os.getcwd()
    os.chdir(arg)
    if os.path.exists(".git") == True:
        os.system("git pull")
        print ("[OK] \n")
    elif os.path.exists(".svn") == True:
        os.system("svn up")
        print ("[OK] \n")
    else:
        print("AVISO: Plugin "+name+" não está versionado.\n")
    os.chdir(savedPath)

def is_writable(file):
    '''
    Função que verifica se um arquivo possui permissão de escrita
    '''
    if os.path.isdir(file):
        name = "diretório"
    elif os.path.isfile(file):
        name = "arquivo"

    if not os.access(file, os.W_OK):
        print("AVISO: O "+name+" '"+file+"' não possui permissão de escrita.\n")
        exit()
   
# ÍNICIO DO SCRIPT
if __name__ == '__main__':

    if len(sys.argv) == 2:
        if sys.argv[1] == "version":
            version()

    os.system("clear")

    print ("#===============================================================================#")
    print ("# INSTALAÇÃO AUTOMÁTICA DOS PLUGINS HOMOLOGADOS PARA UMA INSTÂNCIA EM WORDPRESS #")
    print ("#===============================================================================#\n")

    #if os.getcwd().split('/')[-1] != "wp-content":
    path, file = os.path.split(os.getcwd())
    if file != "wp-content":
        print("AVISO: Esse script não pode ser executado nesse diretório. Interrompendo execução... \n")
        exit()

    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            if sys.argv[1] == "install":
                is_writable("plugins/")
                installPlugin("clone", "bvs")

                for x in PLUGINS:
                    installPlugin("checkout", x)

                print ("# PROCEDIMENTO FINALIZADO!!!! # \n")

            elif sys.argv[1] == "update":
                # Atualizando os plugins instalados no WordPress
                print ("--------------------------------------")
                print ("* Atualização dos plugins instalados *")
                print ("--------------------------------------\n")

                is_writable("plugins/")
                DIRS = commands.getoutput('ls -d plugins/*/ ').split('\n')

                for x in DIRS:
                    updatePlugins(x)

                print ("# PROCEDIMENTO FINALIZADO!!!! # \n")

            else:
                assistFunction()

        # Instalando plugins não homologados
        if len(sys.argv) == 3:
            if sys.argv[1] == "clone" or sys.argv[1] == "checkout":
                is_writable("plugins/")

                name = sys.argv[2].replace('-',' ')
                name = name.upper()

                if os.path.exists("plugins/"+sys.argv[2]) == True:
                    print("AVISO: Plugin "+name+" já está instalado.\n")
                    exit();
                else:
                    installPlugin(sys.argv[1], sys.argv[2])
                    print ("# PROCEDIMENTO FINALIZADO!!!! # \n")

            elif sys.argv[1] == "translate":
                for x in LANGUAGES.items():
                    translateAdmin(x, sys.argv[2])
                    if sys.argv[2] == "list": break

            else:
                assistFunction()

    else:
        assistFunction() 
