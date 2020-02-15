"""Old test suite expressed as pytest-type functions.

This module exposes the old test suite as module-level test_xxx()
functions recognized by pytest.

We should start writing unittests as functions (or classes) that
pytest works with.  We can also port the old tests to that form, where
it matters.

Either way: The goal is that the list of tests provided by this module
becomes shorter, and the list of tests in other modules becomes
longer."""


from pathlib import Path
import runpy
from typing import Dict, Any, Generator
import unittest

import ase.test as asetest


class TestModule:
    ignorefiles = {'__init__.py', 'testsuite.py', 'newtestsuite.py',
                   'conftest.py'}
    testdir = Path(asetest.__file__).parent

    def __init__(self, testname: str):
        # Testname is e.g. "fio.dftb".
        # Referring to the file ase/test/fio/dftb.py
        # or the module ase.test.fio.dftb
        self.testname = testname

    @property
    def module(self) -> str:
        return 'ase.test.{}'.format(self.testname)

    @property
    def path(self) -> Path:
        return Path(self.module.replace('.', '/') + '.py')

    @property
    def is_pytest_style(self) -> bool:
        # Files named test_* or *_test are are picked up by pytest
        # automatically.  We call these "pytest-style" modules.
        #
        # The other modules must be for our own old test suite.
        name = self.path.name
        return 'test_' in name or '_test' in name

    @classmethod
    def from_relpath(cls, relpath) -> "TestModule":
        module = TestModule.relpath2module(relpath)
        return TestModule(module)

    @staticmethod
    def filename_to_testname(filename):
        name, py = str(filename).rsplit('.', 1)
        assert py == 'py'
        return name.replace('/', '.')

    def __repr__(self):
        return 'TestModule(\'{}\')'.format(self.testname)

    @property
    def pytest_function_name(self):
        return 'test_' + self.testname.replace('.', '_')

    @property
    def pytest_identifier(self):
        if self.is_pytest_style:
            return 'test_modules.py::{}'.format(self.pytest_function_name)
        else:
            raise RuntimeError

    @classmethod
    def glob_all_test_modules(cls) -> "Generator[TestModule]":
        """Return a list of modules ['ase.test.xxx', 'ase.test.yyy', ...]."""
        testfiles = sorted(cls.testdir.glob('*.py'))
        testfiles += sorted(cls.testdir.glob('*/*.py'))
        # XXX Some tests were added at */*/*.py level, but the old test suite
        # never globbed so deep.  So these tests never ran.
        # We can/should rehabilitate them.

        for testfile in testfiles:
            if testfile.name in cls.ignorefiles:
                continue
            if '#' in testfile.name:
                continue  # Ignore certain backup files.
            rel_testfile = testfile.relative_to(cls.testdir)
            # We want to normalize the naming, hence as_posix():
            testname = cls.filename_to_testname(rel_testfile.as_posix())
            yield TestModule(testname)

    @classmethod
    def all_test_modules_as_dict(cls):
        dct = {}
        for mod in cls.glob_all_test_modules():
            dct[mod.testname] = mod
        return dct

    def define_script_test_function(self):
        module = self.module

        def test_script():
            try:
                runpy.run_module(module, run_name='test')
            except ImportError as ex:
                exmod = ex.args[0].split()[-1].replace("'", '').split('.')[0]
                if exmod in ['matplotlib', 'Scientific', 'lxml', 'Tkinter',
                             'flask', 'gpaw', 'GPAW', 'netCDF4', 'psycopg2',
                             'kimpy']:
                    raise unittest.SkipTest('no {} module'.format(exmod))
                else:
                    raise
            except Exception as ex:
                if 'no display name' in str(ex):
                    raise unittest.SkipTest('requires display: {}'.format(ex))
                else:
                    raise

        test_script.__name__ = self.pytest_function_name
        return test_script

    @classmethod
    def add_oldstyle_tests_to_namespace(cls, namespace: Dict[str, Any]):
        for testmodule in sorted(cls.glob_all_test_modules(),
                                 key=lambda module: module.testname):
            if testmodule.is_pytest_style:
                continue

            testfunc = testmodule.define_script_test_function()
            namespace[testfunc.__name__] = testfunc
