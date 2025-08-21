import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent


def get_python_version() -> str:
    """Returns the Python version being used."""
    import sys

    return sys.version


def get_packages_installed() -> list[str]:
    """Returns a list of installed Python packages in the current environment.

    This is useful for debugging or checking for dependencies.

    Returns:
        list[str]: A list of installed package names.
    """
    from importlib import metadata

    return [
        f"{dist.metadata["Name"]}:{dist.metadata["Version"]}"
        for dist in metadata.distributions()
    ]


def get_os_version() -> str:
    """Returns the operating system version."""
    import os.path

    if os.path.isfile("/etc/os-release"):
        with open("/etc/os-release") as f:
            return f.read()
    else:
        import platform

        return platform.platform()


def get_env_vars() -> list[str]:
    """Returns a list of environment variables."""
    import os

    return [f"{key}={value}" for key, value in os.environ.items()]


def get_shells() -> list[str]:
    """Returns a list of available shells."""
    import shutil

    shells = []
    for shell in ["/bin/bash", "/bin/sh", "/bin/zsh", "/bin/fish"]:
        if shutil.which(shell):
            shells.append(shell)
    return shells


def execute_bash_command(command: str) -> str:
    """Executes a bash command and returns the output."""
    import subprocess

    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr.strip()}"
    except Exception as e:
        return f"Error executing command: {e}"


root_agent = Agent(
    name="hack_agent",
    model="gemini-2.0-flash",
    description=("Agent to answer questions about the running environment"),
    instruction=(
        "You are a helpful agent who can answer user questions about the runtime environment of agent. Demonstrates what a malicous agent could do by answering questions about the environment, such as the Python version, installed packages, OS version, environment variables, available shells, and executing bash commands."
    ),
    tools=[
        get_python_version,
        get_packages_installed,
        get_os_version,
        get_env_vars,
        get_shells,
        execute_bash_command,
    ],
)
