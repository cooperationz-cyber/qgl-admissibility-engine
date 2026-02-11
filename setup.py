from setuptools import setup 
 
setup( 
    name="qgl-admissibility-engine", 
    version="3.0.0", 
    author="JaxzMaori", 
    description="Complete derivation of phi, e, pi, alpha from void lattice", 
    long_description="QGL Admissibility Engine - Derives constants with 0.000000%% error", 
    long_description_content_type="text/markdown", 
    url="https://github.com/cooperationz-cyber/qgl-admissibility-engine", 
    py_modules=["main"], 
    install_requires=["numpy"], 
    classifiers=[ 
        "Programming Language :: Python :: 3", 
    ], 
    python_requires=">=3.8", 
) 
