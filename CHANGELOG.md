# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.5.1] - 2025-06-10

### Fixed

- Added the missing dose route info in standard.md of docs. Fix for Issue https://github.com/blakeaw/pysb-pkpd/issues/23

## [0.5.0] - 2025-06-06

### Added

- `standard` module defining convenience functions to quickly generate standard one-, two-, and three-compartment models. Added corresponding tests as well.
- Initial set of documentation source files for mkdocs. 

## [0.4.0] - 2025-01-30

### Added

- `CONTRIBUTING.md` file as per https://github.com/blakeaw/pysb-pkpd/issues/24
- An initial suite of automated tests compatible with pytest and coverage. Issue https://github.com/blakeaw/pysb-pkpd/issues/23

### Fixed

- Error in the `dose_absorbed` macro which was causing an extra `ka` parameter to be added to the model.

## [0.3.3] - 2024-07-21

### Fixed

- Fix for Issue https://github.com/blakeaw/pysb-pkpd/issues/20

## [0.3.2] - 2024-07-18

### Fixed

- Problem with local variable `F` not being defined when `f` is a `Parameter` instance.; Fix for Issue https://github.com/blakeaw/pysb-pkpd/issues/17

## [0.3.1] - 2024-07-03

### Fixed

- Missing sub-packages problem when installing with pip from the repo; Fix for Issue https://github.com/blakeaw/pysb-pkpd/issues/16

## [0.3.0] - 2024-07-01

### Added

- New PD macro `fixed_effect` encoding a fixed-effect model for the effect/response. Issue https://github.com/blakeaw/pysb-pkpd/issues/7
- `intercept` argument for the `linear_effect` PD model which allows users to set the y-intercept of the linear model. Issue https://github.com/blakeaw/pysb-pkpd/issues/9
- New PD macro `loglinear_effect` encoding a log-linear model for the effect/response as a function of concentration. Issue https://github.com/blakeaw/pysb-pkpd/issues/8
- New `util` module that defines the `simulate` function: Issue https://github.com/blakeaw/pysb-pkpd/issues/11

### Changed

- Replaced the `setup.py` script with a `pyproject.toml`; Issue https://github.com/blakeaw/pysb-pkpd/issues/13
- `linear_effect` PD macro: updated the parameter names to prefix them with `LinEffect_` to make sure they are unique.


## [0.2.1] - 2023-10-17

### Fixed
- Updated the mechanism for the `dose_absorbed` dosing macro function to use a precursor; Fix for Issue https://github.com/blakeaw/pysb-pkpd/issues/4

## [0.2.0] - 2023-05-23

### Added
- `dose_absorbed` dosing macro function to the `pysb.pkpd.macros` module.
- `linear_effect` PD macro function to the `pysb.pkpd.macros` module.
- `one_compartment` compartment macro function to the `pysb.pkpd.macros` module.
- `drug_monomer` macro function to the `pysb.pkpd.macros` module.
- Functions from the `macros` module are imported into `pkpd.__init__` so that they can be called directly from the `pkpd` namespace. 
- `example-notebooks` directory with a new PKRO example case. 

## [0.1.0] - 2023-05-23

### Added
- Initial development version of the package.

## [Unreleased] - yyyy-mm-dd

N/A

### Added

### Changed

### Fixed