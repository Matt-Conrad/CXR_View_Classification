import setuptools

setuptools.setup(
    name="cxr_pipeline",
    version="0.0.1",
    author="Matt-Conrad",
    author_email="mattgrayconrad@gmail.com",
    description="CXR pipeline code to be shared by multiple applications",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)