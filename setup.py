from setuptools import setup, find_packages

setup(
    name="wdgen",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to generate and collect dipole structures.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wdgen",  # 替换为你的项目链接
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wdgen=wdgen.main:main",  # 将 wdgen 命令绑定到 wdgen.main 中的 main 函数
        ]
    },
    install_requires=[
        "numpy",
        "matplotlib",
        "ase",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
