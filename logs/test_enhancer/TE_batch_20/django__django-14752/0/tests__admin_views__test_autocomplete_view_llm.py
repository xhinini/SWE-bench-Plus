def test_serialize_result_override_adds_extra_field(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'extra': 'YES'}
    Question.objects.create(question='Alpha')
    request = self.factory.get(self.url, {'term': 'alpha', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['extra'], 'YES')

def test_serialize_result_override_changes_text(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['text'] = base['text'].upper()
            return base
    q = Question.objects.create(question='lowercase')
    request = self.factory.get(self.url, {'term': 'lower', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['text'], q.question.upper())

def test_serialize_result_override_changes_id_for_custom_to_field(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'id': f'pref-{getattr(obj, to_field_name)}', 'text': str(obj)}
    q = Question.objects.create(question='What?', uuid=None)
    q.uuid = q.uuid or q.pk
    q.save()
    opts = {'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question_with_to_field'}
    request = self.factory.get(self.url, {'term': 'what', **opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertTrue(data['results'][0]['id'].startswith('pref-'))

def test_serialize_result_used_on_both_pages(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'from_override': True}
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertTrue(all((r.get('from_override') is True for r in data['results'])))
    request = self.factory.get(self.url, {'term': '', 'page': '2', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertTrue(all((r.get('from_override') is True for r in data['results'])))

def test_serialize_result_for_mti_target_models(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'marker': 'mti'}
    o = Employee.objects.create(name='Ada Lovelace', gender=2, code='ada', alive=True)
    opts = {'app_label': WorkHour._meta.app_label, 'model_name': WorkHour._meta.model_name, 'field_name': 'employee'}
    request = self.factory.get(self.url, {'term': 'ada', **opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['text'], o.name)
    self.assertEqual(data['results'][0]['marker'], 'mti')

def test_default_serialize_result_generates_string_id(self):
    Question.objects.create(question='One')
    request = self.factory.get(self.url, {'term': 'one', **self.opts})
    request.user = self.superuser
    response = AutocompleteJsonView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertTrue(isinstance(data['results'][0]['id'], str))

def test_serialize_result_with_custom_pk_field_returns_expected_value(self):
    q = Question.objects.create(question='CustomPKTest')
    opts = {'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'related_questions'}
    request = self.factory.get(self.url, {'term': 'custompk', **self.opts})
    request.user = self.superuser
    response = AutocompleteJsonView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], str(q.pk))

def test_serialize_result_not_called_when_permission_denied_early(self):

    class CustomView(AutocompleteJsonView):
        called = 0

        def serialize_result(self, obj, to_field_name):
            type(self).called += 1
            raise AssertionError('serialize_result() should not be called when permission denied')
    Question.objects.create(question='permtest')
    request = self.factory.get(self.url, {'term': 'permtest', **self.opts})
    request.user = self.user
    with self.assertRaises(PermissionDenied):
        CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(CustomView.called, 0)

def test_serialize_result_can_call_super_and_extend(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['posted_str'] = getattr(obj, 'posted', None) and str(obj.posted)
            return base
    Question.objects.create(question='QwithDate', posted=datetime.date(2021, 1, 1))
    request = self.factory.get(self.url, {'term': 'qwith', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIn('posted_str', data['results'][0])
    self.assertEqual(data['results'][0]['posted_str'], str(Question.objects.get(question='QwithDate').posted))