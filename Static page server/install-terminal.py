### TUI-based installation script for WebRoot
### Automatically scans and installs all required dependencies
### Creates configuration files and user database

import os
import json
import sys
import hashlib
import subprocess
from pathlib import Path

# TUI Library for better terminal interface
try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.progress import Progress
    from rich.table import Table
except ImportError:
    print("Installing required TUI packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.progress import Progress
    from rich.table import Table

console = Console()

# All dependencies detected from your codebase
REQUIRED_PACKAGES = {
    'flask': 'Flask web framework',
    'websockets': 'WebSocket support for real-time communication',
    'gevent': 'Asynchronous workers for Gunicorn',
    'gunicorn': 'Production WSGI HTTP Server',
    'aiofiles': 'Async file operations',
}

OPTIONAL_PACKAGES = {
    'python-dotenv': 'Environment variable management',
}

# Standard library modules that should never be pip-installed
STDLIB_MODULES = {
    'abc', 'ast', 'asyncio', 'base64', 'builtins', 'collections', 'contextlib',
    'copy', 'csv', 'dataclasses', 'datetime', 'decimal', 'enum', 'errno',
    'functools', 'gc', 'glob', 'hashlib', 'html', 'http', 'importlib', 'inspect',
    'io', 'itertools', 'json', 'logging', 'math', 'multiprocessing', 'operator',
    'os', 'pathlib', 'pickle', 'platform', 'pprint', 'queue', 'random', 're',
    'shutil', 'signal', 'socket', 'ssl', 'stat', 'string', 'struct', 'subprocess',
    'sys', 'tempfile', 'textwrap', 'threading', 'time', 'traceback', 'types',
    'typing', 'unittest', 'urllib', 'uuid', 'warnings', 'weakref', 'zipfile',
}


def scan_python_files(root_path='.'):
    """Scan all Python files to detect additional imports"""
    detected_imports = set()

    for root, dirs, files in os.walk(root_path):
        # Skip common directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv']]

        for file in files:
            if file.endswith('.py'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        for line in f:
                            stripped = line.strip()
                            if stripped.startswith('import '):
                                # Handle: import os, sys, json
                                parts = stripped[len('import '):].split(',')
                                for part in parts:
                                    module = part.strip().split('.')[0].split(' ')[0]
                                    if module:
                                        detected_imports.add(module)
                            elif stripped.startswith('from '):
                                parts = stripped.split()
                                if len(parts) >= 2:
                                    module = parts[1].split('.')[0]
                                    if module:
                                        detected_imports.add(module)
                except Exception:
                    pass

    return detected_imports


def get_pip_package_name(import_name):
    """Map import names to pip package names. Returns None for stdlib or unknown builtins."""
    # Explicit pip name overrides (import name differs from pip package name)
    pip_name_overrides = {
        'flask': 'flask',
        'websockets': 'websockets',
        'gevent': 'gevent',
        'gunicorn': 'gunicorn',
        'aiofiles': 'aiofiles',
        'dotenv': 'python-dotenv',
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'sklearn': 'scikit-learn',
        'yaml': 'PyYAML',
        'bs4': 'beautifulsoup4',
        'serial': 'pyserial',
    }

    if import_name in pip_name_overrides:
        return pip_name_overrides[import_name]

    # Skip stdlib modules — do not attempt to pip-install them
    if import_name in STDLIB_MODULES:
        return None

    # For anything else, return as-is (third-party packages usually match their import name)
    return import_name


def install_packages(packages):
    """Install required packages. Returns lists of succeeded and failed packages."""
    console.print(Panel.fit("[bold cyan]Installing Dependencies[/bold cyan]"))

    succeeded = []
    failed = []

    with Progress() as progress:
        task = progress.add_task("[cyan]Installing packages...", total=len(packages))

        for package in packages:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-q", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                succeeded.append(package)
            except subprocess.CalledProcessError:
                console.print(f"[red]✗ Failed to install {package}[/red]")
                failed.append(package)
            finally:
                progress.update(task, advance=1)

    return succeeded, failed


def create_directories(folder_path):
    """Create required directory structure"""
    console.print(Panel.fit("[bold cyan]Creating Directory Structure[/bold cyan]"))

    lines = []
    lines.append(f'_log_folder_path = "{folder_path}"\n')

    # Create logs directory
    logs_path = os.path.join(folder_path, "logs")
    os.makedirs(logs_path, exist_ok=True)

    log_files = ["error_logs.csv", "download_logs.csv", "user_logs.csv", "upload_logs.csv"]

    with Progress() as progress:
        task = progress.add_task("[cyan]Creating log files...", total=len(log_files))

        for log_file in log_files:
            log_file_path = os.path.join(logs_path, log_file)
            with open(log_file_path, "w") as f:
                pass
            lines.append(f'_{log_file[:-4]}_file_path = "{log_file_path}"\n')
            progress.update(task, advance=1)

    return lines, logs_path


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def setup_user_credentials(folder_path):
    """Setup user credentials in database (passwords are stored hashed)."""
    console.print(Panel.fit("[bold cyan]User Credentials Setup[/bold cyan]"))

    user_cred = {}

    console.print("[bold]Enter user credentials (leave username empty to finish):[/bold]")

    while True:
        username = Prompt.ask("Username", default="").strip()
        if not username:
            break

        password = Prompt.ask("Password", password=True)
        if not password:
            console.print("[yellow]⚠ Password cannot be empty, skipping[/yellow]")
            continue

        confirm = Prompt.ask("Confirm password", password=True)
        if password != confirm:
            console.print("[yellow]⚠ Passwords do not match, skipping[/yellow]")
            continue

        user_cred[username] = hash_password(password)
        console.print(f"[green]✓ User '{username}' added[/green]")

    # Create database directory
    db_path = os.path.join(folder_path, "database")
    os.makedirs(db_path, exist_ok=True)

    cred_file = os.path.join(db_path, "user_credentials.json")
    with open(cred_file, "w") as f:
        json.dump(user_cred, f, indent=2)

    console.print(f"[green]✓ Credentials saved to {cred_file}[/green]")

    return [f'_user_login_credential_path = "{cred_file}"\n'], cred_file


def setup_ssl_certificates(folder_path):
    """Setup SSL certificates for HTTPS"""
    console.print(Panel.fit("[bold cyan]SSL/TLS Certificate Setup[/bold cyan]"))

    if not Confirm.ask("Do you want to enable HTTPS/encryption?", default=False):
        return []

    cert_path = os.path.join(folder_path, "certificates")
    os.makedirs(cert_path, exist_ok=True)

    console.print("[yellow]⚠ Note: You'll be asked to fill certificate information[/yellow]")
    console.print("[dim]Generating self-signed certificate for 365 days...[/dim]")

    try:
        subprocess.run(
            [
                "openssl", "req", "-x509", "-newkey", "rsa:4096",
                "-nodes", "-out", os.path.join(cert_path, "cert.pem"),
                "-keyout", os.path.join(cert_path, "key.pem"),
                "-days", "365"
            ],
            check=True
        )
        console.print("[green]✓ SSL certificates generated successfully[/green]")
        return [f'_certificate_path = "{cert_path}"\n']
    except subprocess.CalledProcessError:
        console.print("[red]✗ Failed to generate SSL certificate[/red]")
        console.print("[yellow]⚠ Please generate manually or continue without HTTPS[/yellow]")
        return []
    except FileNotFoundError:
        console.print("[red]✗ OpenSSL not found on your system[/red]")
        console.print("[yellow]⚠ Install OpenSSL or skip SSL setup[/yellow]")
        return []


def generate_paths_file(lines, output_path="_paths.py"):
    """Generate the _paths.py configuration file"""
    console.print(Panel.fit("[bold cyan]Generating Configuration File[/bold cyan]"))

    with open(output_path, "w") as f:
        f.writelines(lines)

    console.print(f"[green]✓ Configuration file generated: {output_path}[/green]")


def show_summary(detected_imports, succeeded, failed, config_path):
    """Show installation summary"""
    table = Table(title="Installation Summary")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Details", style="magenta")

    table.add_row("Scanned Imports", str(len(detected_imports)))
    table.add_row("Packages Installed", str(len(succeeded)))
    table.add_row("Packages Failed", f"[red]{len(failed)}[/red]" if failed else "0")
    table.add_row("Config File", config_path)

    console.print(table)

    if failed:
        console.print("\n[red]Failed packages:[/red]")
        for pkg in failed:
            console.print(f"  [red]• {pkg}[/red]")


def main():
    """Main installation flow"""
    console.print(Panel("[bold green]WebRoot Installation[/bold green]", expand=False))

    # Scan for dependencies
    console.print("[bold]Scanning Python files for dependencies...[/bold]")
    detected_imports = scan_python_files()

    # Filter to get actual installable packages (skip stdlib)
    packages_to_install = []
    for imp in sorted(detected_imports):
        pkg = get_pip_package_name(imp)
        if pkg and pkg not in packages_to_install:
            packages_to_install.append(pkg)

    # Show detected packages
    console.print("\n[bold cyan]Detected Dependencies:[/bold cyan]")
    for pkg in packages_to_install:
        console.print(f"  • {pkg}")

    if not packages_to_install:
        console.print("[yellow]No third-party packages detected.[/yellow]")

    # Install packages
    succeeded, failed = [], []
    if packages_to_install:
        if Confirm.ask("\nProceed with installation?", default=True):
            succeeded, failed = install_packages(packages_to_install)
            console.print("[green]✓ Installation step complete[/green]")
        else:
            console.print("[yellow]Installation cancelled[/yellow]")
            return

    # Get installation folder
    console.print("\n[bold cyan]Configuration[/bold cyan]")
    folder_path = Prompt.ask(
        "Enter the folder path for logs, certificates, and database",
        default=os.getcwd()
    )

    if not os.path.exists(folder_path):
        console.print(f"[yellow]Creating folder: {folder_path}[/yellow]")
        os.makedirs(folder_path, exist_ok=True)

    # Setup process
    lines = []

    # Create directories
    dir_lines, _ = create_directories(folder_path)
    lines.extend(dir_lines)

    # Setup users
    if Confirm.ask("Setup user credentials?", default=True):
        user_lines, _ = setup_user_credentials(folder_path)
        lines.extend(user_lines)

    # Setup SSL
    ssl_lines = setup_ssl_certificates(folder_path)
    lines.extend(ssl_lines)

    # Generate config
    config_path = os.path.join(folder_path, "_paths.py")
    generate_paths_file(lines, config_path)

    # Show summary
    show_summary(detected_imports, succeeded, failed, config_path)

    console.print("\n[bold green]✓ Installation completed successfully![/bold green]")
    console.print(f"[yellow]Config file: {config_path}[/yellow]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Installation cancelled by user[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)
