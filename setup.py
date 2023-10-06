from setuptools import find_packages, setup
# from typing import List

HYPEN_E_DOT='-e .'

def get_requirements(file_name:str)->list[str]:
    '''
        this function returns list of requirements
    '''
    requirements=[]

    with open(file_name) as file_obj:
        requirements=file_obj.readlines
        requirements=[req.replace('\n',"") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name="ML_Project",
    version="0.0.1",
    author="Akshay",
    packages=find_packages(),
    requires=get_requirements('requirements.txt')
)