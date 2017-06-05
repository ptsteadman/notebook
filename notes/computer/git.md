# Git and GitHub

`git cherry-pick <commit>` applies another commit, even if it's on another
branch or whatever.

`git push origin :<branch>` deletes a remote branch.

`git reset HEAD~` uncommits the most recent commit so that it can be broken
apart, etc

`git update-index --assume-unchanged path/to/file`

`git branch -m <new-name>` rename branch you're on

`git checkout -b newbranch` to create and checkout a branch in one fell swoop

Add `*.s??` to `~/.gitignore` to globally ignore vim swap files
and then run `git config --global core.excludesfile ~/.gitignore`
