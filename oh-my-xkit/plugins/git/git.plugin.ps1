# Git Plugin - Simple version

# Basic git aliases  
function global:gst { git status }
function global:ga { git add @args }
function global:gc { git commit -m @args }
function global:gp { git push }
function global:gl { git pull }
function global:gb { git branch @args }
function global:gco { git checkout @args }

Write-Verbose "Git plugin loaded"