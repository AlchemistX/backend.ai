.. role:: raw-html-m2r(raw)
   :format: html


Install Agent
=============

We assume that your system is configured with a sudoable admin user named ``devops``.
Your Backend.AI manager should be already set up and running.

Guide variables
---------------

⚠️ Prepare the values of the following variables before working with this page and replace their occurrences with the values when you follow the guide.


.. list-table::
   :header-rows: 1

   * - Name
     - Meaning
   * - ``{NS}``
     - The etcd namespace (just create a unique string like domain names)
   * - ``{ETCDADDR}``
     - The etcd cluster address (\ ``{ETCDHOST}:{ETCDPORT}``\ , ``localhost:2379`` for development setup)
   * - ``{ENDPOINT}``
     - The DNS hostname of the API server (depending on your environment, this may be either a publicly registered domain or a local private domain)


Optional variables
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Meaning
   * - ``{SSLCERT}``
     - The path to your SSL certificate (bundled with CA chain certificates)
   * - ``{SSLPKEY}``
     - The path to your SSL private key
   * - ``{S3AKEY}``
     - The access key for AWS S3 or compatible services [#fn1]_
   * - ``{S3SKEY}``
     - The secret key for AWS S3 or compatible services
   * - ``{DDAPIKEY}``
     - The Datadog API key
   * - ``{DDAPPKEY}``
     - The Datadog application key
   * - ``{SENTRYURL}``
     - The private Sentry report URL


.. [#fn1] AWS S3 is used to store the output files generated by the user code in kernels' ``/home/work/.output`` directory.
   If not specified, Backend.AI will just skip uploading generated files.


Install dependencies for daemonization
--------------------------------------

Ubuntu
^^^^^^

.. code-block:: console

   $ sudo apt-get -y update
   $ sudo apt-get -y dist-upgrade
   $ sudo apt-get install -y ca-certificates git-core supervisor

Here are some optional but useful packages:

.. code-block:: console

   $ sudo apt-get install -y vim tmux htop

CentOS / RHEL
^^^^^^^^^^^^^

(TODO)

Prepare CUDA (if available)
---------------------------

Check out the [[Install CUDA]] guide.

Prepare Python 3.6+
-------------------

Check out [[Install Python via pyenv]] for instructions.
Create a virtualenv named ``venv-agent``.

**(Only in Linux)** To enable detailed resource statistics, give the Python executable to have ``CAP_SYS_ADMIN``\ , ``CAP_SYS_PTRACE``\ , and ``CAP_DAC_OVERRIDE`` capabilities.

.. code-block:: console

   $ sudo setcap cap_sys_ptrace,cap_sys_admin,cap_dac_override+eip "$(readlink -f $(pyenv which python))"

Install Backend.AI Agent as Package
-----------------------------------

.. code-block:: console

   $ pyenv shell venv-agent
   $ pip install -U setuptools pip
   $ pip install -U backend.ai-agent

Monitoring and Logging
----------------------

Check out the [[Install Monitoring and Logging Tools]] guide.

Configure supervisord
---------------------

supervisord application config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ sudo vi /etc/supervisor/conf.d/apps.conf

.. code-block:: dosini

   [program:backendai-agent]
   user = devops
   stopsignal = TERM
   stopasgroup = true
   command = /home/devops/run-agent.sh

pyenv + venv initialization script for non-login shells
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ vi /home/devops/init-venv.sh

.. code-block:: shell

   #!/bin/bash
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   pyenv shell venv-agent

Prepare scratch directory (place for kernel containers' ``/home/work``\ )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ sudo mkdir -p /var/cache/scratches
   $ sudo chown devops:devops /var/cache/scratches

The main program managed by supervisord
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   $ vi /home/devops/run-agent.sh

.. code-block:: shell

   source /home/devops/init-venv.sh
   umask 0002
   export AWS_ACCESS_KEY_ID="{S3AKEY}"
   export AWS_SECRET_ACCESS_KEY="{S3SEKEY}"
   export DATADOG_API_KEY={DDAPIKEY}
   export DATADOG_APP_KEY={DDAPPKEY}
   export RAVEN_URI="{SENTRYURL}"
   exec python -m ai.backend.agent.server \
               --etcd-addr {ETCDADDR} \
               --namespace {NS} \
               --scratch-root=/var/cache/scratches

Prepare Kernel Images
---------------------

You need to pull the kernel container images first to actually spawn compute sessions.
The name and tag pairs of images must be also specified in ``backend.ai-manager/sample-configs/image-metadata.yml`` file imported into etcd.

Here are the pull commands for a few commonly used Python-based images:

.. code-block:: console

   $ docker pull lablup/kernel-python:3.6-debian
   $ docker pull lablup/kernel-python-tensorflow:1.8-py36
   $ docker pull lablup/kernel-python-tensorflow:1.8-py36-gpu

For the full list of publicly available kernels, `check out the kernels repository. <https://github.com/lablup/backend.ai-kernels>`_

Finally, Run!
-------------

.. code-block:: console

   $ sudo supervisorctl reread
   $ sudo supervisorctl start backendai-agent
