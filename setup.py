from setuptools import setup, find_packages

requires = [
    "pyramid",
    "pyramid_tm",
    "pyramid_layout",
    "pyramid_fanstatic",
    "sqlalchemy==0.7.10", # for formalchemy BBB
    "zope.sqlalchemy",
    "webhelpers2",
    "paginate",
    "feedgenerator",
    "formalchemy",
    "cliff",
    "js.tinymce",
    "js.jquery",
]

tests_require = [
    "pytest",
    "mock",
    "coverage",
    "webtest",
    "pytest-cov",
]

points = {
    "console_scripts": [
        "clarith=clarith:main",
    ],
    "clarith.commands": [
        "create_blog=clarith.blog.commands:CreateBlog",
    ],
    "paste.app_factory": [
        "main=clarith.blog:main"
    ],
    "fanstatic.libraries": [
        "clarith=clarith.fa.resources:clarith_library",
    ]
}


setup(
    name='clarith',
    version='1.0',
    url='http://bitbucket.org/aodag/clarith',
    license='MIT',
    author='Atsushi Odagiri',
    author_email='aodagx@gmail.com',
    description='clarith is basic blog app',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requires,
    include_package_data=True,
    tests_require=tests_require,
    entry_points=points,
    extras_require={
      "testing": requires+tests_require,
      "develop": ["alembic", "pyramid_debugtoolbar"],
    },
)
