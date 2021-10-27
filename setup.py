"""Install Pipeswitch."""

from distutils.core import setup

setup(
    name="pipeswitch",
    url="https://github.com/netx-repo/Pipeswitch",
    packages=['pipeswitch', 'util', 'task', 'client', 'kill_restart', 'ready_model'],
)