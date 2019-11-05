from setuptools import setup

setup(
    name='sipeapps',
    version='3.0.4',
    packages=['financeiro'],
    include_package_data=True,
    license='MIT License',
    description='Conjunto de apps Sipe Sistemas',
    url='http://github.com/sipesistemas',
    author='Sipe Sistemas',
    author_email='contato@sipesistemas.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=2.2.7',
        'djangorestframework>=3.10.3',
    ]
)
