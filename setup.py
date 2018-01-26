import setuptools

setuptools.setup(name='communautopy',
                 version='0.1',
                 description='Communauto Python client library',
                 long_description=open('README.md').read().strip(),
                 author='isra17',
                 author_email='isra017@gmail.com',
                 url='https://github.com/isra17/communautopy',
                 packages=['communauto'],
                 install_requires=['zeep', 'haversine', 'googlemaps'],
                 python_requires='>=3.5',
                 license='GNU General Public License v3 (GPLv3)')
