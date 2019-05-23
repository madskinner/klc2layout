import setuptools
from klc2layout.myclasses.myconst.therest import THIS_VERSION

setuptools.setup(
    name="klc2layout",
    version=THIS_VERSION,
    url="https://github.com/madskinner/klc2layout",
    author="Mark Skinner",
    author_email="mark_skinner@sil.org",
    description="Convert msklc files to SPKL, kmfl and Keyman",
    long_description=open('README.rst').read(),
#    data_files=[('../tests', ['set_tags.json', 'default_values.json', 'hash_tag_on.json', 'idiot_tags.json', 'localized_text.json', 'read_tag.json', 'read_tag_hide_encoding.json', 'read_tag_info.json', 'trim_tag.json',]),]
#                ('', ['set_tags.json', 'default_values.json', 'hash_tag_on.json', 'idiot_tags.json', 'localized_text.json', 'read_tag.json', 'read_tag_hide_encoding.json', 'read_tag_info.json', 'trim_tag.json',]),],
    packages=setuptools.find_packages(),
#    package_data={'klc2layout': ['*.html', '*.json', '*.ico', 'images/*.png', 'images/*.jpg', 'images/*.ico']},
    package_data={'klc2layout': ['*.html', '*.ico', 'images/*.png', 'images/*.jpg', 'images/*.ico']},
    install_requires=["unidecode",],
    license='MIT',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: End Users/Desktop',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6'],
    keywords='publish mp3 metadata sdcard',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/madskinner/klc2layout/issues',
        'Funding': 'https://donate.pypi.org',
        'English docs': ' https://klc2layout.readthedocs.org',
        'Docs en français': ' https://klc2layout.readthedocs.org',
        'Source': 'https://github.com/madskinner/klc2layout/',
    },
    include_package_data=True
)
