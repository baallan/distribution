The steps for an offgrid build with the distribution recipes are as follows.
We will use the rhel7 build as an example, but any other recipe will be similarly used.

# Get the sources

    mkdir sources
    cd sources
    git clone https://github.com/baallan/distribution.git
    git clone https://github.com/ovis-hpc/ovis.git
    git clone https://github.com/opengridcomputing/SOS.git
    cd ..
    tar czf sources.tar.gz sources

Please note: Do NOT use the Github offered zip files from these repositories.
The automatic zip files produced by github are broken because the do not
contain the .git our build assumes to exist.

# Copy the sources.tar.gz file into your off-grid environment and extract it.

# Unpack the sources

    tar xzf sources.tar.gz
    cd sources

# Modify a build recipe for your site

    cd distribution
    cp -a rhel7 rhel7-original
    cd rhel7

# Modify ./firerpms with your favorite editor
Change lines

    #SOSREPO=gitlab@gitlab.opengridcomputing.com:tom/SOS.git
    OVISREPO=https://github.com/ovis-hpc/ovis.git

to

    SOSREPO=../../SOS
    OVISREPO=../../ovis

then do the build:

    ./firerpms


