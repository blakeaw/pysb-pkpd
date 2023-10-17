# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

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