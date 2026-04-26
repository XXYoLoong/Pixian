param(
  [string]$RepoUrl = "https://github.com/XXYoLoong/Pixian.git"
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Test-Path ".git")) {
  git init
}

git add .
git commit -m "Initial Pixian release" 2>$null

$remoteExists = git remote | Select-String -Pattern "^origin$"
if (-not $remoteExists) {
  git remote add origin $RepoUrl
} else {
  git remote set-url origin $RepoUrl
}

git branch -M main
git push -u origin main
