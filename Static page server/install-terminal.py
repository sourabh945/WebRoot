### TUI-based installation script for WebRoot
### Automatically scans and installs all required dependencies
### Creates configuration files and user database

import os
import json
import sys
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

_separator = os.sep

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
                            if line.strip().startswith(('import ', 'from ')):
                                parts = line.strip().split()
                                if parts[0] == 'import':
                                    module = parts[1].split('.')[0].split(',')[0]
                                    detected_imports.add(module)
                                elif parts[0] == 'from':
                                    module = parts[1].split('.')[0]
                                    detected_imports.add(module)
                except:
                    pass
    
    return detected_imports


def get_pip_package_name(import_name):
    """Map import names to pip package names"""
    mapping = {
        'flask': 'flask',
        'websockets': 'websockets',
        'gevent': 'gevent',
        'gunicorn': 'gunicorn',
        'aiofiles': 'aiofiles',
        'datetime': None,
        'random': None,
        'string': None,
        'functools': None,
        'os': None,
        'json': None,
        'sys': None,
        'csv': None,
        'pathlib': None,
        'asyncio': None,
        'multiprocessing': None,
    }
    return mapping.get(import_name, import_name)


def install_packages(packages):
    """Install required packages"""
    console.print(Panel.fit("[bold cyan]Installing Dependencies[/bold cyan]"))
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Installing packages...", total=len(packages))
        
        for package in packages:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-q", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                progress.update(task, advance=1)
            except subprocess.CalledProcessError:
                console.print(f"[red]✗ Failed to install {package}[/red]")
                progress.update(task, advance=1)


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


def setup_user_credentials(folder_path):
    """Setup user credentials in database"""
    console.print(Panel.fit("[bold cyan]User Credentials Setup[/bold cyan]"))
    
    user_cred = {}
    
    console.print("[bold]Enter user credentials (leave empty to skip):[/bold]")
    
    while True:
        username = Prompt.ask("Username", default="").strip()
        if not username:
            break
        
        password = Prompt.ask("Password", password=True)
        if password:
            user_cred[username] = password
            console.print(f"[green]✓ User '{username}' added[/green]")
        else:
            console.print("[yellow]⚠ Password cannot be empty, skipping[/yellow]")
    
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


def show_summary(detected_packages, installed_packages, config_path):
    """Show installation summary"""
    table = Table(title="Installation Summary")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Details", style="magenta")
    
    table.add_row("Detected Imports", str(len(detected_packages)))
    table.add_row("Installed Packages", str(len(installed_packages)))
    table.add_row("Config File", config_path)
    
    console.print(table)


def main():
    """Main installation flow"""
    console.print(Panel.fit("[bold green]WebRoot Installation[/bold green]", expand=False))
    
    # Scan for dependencies
    console.print("[bold]Scanning Python files for dependencies...[/bold]")
    detected_imports = scan_python_files()
    
    # Filter to get actual packages to install
    packages_to_install = []
    for imp in detected_imports:
        pkg = get_pip_package_name(imp)
        if pkg and pkg not in packages_to_install:
            packages_to_install.append(pkg)
    
    # Show detected packages
    console.print("\n[bold cyan]Detected Dependencies:[/bold cyan]")
    for pkg in sorted(packages_to_install):
        console.print(f"  • {pkg}")
    
    # Install packages
    if Confirm.ask("\nProceed with installation?", default=True):
        install_packages(packages_to_install)
        console.print("[green]✓ All packages installed[/green]")
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
    show_summary(detected_imports, packages_to_install, config_path)
    
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
