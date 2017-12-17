import unittest, os
from normalizer import Normalizer

class NormalizerIntegratedTest(unittest.TestCase):
  def setUp(self):
    self.normalizer = Normalizer()
    dirs = [
        'testdir',
        'testdir/subdir',
        'testdir/subdir/nasty subdir',
        'testdir/subdir/subsubdir',
        ]
    for d in dirs:
      os.mkdir(d)

    files = [
        'testdir/one',
        'testdir/two',
        'testdir/subdir/foo bar',
        'testdir/subdir/three',
        'testdir/subdir/subsubdir/four',
        'testdir/subdir/nasty subdir/nasty file',
        ]
    for f in files:
      os.mknod(f)

  def tearDown(self):
    os.system('rm -rf testdir')

  def test_sees_files_from_directory(self):
    expected_names = {
        'one',
        'two',
        'subdir/three',
        'subdir/subsubdir/four',
        'subdir/foo bar',
        'subdir/nasty subdir/nasty file',
        }
    self.assertEqual(expected_names, set(self.normalizer.get_files('testdir')))

  def test_normalizes_nested(self):
    normalized_names = {
        'one',
        'two',
        'subdir/three',
        'subdir/subsubdir/four',
        'subdir/foo_bar',
        'subdir/nasty subdir/nasty_file',
        }
    self.assertEqual(normalized_names, set(self.normalizer.normalize_in_dir('testdir')))
