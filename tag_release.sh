#!/bin/bash
set -e

RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[94m"
ENDCOLOR="\e[0m"

# make sure the git repo is clean
test -z "$(git status --porcelain)" || (echo -e "${RED}Repository is dirty. Aborting. ${ENDCOLOR}" && exit 1)

# store current git hash for undo command
current_git_hash=$(git show --oneline -s | cut -f 1 -d" ")
undo_command="git reset --hard $current_git_hash"
echo -e "If anything goes wrong use $BLUE $undo_command $ENDCOLOR to reset your repository."

# Get the current version from pyproject.toml and make sure it is a .dev version
version="$(uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version)"
echo "Current Project version is $version"
if [[ !  $version == *".dev"* ]]; then
  echo -e "${RED}$version is no dev version. Aborting.${ENDCOLOR}"
  exit 1
fi

# Determine release version
version="$(echo $version | sed 's/\.dev.*$//')"

# Ask user
echo -e "Release version ${GREEN} $version ${ENDCOLOR} ? [y/N]"
read answer
if  [[ ! $answer =~ ^[Yy]$ ]] ; then
  echo "Aborted" && exit 1
fi

# Switch pyproject.toml to release version and commit
uvx --from=toml-cli toml set --toml-path=pyproject.toml project.version $version
git commit -am"chore(tag_release): tag release version $version"

# Tag this version
tag="v$version"
echo "Creating tag: $tag"
git tag $tag

# Start the next dev version
new_version="$(echo $version | awk -F. '{$NF = $NF + 1;} 1' | sed 's/ /./g')".dev0

echo "Starting new version: $new_version"
uvx --from=toml-cli toml set --toml-path=pyproject.toml project.version $new_version
git commit -am"chore(tag_release): start developing version $new_version"

echo -e "Tag created. Use $BLUE git push --tags $ENDCOLOR to make this release permanent"
echo -e "Or undo all changes with $GREEN $undo_command && git tag --delete $tag $ENDCOLOR"

