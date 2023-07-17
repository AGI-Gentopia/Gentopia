from setuptools import setup, find_packages

setup(
    name='gentopia',
    version='0.1',
    packages=find_packages(exclude=['llm', 'llm.*']),
    url='https://github.com/Gentopia-AI/Gentopia',
    license='Apache-2.0 license',
    author='billxbf',
    author_email='billxbf@gmail.com',
    description='Gentopia assembles and serves specialized ALM agents driven by configs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    extras_require={
            'huggingface': ['torch', 'transformers', 'optimum', 'peft'],
        },
    install_requires=[
        'tenacity',
        'python-dotenv',
        'arxiv',
        'chardet',
        'cchardet',
        'numexpr',
        'googlesearch-python',
        'wolframalpha',
        'numpy',
        'rich',
        'tqdm',
        'prompt-toolkit',
        'regex',
        'attrs',
        'fastapi',
        'geopy',
        'pydantic',
        'pytest',
        'PyYAML',
        'requests',
        'setuptools',
        'uvicorn',
    ],
)
