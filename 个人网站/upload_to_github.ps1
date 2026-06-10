$ErrorActionPreference = 'Stop'

$remoteUrl = 'ssh://git@ssh.github.com:443/xiaosheng258/HYM_first.git'
$branch = 'main'

if (-not (Test-Path '.git')) {
    git init -b $branch
}

git branch -M $branch

$remoteNames = git remote
if ($remoteNames -contains 'origin') {
    git remote set-url origin $remoteUrl
} else {
    git remote add origin $remoteUrl
}

git add -A

$status = git status --porcelain
if ($status) {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    git commit -m "Upload personal site $stamp"
}

git push origin "$branch`:$branch" --force
