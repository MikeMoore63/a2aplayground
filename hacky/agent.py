from google.adk.agents import Agent
import argparse
from vertexai.preview import reasoning_engines
from vertexai import agent_engines
import vertexai
import os


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
    """Returns a list of environment variables and values."""

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


def hacky_agent() -> Agent:
    return Agent(
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


def init_vertex():
    gcs_bucket = os.getenv("GCS_BUCKET", "gs://bobby-test")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT","methodical-bee-162815")
    region = os.getenv("GOOGLE_CLOUD_REGION","us-central1")
    vertexai.init(
        project=project_id,               # Your project ID.
        location=region,                # Your cloud region.
        staging_bucket=gcs_bucket,  # Your staging bucket.
    )

root_agent = hacky_agent()

app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="agent_app.py",
        description="An Agent Engine app that wraps the hacky agent",
        epilog="Have fun with it",
    )
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-d", "--deploy", action="store_true")
    parser.add_argument("-d2", "--deploy2", action="store_true")
    parser.add_argument("remote")
    args = parser.parse_args()

    if args.test:
        session = app.create_session(user_id="u_123")
        app.list_sessions(user_id="u_123")
        for event in app.stream_query(
            user_id="u_123",
            session_id=session.id,
            message="whats the OS, python version, env variables and packages installed?",
        ):
            print(event)
    if args.deploy:
        init_vertex()
        requirements = [
            "google-cloud-aiplatform[agent_engines,adk]",
            # any other dependencies
        ]
        extra_packages = ["installation_scripts/install.sh"]
        build_options = {"installation_scripts": ["installation_scripts/install.sh"]}
        gcs_dir_name = "one"
        display_name = "Hacky agent no psci, nocmek, no custom sa, pypi accesible"
        description = """A version of hacky agent to allow exploration of runtime 
env for agent space. o psci, nocmek, no custom sa, pypi accesible
        """
        remote_app = agent_engines.create(
            app,
            requirements=requirements,
            extra_packages=extra_packages,
            build_options=build_options,
            gcs_dir_name=gcs_dir_name,
            display_name=display_name,
            description=description,
        )
        print(remote_app)
    if args.deploy2:
        init_vertex()
        requirements = [
            "google-cloud-aiplatform[agent_engines,adk]",
            # any other dependencies
        ]
        extra_packages = ["installation_scripts/install.sh"]
        build_options = {"installation_scripts": ["installation_scripts/install.sh"]}
        gcs_dir_name = "one"
        display_name = "Hacky agent no psci, nocmek, no custom sa, pypi accesible"
        description = """A version of hacky agent to allow exploration of runtime 
env for agent space. o psci, nocmek, no custom sa, pypi accesible
        """
        remote_app = agent_engines.create(
            app,
            requirements=requirements,
            extra_packages=extra_packages,
            build_options=build_options,
            gcs_dir_name=gcs_dir_name,
            display_name=display_name,
            description=description,
        )
        print(remote_app)
    if args.remote:
        remote_app = agent_engines.get(args.remote)
        for event in remote_app.stream_query(
            user_id="u_123",
            message="whats the OS, python version, env variables and packages installed?",
        ):
            print(event)
        for event in remote_app.stream_query(
            user_id="u_123",
            message="execute bash script id",
        ):
            print(event)

