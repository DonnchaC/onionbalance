UNRELEASED
----------

- Add support for connecting to the Tor control port over a unix domain socket.

0.1.4
-----

- Use setproctitle to set a cleaner process title
- Replace the python-schedule dependency with a custom scheduler.
- Add a Unix domain socket which outputs the status of the OnionBalance
  service when a client connects. By default this socket is created at
  `/var/run/onionbalance/control`. Thank you to Federico Ceratto for the
  original socket implementation.
- Add support for handling the `SIGINT` and `SIGTERM` signals. Thank you to
  Federico Ceratto for this feature.
- Upgrade tests to use the stable Tor 0.2.7.x release.
- Fix bug when validating the modulus length of a provided RSA private key.
- Upload distinct service descriptors to each hidden service directory by
  default. The distinct descriptors allows up to 60 introduction points or
  backend instances to be reachable by external clients. Thank you to Ceysun
  Sucu for describing this technique in his Masters thesis.
- Add `INITIAL_DELAY` option to wait longer before initial descriptor
  publication. This is useful when there are many backend instance descriptors
  which need to be downloaded.
- Add configuration option to allow connecting to a Tor control port on a
  different host.
- Remove external image assets when documentation is generated locally
  instead of on ReadTheDocs.

0.1.3
-----

- Streamline the integration tests by using Tor and Chutney from the
  upstream repositories.
- Fix bug when HSFETCH is called with a HSDir argument (3d225fd).
- Remove the 'schedule' package from the source code and re-add it as a
  dependency. This Python package is now packaged for Debian.
- Extensively restructure the documentation to make it more comprehensible.
- Add --version argument to the command line
- Add configuration options to output log entries to a log file.

0.1.2
-----

- Remove dependency on the schedule package to prepare for packaging
  OnionBalance in Debian. The schedule code is now included directly in
  onionbalance/schedule.py.
- Fix the executable path in the help messages for onionbalance and
  onionbalance-config.

0.1.1
-----

- Patch to resolve issue when saving generated torrc files from
  onionbalance-config in Python 2.


0.1.0
-----

-  Initial release
