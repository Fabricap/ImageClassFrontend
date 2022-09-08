from setuptools import setup , find_packages

with open('requirements.txt' , mode = 'r+' , encoding = 'utf-8') as file:
    content = [requirement.strip() for requirement in file.readlines()]


setup(name = 'FindingMemoFrontend',
      packages = find_packages(),
      include_package_data=True,
      install_requires=content
      )
