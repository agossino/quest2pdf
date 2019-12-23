from setuptools import find_packages, setup
from src.quest2pdf import _version

with open("README.md", "r") as longdesc:
   long_description = longdesc.read()

setup(
   name="quest2pdf",
   description="From cvs to question.",
   long_description=long_description,
   author="ago",
   version=_version.__version__,
   packages=find_packages(where="src/"),
   package_dir={"": "src"},
)
