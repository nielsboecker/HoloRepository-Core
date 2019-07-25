# HoloStorage Accessor API Changelog
All changes done to the HoloStorage Accessor API spec will be documented here.

View the interactive documentation of the most updated API at the following link:
https://app.swaggerhub.com/apis/boonwj/HoloRepository/

## [0.2.0] - 2019-07-25
### Changed
- Hologram metadata is nested within `metadata` property in Hologram Schema
- Patient metadata is nested within `metadata` property in Patient Schema
- `/patients` and `/patients/{pid}` results will contain hologram `author` information
### Added
- Add `FROM_DEPTHVISOR_RECORDING` to `creationMode` enum
- Query field `creationmode` for filtering results based on `creationMode` of holograms on `/patients` and `/holograms` endpoints
- Error message returned on errors

## [0.1.4] - 2019-07-14
### Changed
- `creationMode` field's content to "GENERATE_FROM_IMAGING_STUDY" and
"UPLOAD_EXISTING_MODE"

## [0.1.3] - 2019-07-13
### Added
- `creationMode` field to hologram resource based on HoloPipelines input
- `pipelineId` field to hologram resource based on HoloPipelines input
- Update title and description of hologram upload schema

## [0.1.2]
Initial version of api spec based on inputs from UI and HoloLens App team.
