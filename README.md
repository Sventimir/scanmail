# Scanmail script for Linux

The task of this script is to parse new mail in a mailbox, retrieve headers
of any new messages and display a notification if new mail has arrived.
Intended to be run periodically as a system service, removing the need to
keep an email client (such as Thunderbird) constantly open.

Dependencies
-------------
* Python 3.8.6 (should work with any Python 3.x.x, but wasn't tested)
* `isync` (e-mail synchroniser)
* `libnotify` (notification server)
* a notification display

Alternate dependencies
----------------------

Both `isync` and `libnotify` can be replaced with any other tools suitable for
their respective jobs. In such cases the script will require some adaptations.
For now both `isync` and `libnotify` commands are hard-coded.

Environment
------------

Script depends on several environment variables being set to appropriate values:
* `HOME` (home directory of the user whose mail is being scanned)
* `DISPLAY` (X server display, required by `notify-send`)
* `DBUS_SESSION_BUS_ADDRESS` (also required by `notify-send`)

On my system (Arch Linux) `DBUS_SESSION_BUS_ADDRESS` is set to `unix:path=/run/user/1000/bus`.
Note that `1000` is the uid of the owner of the mailbox. It can be different on
each installation and for each user of the system. Other values may be
appropriate on other systems.

Suggested usage
---------------

Although the script may be run manually, it's intended to be run as a system
service using a `systemd` timer or `cron`.

In case of `systemd` service definitions are included. These files should be
installed in `/etc/systemd/system` and both should be enabled with

    $ systemctl enable scanmail.service
    $ systemctl enable scanmail.timer

`scanmail.service` can also be triggered manually at any moment.
