#!/usr/bin/env python3
"""
XKit v3.0 - Enhanced PowerShell Framework Setup
Hybrid MCP Architecture with Plugin System and Event-Driven Architecture
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="xkit",
    version="3.0.0",
    description="Enhanced PowerShell Framework with Hybrid MCP Architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="XKit Development Team",
    author_email="dev@xkit.framework",
    url="https://github.com/rootkit-original/WindowsPowerShell",
    project_urls={
        "Bug Reports": "https://github.com/rootkit-original/WindowsPowerShell/issues",
        "Source": "https://github.com/rootkit-original/WindowsPowerShell",
        "Documentation": "https://github.com/rootkit-original/WindowsPowerShell/blob/main/docs/README.md"
    },
    
    # Package configuration
    packages=find_packages(where="Scripts"),
    package_dir={"": "Scripts"},
    python_requires=">=3.11",
    install_requires=requirements,
    
    # Entry points
    entry_points={
        "console_scripts": [
            "xkit=xkit_main:main",
            "xkit-mcp=xkit.mcp.client:main",
            "xkit-plugin=xkit.plugins.manager:main",
        ],
    },
    
    # Package data
    include_package_data=True,
    package_data={
        "xkit": [
            "config/*.json",
            "mcp/config.json",
            "mcp/servers/*.py",
            "plugins/core/*.py",
            "plugins/integrations/*.py",
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Build Tools",
        "Framework :: AsyncIO",
    ],
    
    # Keywords
    keywords="powershell, framework, mcp, plugins, automation, ai, telegram, git",
    
    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1", 
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.1.0",
            "mypy>=1.6.1",
        ],
        "ai": [
            "google-generativeai>=0.3.0",
            "openai>=1.3.7",
            "anthropic>=0.7.7",
        ],
        "telegram": [
            "python-telegram-bot>=20.6",
        ],
        "container": [
            "docker>=6.1.3",
        ],
        "all": [
            "google-generativeai>=0.3.0",
            "openai>=1.3.7", 
            "anthropic>=0.7.7",
            "python-telegram-bot>=20.6",
            "docker>=6.1.3",
        ],
    },
    
    # ZIP safe
    zip_safe=False,
)