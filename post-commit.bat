@echo off
setlocal
SET REPOS=%1
SET USER=%2
SET SVN="C:/Program Files/VisualSVN Server/bin/svn.exe"
SET DIR="D:/www/cloudchicken"
(call %SVN% update %DIR% --username wangyong --password wy1001001 --non-interactive)
