# Docker Plugin - Simple version

# Docker aliases
function global:d { docker @args }
function global:dps { docker ps @args }
function global:di { docker images @args }

# Podman aliases (if available)
if (Get-Command podman -ErrorAction SilentlyContinue) {
    function global:p { podman @args }
    function global:pps { podman ps @args }
    function global:pi { podman images @args }
}

Write-Verbose "Docker plugin loaded"