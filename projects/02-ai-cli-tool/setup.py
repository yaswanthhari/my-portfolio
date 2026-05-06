from setuptools import setup, find_packages

setup(
    name="ai-summarizer-cli",
    version="1.0.0",
    author="Yaswanth Hari",
    description="AI-powered text summarizer CLI tool",
    py_modules=["summarize"],
    install_requires=[
        "click>=8.0.0",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "pyperclip>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "summarize=summarize:main",
        ],
    },
)
