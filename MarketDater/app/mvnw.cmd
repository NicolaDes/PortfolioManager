@echo off
setlocal

set BASEDIR=%~dp0

set MAVEN_OPTS=-Xmx1024m
cmd.exe /C "%BASEDIR%mvnw.cmd" %*
