from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qgl-admissibility-engine",
    version="1.0.0a0",
    author="JaxzMaori (Ngāti Porou)",
    license="GPL-3.0-or-later",
    description="A structural physics engine deriving constants from a void lattice.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cooperationz-cyber/qgl-admissibility-engine", # UPDATE THIS
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        # "matplotlib",  # if needed for visualizations
    ],
    entry_points={
        'console_scripts': [
            'qgl-run=qgl.admissibility_engine:main',
            'qgl-test=qgl.collapse_test:main',
        ],
    },
    include_package_data=True,
)