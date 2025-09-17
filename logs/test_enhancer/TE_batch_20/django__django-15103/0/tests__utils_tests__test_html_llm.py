def test_json_script_empty_string_id(self):
    self.assertEqual(json_script('a', ''), '<script type="application/json">"a"</script>')

def test_json_script_zero_id(self):
    self.assertEqual(json_script('a', 0), '<script type="application/json">"a"</script>')

def test_json_script_false_id(self):
    self.assertEqual(json_script('a', False), '<script type="application/json">"a"</script>')

def test_json_script_empty_list_id(self):
    self.assertEqual(json_script('a', []), '<script type="application/json">"a"</script>')

def test_json_script_string_zero_id(self):
    self.assertEqual(json_script('a', '0'), '<script id="0" type="application/json">"a"</script>')

def test_json_script_integer_id(self):
    self.assertEqual(json_script('a', 1), '<script id="1" type="application/json">"a"</script>')

def test_json_script_mark_safe_id(self):
    self.assertEqual(json_script('a', mark_safe('good')), '<script id="good" type="application/json">"a"</script>')

def test_json_script_lazystr_id(self):
    self.assertEqual(json_script('a', lazystr('lazyid')), '<script id="lazyid" type="application/json">"a"</script>')

def test_json_script_escaped_id(self):
    self.assertEqual(json_script('a', '<bad>'), '<script id="&lt;bad&gt;" type="application/json">"a"</script>')

def test_json_script_space_id(self):
    self.assertEqual(json_script('a', ' '), '<script id=" " type="application/json">"a"</script>')