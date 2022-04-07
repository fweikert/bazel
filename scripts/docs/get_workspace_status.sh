if [ -d .git ] || git rev-parse --git-dir > /dev/null 2>&1; then
  git_rev=$(git rev-parse --abbrev-ref HEAD)
  if [[ $? != 0 ]];
  then
      exit 1
  fi
  echo "BUILD_SCM_REVISION ${git_rev}"
else
  echo "BUILD_SCM_REVISION no_git"
fi;
