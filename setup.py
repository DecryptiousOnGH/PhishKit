from setuptools import setup, find_packages

setup(
    name="phishkit-builder",
    version="1.0.0",
    description="Educational phishing awareness testing tool",
    author="Decryptious_ on Discord / Punchborn on IG",
    py_modules=["phishkit"],
    install_requires=[
        "requests>=2.31.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "phishkit=phishkit:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)