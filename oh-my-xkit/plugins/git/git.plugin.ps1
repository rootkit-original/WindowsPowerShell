# Git Plugin for XKit
# Enhanced git functionality

# Git aliases (oh-my-zsh inspired)
function gst { git status @args }
function ga { git add @args }
function gaa { git add --all @args }
function gcmsg { 
    param([string]$Message)
    git commit -m $Message @args 
}
function gp { git push @args }
function gl { git pull @args }
function gb { git branch @args }
function gco { git checkout @args }
function gcb { 
    param([string]$BranchName)
    git checkout -b $BranchName @args
}
function gd { git diff @args }
function gds { git diff --staged @args }
function glog { git log --oneline --decorate --graph @args }

# Advanced git functions
function git-quick-commit {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message
    )
    
    Write-Host "🔄 Adding all changes..." -ForegroundColor Yellow
    git add -A
    
    Write-Host "📝 Committing with message: '$Message'" -ForegroundColor Yellow  
    git commit -m $Message
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Commit successful!" -ForegroundColor Green
    } else {
        Write-Host "❌ Commit failed!" -ForegroundColor Red
    }
}

function git-branch-clean {
    Write-Host "🧹 Cleaning merged branches..." -ForegroundColor Yellow
    
    # Get current branch
    $currentBranch = git rev-parse --abbrev-ref HEAD
    
    # Get merged branches (excluding main, master, develop, current)
    $mergedBranches = git branch --merged | Where-Object { 
        $branch = $_.Trim()
        $branch -notmatch "^\*" -and 
        $branch -notin @("main", "master", "develop", $currentBranch) -and
        $branch -ne ""
    }
    
    if ($mergedBranches) {
        Write-Host "📋 Merged branches to delete:" -ForegroundColor Cyan
        $mergedBranches | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
        
        $confirm = Read-Host "Delete these branches? (y/N)"
        if ($confirm -eq "y" -or $confirm -eq "Y") {
            $mergedBranches | ForEach-Object {
                $branch = $_.Trim()
                Write-Host "🗑️  Deleting branch: $branch" -ForegroundColor Red
                git branch -d $branch
            }
            Write-Host "✅ Branch cleanup complete!" -ForegroundColor Green
        } else {
            Write-Host "❌ Cleanup cancelled" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✅ No merged branches to clean" -ForegroundColor Green
    }
}

function git-info {
    Write-Host "📊 Repository Information" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    
    # Repository path
    $repoRoot = git rev-parse --show-toplevel 2>$null
    if ($repoRoot) {
        Write-Host "📁 Repository: $repoRoot" -ForegroundColor White
    }
    
    # Current branch
    $branch = git rev-parse --abbrev-ref HEAD 2>$null
    if ($branch) {
        Write-Host "🌿 Current Branch: $branch" -ForegroundColor Green
    }
    
    # Remote info
    $remotes = git remote -v 2>$null
    if ($remotes) {
        Write-Host "🌐 Remotes:" -ForegroundColor Blue
        $remotes | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
    }
    
    # Status summary
    $status = git status --porcelain 2>$null
    if ($status) {
        $modified = ($status | Where-Object { $_ -match "^.M" }).Count
        $added = ($status | Where-Object { $_ -match "^A." }).Count  
        $deleted = ($status | Where-Object { $_ -match "^.D" }).Count
        $untracked = ($status | Where-Object { $_ -match "^\?\?" }).Count
        
        Write-Host "📈 Changes:" -ForegroundColor Yellow
        if ($modified -gt 0) { Write-Host "   Modified: $modified" -ForegroundColor Yellow }
        if ($added -gt 0) { Write-Host "   Added: $added" -ForegroundColor Green }
        if ($deleted -gt 0) { Write-Host "   Deleted: $deleted" -ForegroundColor Red }
        if ($untracked -gt 0) { Write-Host "   Untracked: $untracked" -ForegroundColor Magenta }
    } else {
        Write-Host "✅ Working tree clean" -ForegroundColor Green
    }
    
    # Last commit
    $lastCommit = git log -1 --pretty=format:"%h %s (%cr)" 2>$null
    if ($lastCommit) {
        Write-Host "📝 Last Commit: $lastCommit" -ForegroundColor White
    }
}

# Export aliases
New-Alias -Name "gqc" -Value "git-quick-commit" -Force -Scope Global
New-Alias -Name "gbc" -Value "git-branch-clean" -Force -Scope Global
New-Alias -Name "ginfo" -Value "git-info" -Force -Scope Global

# Plugin metadata
$PLUGIN_NAME = "git"
$PLUGIN_AUTHOR = "XKit Team"
$PLUGIN_VERSION = "1.0.0"
$PLUGIN_DESCRIPTION = "Enhanced git functionality and aliases"

Write-Verbose "✅ Loaded plugin: $PLUGIN_NAME v$PLUGIN_VERSION"