# Counts lines of code in current branch, using https://github.com/cgag/loc
#
# Usage: Invoke this script from the directory in which both ./HoloRepository-Core 
# and ./HoloRepository-HoloLens reside.

SHARED_EXCLUDES="(json$|yaml$|yml$|ini$|xml$|md$|txt$)"
CORE_EXCLUDES="./node_modules/.|HoloStorageAccessor/third_party|HoloStorageAccessor/src"
LENS_EXCLUDES="(./Assets/MixedRealityToolkit.|./HoloRepositoryDemoApplication/Library/.|./HoloStorageConnector/Plugins/.)"

loc ./HoloRepository-Core ./HoloRepository-HoloLens \
    --exclude ${SHARED_EXCLUDES} \
    --exclude ${CORE_EXCLUDES} \
    --exclude ${LENS_EXCLUDES}
