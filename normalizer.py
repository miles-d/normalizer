import os, sys

class Normalizer:
  def normalize(self, name):
    dirname = os.path.dirname(name)
    basename = self.replace_nasty_chars(os.path.basename(name))

    if dirname:
      return dirname + '/' + basename
    return basename

  def replace_nasty_chars(self, basename):
    replacements = {
        '"': '',
        '\'': '',
        ' ': '_',
        '.': '_',
        }

    for old, new in replacements.items():
      basename = basename.replace(old, new)
    return basename

  def normalize_in_dir(self, dirname):
    normalized_paths = map(self.normalize, self.get_files(dirname))
    return list(normalized_paths)

  def get_files(self, dirname):
    dirs = []
    for dirpath, dirnames, filenames in os.walk(dirname):
      for filename in filenames:
        dirs.append(os.path.join(dirpath, filename))
    dirs = map(lambda p: p[len(dirname)+1:], dirs)
    return list(dirs)

  def needs_normalizing(self, name):
    return name != self.normalize(name)


if __name__ == '__main__':
  normalizer = Normalizer()
  dirname = sys.argv[1]
  dry_run = len(sys.argv) > 2 and sys.argv[2] == '--dry-run'
  files = normalizer.get_files(dirname)
  if dry_run:
    for f in files:
      print('old name: ' + f)
      print('new name: ' + normalizer.normalize(f))
  else:
    for f in files:
      realname = dirname + '/' + f
      if normalizer.needs_normalizing(f):
        os.rename(realname, normalizer.normalize(realname))
