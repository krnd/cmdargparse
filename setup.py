from setuptools import find_packages, setup


setup(
    name="cmdargparse",
    version="0.0.0",
    description="A declarative way to define `cmd2` argument parsers.",
    author="Kilian Kaiping (krnd)",
    url="https://github.com/krnd/cmdargparse",
    license="MIT",
    packages=find_packages(include="cmdargparse"),
    python_requires=">=3.13",
    install_requires=[
        ("cmd2" "~=2.7"),
    ],
    keywords=[
        "CLI",
        "cmd",
        "command",
        "interactive",
        "prompt",
        "Python",
    ],
    classifiers=[
        # "Development Status :: 3 - Alpha"
        #   The project is a work-in-progress. It may have a basic feature set but is likely
        #   unstable and not suitable for production use.
        # "Development Status :: 4 - Beta"
        #   The project is feature-complete but still needs testing and bug-fixing. It is fairly
        #   stable but not yet considered production-ready.
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
