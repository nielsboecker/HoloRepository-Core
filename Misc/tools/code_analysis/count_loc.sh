#!/bin/bash

# Counts lines of code in current branch, using https://github.com/cgag/loc
#
# Usage: Invoke this script with the relevant project directories as arguments
# Example: count_loc.sh ./HoloRepository-Core ./HoloRepository-HoloLens

echo "Counting project related LOC in directories: ${@}"

SHARED_EXCLUDES="(json$|yaml$|yml$|ini$|xml$|md$|txt$)"
CORE_EXCLUDES="node_modules|HoloRepositoryUI/server/dist|HoloRepositoryUI/client/build|HoloStorageAccessor/third_party|HoloStorageAccessor/src|HoloPipelines/core/third_party"
LENS_EXCLUDES="(Assets/MixedRealityToolkit|HoloRepositoryDemoApplication/Library|HoloStorageConnector/Plugins)"

loc "${@}" \
    --exclude ${SHARED_EXCLUDES} \
    --exclude ${CORE_EXCLUDES} \
    --exclude ${LENS_EXCLUDES}
