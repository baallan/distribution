This file covers some RAQs (rarely asked questions) that are of high utility when explaining
(to people who think they could do better) why we manage packaging the way we do in this repository.

Questions:

1. Why can't I just download a tar file ready to use without autoconf/automake?
2. Why must I (well, the packaging scripts named 'firerpm') configure a source tree before generating rpms?


Answers:

1. No conventional tar files.

    The reason the ovis (and many other DOE projects) cannot follow the typical build structure where published code is not autogen-dependent (no configure.ac needed by recipients) is that historically (and probably still today) the autotool-related scripts will fail on advanced and pre-release HPC platforms unless they are generated with the autotools provided in the deployment environment. Significant subsystems of OVIS are excluded depending on the target platform. No single target platform can compile all of the available options together.

    Similar issues apply to cmake, scons, and other autotools alternatives.

    Ultimately we end up where we are: everyone who wants to build from source must cope with the rigors of autogen instead of simple configure/make/make install. We try to keep our autotooling compatible with the latest mainline Redhat Enterprise offerings and back compatible with the current and one previous Redhat Enterprise Linux and Cray Linux Environment editions.

2. Double configure in building RPMs.

    The reason ovis must be configured has several parts:

    a. The RPM specification file must be massaged according to the variables determined in configure.

    b. The result of 'make dist' depends on the choices made in configure.

    c. The SRPM generated will be broken (missing or extra sources) if the configure options differ between what was specified to 'make dist' and what is specified in building the RPMs. The .spec file will be bad.

