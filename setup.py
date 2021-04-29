from setuptools import setup


def load_requirements():
    with open("requirements.txt", "r") as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name="z3-picross-solver",
    version="1.0.0",
    install_requires=load_requirements(),
    entry_points={"console_scripts": ["z3-picross-solver = picross_solver.core:main"]},
)
