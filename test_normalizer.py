import unittest
from normalizer import Normalizer

class NormalizerTest(unittest.TestCase):
  def setUp(self):
    self.normalizer = Normalizer()

  def test_removes_quotes(self):
    self.assertEqual('bar', self.normalizer.normalize('"b\'a\'r"'))
    self.assertEqual('barbaz', self.normalizer.normalize('"bar"\'baz\''))

  def test_replaces_spaces_with_underscores(self):
    self.assertEqual('foo_bar', self.normalizer.normalize('foo bar'))

  def test_replaces_dots_with_underscores(self):
    self.assertEqual('foo_bar', self.normalizer.normalize('foo.bar'))

  def test_only_normalizes_basename(self):
    self.assertEqual('one two/three_four', self.normalizer.normalize('one two/three four'))

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

  def test_checks_if_needs_normalization(self):
    self.assertTrue(self.normalizer.needs_normalizing('foo bar'))
    self.assertFalse(self.normalizer.needs_normalizing('foo_bar'))
