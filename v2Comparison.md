OVIS v3.4.6 is a features and bug fix release. 

See the change notes at
https://github.com/ovis-hpc/ovis/releases/tag/v3.4.6

OVIS v3.4.2 is a patch for improved usability.

New features:

* store_csv support for automatic rename of closed files, avoiding extra log/pipe usage.
* check for correct use of init scripts
* adds line numbers to error messages when parsing configuration files.

OVIS v3.4 is a major rewrite of LDMS v2.

New features:

* Systemd support
* More samplers
* Ldmsd startup script options
* Ldmsd python control options
* Baler log processing included
* SOS database included
* File event notification of CVS files to FIFO/file
* New Cray transport and sampler support

Modified features:

* Updated genders attributes and per-plugin configuration file options
* Extended support of hostname fragments in gender values.
* Total bypass of gender data use in systemd scripts.
* Extended SLURM data (user id) sampling
* Extended support of environment variables in configuration options

Removed features:

* In-daemon execution of CSV file event handler programs.
 * Convert your pipeline programs to follow file or fifo.

For additional details, see the man pages.

TOSS users in particular will want to see man pages ldmsd-genders and ldms-attributes.
