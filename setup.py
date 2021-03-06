from setuptools import setup,find_packages

setup(
    name="analyze",
    version="1.0",
    author="liuran",
    author_email="liuran-001@126.com",
    description="analyze function",
    packages=find_packages(),
    install_requires=[
        'gevent',
        'Flask',
        'kombu',
        'SQLAlchemy',
        'psutil',
        'reportlab'
    ],
    entry_points={
        'console_scripts':[
            'report-gen=analyze.report_gen:main',
            'analyze=analyze.analyze_main:analyze_main',
            'analyze-db-sync=analyze.analyze_db_sync:main',
            'search-engine-monitor=analyze.search_engine_monitor:main',
        ]
    }
)
