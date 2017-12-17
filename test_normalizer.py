import unittest
from normalizer import Normalizer

class NormalizerTest(unittest.TestCase):
  def setUp(self):
    self.normalizer = Normalizer()

  def test_removes_quotes(self):
    self.assertEqual('bar', self.normalizer.normalize('"b\'a\'r"'))
    self.assertEqual('barbaz', self.normalizer.normalize('"bar"\'baz\''))
    # weird quotes
    self.assertEqual('foobar', self.normalizer.normalize('foo’bar'))
    self.assertEqual('foobar', self.normalizer.normalize('foo”bar'))
    self.assertEqual('foobar', self.normalizer.normalize('foo“bar'))

  def test_replaces_spaces_with_underscores(self):
    self.assertEqual('foo_bar', self.normalizer.normalize('foo bar'))

  def test_replaces_parens_with_underscores(self):
    self.assertEqual('_foobar_', self.normalizer.normalize('(foobar)'))
    self.assertEqual('_foobar_', self.normalizer.normalize('[foobar]'))

  def test_replaces_characters(self):
    self.assertEqual('band_song', self.normalizer.normalize('band_-_song'))
    self.assertEqual('band_song', self.normalizer.normalize('band__song'))

  def test_only_normalizes_basename(self):
    self.assertEqual('one two/three_four', self.normalizer.normalize('one two/three four'))

  def test_checks_if_needs_normalization(self):
    self.assertTrue(self.normalizer.needs_normalizing('foo bar'))
    self.assertFalse(self.normalizer.needs_normalizing('foo_bar'))

  def test_does_not_mutilate_extension(self):
    self.assertEqual('foo_bar.mp3', self.normalizer.normalize('foo bar.mp3'))
