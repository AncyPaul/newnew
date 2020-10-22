
Enable cgroup swapping in Ubuntu
--------------------------------

Out of the box a Docker installation on Ubuntu, we may not be capable of setting limits. 

This is because cgroups swapping is disabled by default. When attempting to set limits you will be given the following error.

`WARNING: Your kernel does not support swap limit capabilities or the cgroup is not mounted. Memory limited without swap.`

To address this error we can enable cgroup swapping by doing the following:

Procedure
---------
* Open the grub configuration file.

  `vi /etc/default/grub`

* Add the following line. If the GRUB_CMDLINE_LINUX optional already exists, modify it to include the values below.

  `GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"`

* Save the changes and update the grub configuration.

  `sudo update-grub`
  
 * Before the changes will be applied, reboot the docker host.
 
