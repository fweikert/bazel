#if [ -d .git ] || git rev-parse --git-dir > /dev/null 2>&1; then
#  git_rev=$(git rev-parse --abbrev-ref HEAD)
#  if [[ $? != 0 ]];
#  then
#      exit 1
#  fi
#  echo "BUILD_SCM_REVISION ${git_rev}"
#else
#  echo "BUILD_SCM_REVISION no_git"
#fi;

## TODO: remove
echo BUILD_SCM_REVISION "$(git rev-parse --abbrev-ref HEAD)"
exit 0

RELEASE_NAME=$(source scripts/release/common.sh; get_full_release_name)

if [[ -z "$RELEASE_NAME" ]]; then
  echo "Failed to get a release name, are you on a release branch?"
  exit 1
else
  echo "BUILD_SCM_REVISION $RELEASE_NAME"
fi
