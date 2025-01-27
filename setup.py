import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_eventmonitor",
    version="0.4.0",
    author="Reversedeer",
    description="监控群事件的插件，支持戳一戳，成员变动，群荣誉，运气王变化等提示",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Reversedeer/nonebot_plugin_eventmonitor",
    project_urls={
        "Bug Tracker": "https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "nonebot2>=2.0.0rc2",
        "nonebot-adapter-onebot>=2.1.3",
        "requests>=2.28.2",
        "httpx>=0.27.2"
        "poetry>=1.5.0"
        "pillow>=9.4.0"
        "sqlalchemy>=2.0.19"
        "nonebot-plugin-apscheduler>=0.1.3",
    ],
)
