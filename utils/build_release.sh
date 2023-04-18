#!/bin/bash

NAME="wrh_organization"
CUR_DIR=$(dirname -- "$0")

cd ${CUR_DIR}
cd ..
BASE_DIR=$(pwd)
FRONTEND_DIR=${BASE_DIR}/wrh_organization/FRONTEND/wrh_organization_ui

FE_INC_VER_TYPE=patch
BE_INC_VER_TYPE=patch
PREV_RELEASE_COMMIT=$(git log master --grep "\[RELEASE VERSION\]" -1 --format=format:"%H")
echo "Check for Frontend Diff"
FE_HAS_COMMIT=$(git diff --quiet ${PREV_RELEASE_COMMIT} -- ${FRONTEND_DIR}  || echo changed)
echo "Check for Backend Diff"
BE_HAS_COMMIT=$(git diff --quiet ${PREV_RELEASE_COMMIT} -- ${BASE_DIR} ':!wrh_organization/FRONTEND/wrh_organization_ui'  || echo changed)
if [ -z "${FE_HAS_COMMIT}" ]; then
  FE_INC_VER_TYPE="ignore"
fi
if [ -z "${BE_HAS_COMMIT}" ]; then
  BE_INC_VER_TYPE="ignore"
fi

while [ "$1" != "" ]; do
  PARAM=$(echo $1 | awk -F= '{print $1}')
  VALUE=$(echo $1 | awk -F= '{print $2}')
  case $PARAM in
  --fe-inc-ver)
    FE_INC_VER_TYPE=$VALUE
    ;;
  --be-inc-ver)
    BE_INC_VER_TYPE=$VALUE
    ;;
  esac
  shift
done

git checkout master
git pull

cd ./wrh_organization

BACKEND_VERSION=$(cat ./VERSION)
NEW_BACKEND_VERSION=${BACKEND_VERSION}
echo "#############################################"
echo "Current backend version: ${BACKEND_VERSION}"
echo "##############################################"
if [ "${BE_INC_VER_TYPE}" != 'ignore' ]; then
  echo "Bumping backend version: ${BE_INC_VER_TYPE} ..."
  NEW_BACKEND_VERSION=$(pysemver bump ${BE_INC_VER_TYPE} ${BACKEND_VERSION})
  echo "New backend version: ${NEW_BACKEND_VERSION}"
  echo ${NEW_BACKEND_VERSION} >./VERSION
fi

echo "#############################################"
cd ${FRONTEND_DIR}
FRONTEND_VERSION=$(node -p "require('./package.json').version")
echo "Current frontend version: ${FRONTEND_VERSION}"
echo "##############################################"
NEW_FRONTEND_VERSION=${FRONTEND_VERSION}
if [ "${FE_INC_VER_TYPE}" != "ignore" ]; then
  NEW_FRONTEND_VERSION=$(npm version ${FE_INC_VER_TYPE} | sed 's/v//')
  echo "New frontend version: ${NEW_FRONTEND_VERSION}"
fi

if [ "${FE_INC_VER_TYPE}" = 'ignore' ] && [ "${BE_INC_VER_TYPE}" = 'ignore' ]; then
  echo "No new commit after the last release!"
  echo "Build Release: [CANCELED]"
  exit 1
fi

RELEASE_NUMBER=${NEW_BACKEND_VERSION}-${NEW_FRONTEND_VERSION}
echo "Building release #[${RELEASE_NUMBER}] ..."

# we should put running tests here before build
npm run build
if [ $? -ne 0 ]; then
  echo "Failed to build!"
  npm version ${FRONTEND_VERSION}
  echo ${BACKEND_VERSION} >${BASE_DIR}/wrh_organization/VERSION
  exit 1
fi

git add -A && git commit -m "[RELEASE VERSION] ${RELEASE_NUMBER}"

git branch -D lastest-release 2>/dev/null
git push origin --delete lastest-release 2>/dev/null

## Create a new branch to run the build under
git checkout -b lastest-release
newIgnore=$(sed -e 's#dist##g' .gitignore)
echo "$newIgnore" >.gitignore
git add -A && git commit -m "[RELEASE] ${RELEASE_NUMBER}"

git checkout master
git tag "${RELEASE_NUMBER}" lastest-release
git push origin "${RELEASE_NUMBER}"
git push origin lastest-release
git push origin master

echo "Finished Build Release: [${RELEASE_NUMBER}]!"
