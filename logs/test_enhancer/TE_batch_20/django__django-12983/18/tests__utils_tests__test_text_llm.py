def test_slugify_strip_only_dashes(self):
    self.assertEqual(text.slugify('---'), '')

def test_slugify_strip_only_underscores(self):
    self.assertEqual(text.slugify('___'), '')

def test_slugify_strip_only_spaces(self):
    self.assertEqual(text.slugify('   '), '')

def test_slugify_strip_spaces_and_dashes(self):
    self.assertEqual(text.slugify(' - '), '')

def test_slugify_strip_leading_trailing_mix(self):
    self.assertEqual(text.slugify('-__abc__-'), 'abc')

def test_slugify_strip_leading_trailing_underscores(self):
    self.assertEqual(text.slugify('__foo__'), 'foo')

def test_slugify_preserve_internal_underscores(self):
    self.assertEqual(text.slugify('foo__bar'), 'foo__bar')

def test_slugify_mixed_edge_chars(self):
    self.assertEqual(text.slugify('_-foo-_'), 'foo')

def test_slugify_spaces_underscores_and_chars(self):
    self.assertEqual(text.slugify('  _  example  _  '), 'example')

def test_slugify_collapse_then_strip(self):
    self.assertEqual(text.slugify('   - -  '), '')