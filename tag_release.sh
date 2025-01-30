#!/bin/bash
set -e

# make sure the git repo is clean
test -z "$(git status --porcelain)" || echo "Repository is dirty. Aborting." && exit 1

# Get the current version from pyproject.toml and make sure it is a .dev version
version="$(uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version)"
echo "Current Project version is $version"
if [[ ! $version == *".dev"* ]]; then
  echo "$version is no dev version. Aborting."
  exit 1
fi

# Determine release version
version="$(echo $version | sed 's/\.dev.*$//')"
echo "Releasing version: $version"

# Switch pyproject.toml to release version and commit
uvx --from=toml-cli toml set --toml-path=pyproject.toml project.version $version
git commit -am"Tag release version $version"

# Tag this version
tag="v$version"
echo "Creating tag: $tag"
git tag $tag

# Start the next dev version
new_version="$(echo $version | awk -F. '{$NF = $NF + 1;} 1' | sed 's/ /./g')".dev0

echo "Starting new version: $new_version"
uvx --from=toml-cli toml set --toml-path=pyproject.toml project.version $new_version
git commit -am"Start developing version $new_version"

echo "Tag created. Use git push --tags to make this release permanent"



