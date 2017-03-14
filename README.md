As of March 2017, there are several planned platforms, organized by directory. See below for instructions on package construction.

## Platforms with binary packaging

* **toss2/** TOSS 2 RHEL 6 derivative with specialized plugins

* **toss3/** TOSS 3 RHEL 7 derivative with specialized plugins
* **rhel6/** desktop Redhat Enterprise 6 without specialized subsystems.
* **rhel7/** desktop Redhat Enterprise 7 without specialized subsystems.
* **cle6/** Cray Linux Environment 6 (Rhine) with specialized plugins

## Platforms with source build examples
* **u16/** Ubuntu 16 without specialized plugins
 * If you wish to contribute a binary build (.deb format), please contact ovis-help@sandia.gov.

## Making packages
Clone this repository to a scratch directory, go to the directory of interest, and execute the **firerpms** script. E.g.

    git clone gitlab@gitlab.opengridcomputing.com:baallan/distribution.git
    cd distribution
    cd rhel7
    ./firerpms

If successful, this will get you a list of rpms for the latest stable public release on that platform. The rpms are relocatable, which is at variance with most Linux distribution's standard policies.

## Installation
See the Installation.md file for RPM usage guidance.

## Making test packages
For any platform, there may also be a $platform.unstable/ directory containing development, test, and historical builds. Third parties should not attempt to build these unstable packages.
These will be under numerous names. There will often be a **firerpms** script which combines the most recent development sources. In many cases the repositories used will require special access privileges.
When working with test packages, pay particular attention to the variables at the top of the fire script which control repository and branch.

