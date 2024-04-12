# Command useful

### Clean branch git (interface visual studio code)
- Cliquer sur git graph choisir le dernier commit de la branch cible
- Clique droit + reset current branch + hard
- Git push

———————————————
Merge commit into 1
———————————————
##### 1°) Delete unecessary commit form history
git reset --soft HEAD~2
git commit —amend
git push
#### 2°) keep only 1 commit and add new one into last commit message
Git add .
Git commit —amend —no-edit
Git push

# Exclure un dossier qu’on ne veut pas push
Exclure des fichiers
vim .git/info/exclude





