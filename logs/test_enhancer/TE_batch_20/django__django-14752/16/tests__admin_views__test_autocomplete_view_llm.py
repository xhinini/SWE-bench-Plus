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

def test_serialize_result_includes_custom_key(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'custom': 'yes'}
    q = Question.objects.create(question='Unique question')
    request = self.factory.get(self.url, {'term': 'unique', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['custom'], 'yes')

def test_serialize_result_present_on_paginated_first_page(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'custom': 'page1'}
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(len(data['results']), PAGINATOR_SIZE)
    for item in data['results']:
        self.assertEqual(item['custom'], 'page1')

def test_serialize_result_present_on_paginated_second_page(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'custom': 'page2'}
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', 'page': '2', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertTrue(len(data['results']) <= PAGINATOR_SIZE)
    for item in data['results']:
        self.assertEqual(item['custom'], 'page2')

def test_serialize_result_with_custom_to_field(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['to_field_value'] = str(getattr(obj, to_field_name))
            return base
    q = Question.objects.create(question='To field test')
    request = self.factory.get(self.url, {'term': 'to', **self.opts, 'field_name': 'question_with_to_field'})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], data['results'][0]['to_field_value'])

def test_serialize_result_in_distinct_search(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'extra': 'distinct'}
    q1 = Question.objects.create(question='d1')
    q2 = Question.objects.create(question='d2')
    q2.related_questions.add(q1)
    q3 = Question.objects.create(question='d3')
    q3.related_questions.add(q1)
    request = self.factory.get(self.url, {'term': 'd', **self.opts})
    request.user = self.superuser

    class DistinctQuestionAdmin(QuestionAdmin):
        search_fields = ['related_questions__question', 'question']
    with model_admin(Question, DistinctQuestionAdmin):
        response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    ids = {r['id'] for r in data['results']}
    self.assertGreaterEqual(len(ids), 3)
    for item in data['results']:
        self.assertEqual(item['extra'], 'distinct')

def test_serialize_result_with_mti_target(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'name_copy': str(obj)}
    o = Employee.objects.create(name='Selena', gender=2, code='x', alive=False)
    opts = {'app_label': WorkHour._meta.app_label, 'model_name': WorkHour._meta.model_name, 'field_name': 'employee'}
    request = self.factory.get(self.url, {'term': 'selena', **opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['name_copy'], data['results'][0]['text'])

def test_serialize_result_with_fk_pk_target(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'pk_str': str(obj.pk)}
    p = Parent.objects.create(name='ParentName')
    c = PKChild.objects.create(parent=p, name='ChildName')
    opts = {'app_label': Toy._meta.app_label, 'model_name': Toy._meta.model_name, 'field_name': 'child'}
    request = self.factory.get(self.url, {'term': 'child', **opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['pk_str'], data['results'][0]['id'])

def test_serialize_result_respects_limit_choices_to(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'notes': getattr(obj, 'question', '')}
    q = Question.objects.create(question='Allowed question')
    Question.objects.create(question='not allowed')
    request = self.factory.get(self.url, {'term': 'allowed', **self.opts, 'field_name': 'question_with_to_field'})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(len(data['results']), 1)
    self.assertEqual(data['results'][0]['notes'], q.question)

def test_serialize_result_with_multiple_results_includes_custom_key(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'flag': 'multi'}
    Question.objects.create(question='Alpha')
    Question.objects.create(question='Beta')
    request = self.factory.get(self.url, {'term': '', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertGreaterEqual(len(data['results']), 2)
    for r in data['results']:
        self.assertEqual(r['flag'], 'multi')

def test_serialize_result_adds_extra_key(self):

    class ExtraFieldAutocomplete(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'extra': f'extra-{obj.pk}'}
    Question.objects.create(question='Q1')
    Question.objects.create(question='Q2')
    request = self.factory.get(self.url, {'term': 'question', **self.opts})
    request.user = self.superuser
    response = ExtraFieldAutocomplete.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    expected = [{'id': str(q.pk), 'text': q.question, 'extra': f'extra-{q.pk}'} for q in Question.objects.order_by('-posted')[:Paginator if False else Question.objects.count()]]
    self.assertEqual(len(data['results']), Question.objects.count())
    for item in data['results']:
        self.assertIn('extra', item)
        self.assertTrue(item['extra'].startswith('extra-'))

def test_serialize_result_prefixes_id_for_custom_to_field(self):

    class PrefixIdAutocomplete(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            original = super().serialize_result(obj, to_field_name)
            original['id'] = 'ID-' + original['id']
            return original
    q = Question.objects.create(question='Is this a question?')
    request = self.factory.get(self.url, {'term': 'is', **self.opts, 'field_name': 'question_with_to_field'})
    request.user = self.superuser
    response = PrefixIdAutocomplete.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'], [{'id': 'ID-' + str(q.uuid), 'text': q.question}])

def test_serialize_result_preserves_ordering_and_adds_posted(self):

    class PostedAutocomplete(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'posted': str(getattr(obj, 'posted', ''))}
    Question.objects.create(question='Question 1', posted=datetime.date(2021, 8, 9))
    Question.objects.create(question='Question 2', posted=datetime.date(2021, 8, 7))
    request = self.factory.get(self.url, {'term': 'question', **self.opts})
    request.user = self.superuser
    response = PostedAutocomplete.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    expected = [{'id': str(q.pk), 'text': q.question, 'posted': str(q.posted)} for q in Question.objects.order_by('-posted')]
    self.assertEqual(data['results'], expected)

def test_serialize_result_applies_on_paginated_second_page(self):

    class SeqAutocomplete(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'seq': str(obj.pk)}

    class PKOrderingQuestionAdmin(QuestionAdmin):
        ordering = ['pk']
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', 'page': '2', **self.opts})
    request.user = self.superuser
    with model_admin(Question, PKOrderingQuestionAdmin):
        response = SeqAutocomplete.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    expected_objs = Question.objects.order_by('pk')[PAGINATOR_SIZE:]
    self.assertEqual([r['seq'] for r in data['results']], [str(q.pk) for q in expected_objs])

def test_serialize_result_applies_with_search_use_distinct(self):

    class DistinctSerializer(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'pkstr': str(obj.pk)}
    q1 = Question.objects.create(question='question 1')
    q2 = Question.objects.create(question='question 2')
    q2.related_questions.add(q1)
    q3 = Question.objects.create(question='question 3')
    q3.related_questions.add(q1)
    request = self.factory.get(self.url, {'term': 'question', **self.opts})
    request.user = self.superuser

    class DistinctQuestionAdmin(QuestionAdmin):
        search_fields = ['related_questions__question', 'question']
    with model_admin(Question, DistinctQuestionAdmin):
        response = DistinctSerializer.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(len(data['results']), 3)
    for r in data['results']:
        self.assertIn('pkstr', r)

def test_serialize_result_applies_for_mti_to_field(self):

    class MTISerializer(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'name': str(getattr(obj, 'name', ''))}
    o = Employee.objects.create(name='Frida Kahlo', gender=2, code='painter', alive=False)
    opts = {'app_label': WorkHour._meta.app_label, 'model_name': WorkHour._meta.model_name, 'field_name': 'employee'}
    request = self.factory.get(self.url, {'term': 'frida', **opts})
    request.user = self.superuser
    response = MTISerializer.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data, {'results': [{'id': str(o.pk), 'text': o.name, 'name': o.name}], 'pagination': {'more': False}})

def test_serialize_result_applies_for_fk_pk_to_field(self):

    class FKPKSerializer(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {**super().serialize_result(obj, to_field_name), 'name_upper': str(getattr(obj, 'name', '')).upper()}
    p = Parent.objects.create(name='Bertie')
    c = PKChild.objects.create(parent=p, name='Anna')
    opts = {'app_label': Toy._meta.app_label, 'model_name': Toy._meta.model_name, 'field_name': 'child'}
    request = self.factory.get(self.url, {'term': 'anna', **opts})
    request.user = self.superuser
    response = FKPKSerializer.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data, {'results': [{'id': str(c.pk), 'text': c.name, 'name_upper': c.name.upper()}], 'pagination': {'more': False}})

def test_serialize_result_exception_propagates(self):

    class ErrorSerializer(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            raise RuntimeError('serializer failure')
    Question.objects.create(question='Will fail')
    request = self.factory.get(self.url, {'term': 'will', **self.opts})
    request.user = self.superuser
    with self.assertRaises(RuntimeError):
        ErrorSerializer.as_view(**self.as_view_args)(request)

def test_serialize_result_called_for_each_result(self):
    calls = []

    class CountingSerializer(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            calls.append(obj.pk)
            return super().serialize_result(obj, to_field_name)
    q1 = Question.objects.create(question='A')
    q2 = Question.objects.create(question='B')
    q3 = Question.objects.create(question='C')
    request = self.factory.get(self.url, {'term': '', **self.opts})
    request.user = self.superuser
    response = CountingSerializer.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(len(calls), len(data['results']))
    returned_pks = {int(r['id']) for r in data['results']}
    self.assertEqual(set(calls), returned_pks)

def test_default_serialize_result_returns_id_and_text(self):
    q = Question.objects.create(question='Default test')
    request = self.factory.get(self.url, {'term': 'default', **self.opts})
    request.user = self.superuser
    response = AutocompleteJsonView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data, {'results': [{'id': str(q.pk), 'text': q.question}], 'pagination': {'more': False}})

def test_serialize_result_override_custom_to_field(self):
    """serialize_result() override is used for custom to_field (UUID)."""

    class CustomSerializeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['custom'] = 'yes'
            return data
    q = Question.objects.create(question='Is this a question?')
    request = self.factory.get(self.url, {'term': 'is', **{'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question_with_to_field'}})
    request.user = self.superuser
    response = CustomSerializeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], str(q.uuid))
    self.assertEqual(data['results'][0]['custom'], 'yes')

def test_serialize_result_override_pagination_first_page(self):
    """serialize_result() can access request and reflect page (first page)."""

    class PageSerializeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['page'] = self.request.GET.get('page', '1')
            return data
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', **{'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'}})
    request.user = self.superuser
    response = PageSerializeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    for r in data['results']:
        self.assertEqual(r['page'], '1')

def test_serialize_result_override_pagination_second_page(self):
    """serialize_result() can access request and reflect page (second page)."""

    class PageSerializeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['page'] = self.request.GET.get('page', '1')
            return data
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', 'page': '2', **{'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'}})
    request.user = self.superuser
    response = PageSerializeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    for r in data['results']:
        self.assertEqual(r['page'], '2')

def test_serialize_result_override_with_distinct(self):
    """serialize_result() is used when get_search_results requests distinct()."""

    class CustomDistinctView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['distinct_used'] = True
            return data
    q1 = Question.objects.create(question='question 1')
    q2 = Question.objects.create(question='question 2')
    q2.related_questions.add(q1)
    q3 = Question.objects.create(question='question 3')
    q3.related_questions.add(q1)
    request = self.factory.get(self.url, {'term': 'question', **{'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'}})
    request.user = self.superuser

    class DistinctQuestionAdmin(QuestionAdmin):
        search_fields = ['related_questions__question', 'question']
    with model_admin(Question, DistinctQuestionAdmin):
        response = CustomDistinctView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(len(data['results']), 3)
    for r in data['results']:
        self.assertTrue(r.get('distinct_used'))

def test_serialize_result_override_mti_employee(self):
    """serialize_result() override is respected for MTI target models (Employee/WorkHour)."""

    class MTISerializeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['mti'] = True
            return data
    o = Employee.objects.create(name='Frida Kahlo', gender=2, code='painter', alive=False)
    opts = {'app_label': WorkHour._meta.app_label, 'model_name': WorkHour._meta.model_name, 'field_name': 'employee'}
    request = self.factory.get(self.url, {'term': 'frida', **opts})
    request.user = self.superuser
    response = MTISerializeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], str(o.pk))
    self.assertTrue(data['results'][0]['mti'])

def test_serialize_result_override_mti_manager(self):
    """serialize_result() override is respected for multi-level MTI (Manager/Bonus)."""

    class MTISerializeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['mti'] = 'manager'
            return data
    o = Manager.objects.create(name='Frida Kahlo', gender=2, code='painter', alive=False)
    opts = {'app_label': Bonus._meta.app_label, 'model_name': Bonus._meta.model_name, 'field_name': 'recipient'}
    request = self.factory.get(self.url, {'term': 'frida', **opts})
    request.user = self.superuser
    response = MTISerializeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], str(o.pk))
    self.assertEqual(data['results'][0]['mti'], 'manager')

def test_serialize_result_override_fk_pk(self):
    """serialize_result() override is respected for FK with PK target."""

    class FKSerializeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['fk_pk'] = getattr(obj, to_field_name)
            return data
    p = Parent.objects.create(name='Bertie')
    c = PKChild.objects.create(parent=p, name='Anna')
    opts = {'app_label': Toy._meta.app_label, 'model_name': Toy._meta.model_name, 'field_name': 'child'}
    request = self.factory.get(self.url, {'term': 'anna', **opts})
    request.user = self.superuser
    response = FKSerializeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], str(c.pk))
    self.assertEqual(str(data['results'][0]['fk_pk']), str(c.pk))

def test_serialize_result_override_limit_choices_to(self):
    """serialize_result() override is used when limit_choices_to filters results."""

    class LimitSerializeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['limited'] = True
            return data
    q = Question.objects.create(question='Is this a question?')
    Question.objects.create(question='Not a question.')
    request = self.factory.get(self.url, {'term': 'is', **{'app_label': Answer._meta.app_label, 'model_name': Answer._meta.model_name, 'field_name': 'question_with_to_field'}})
    request.user = self.superuser
    response = LimitSerializeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'], [{'id': str(q.uuid), 'text': q.question, 'limited': True}])

def test_serialize_result_custom_id_format(self):
    """serialize_result() can customize the id format (prefix)."""

    class CustomIDView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['id'] = 'custom-' + data['id']
            return data
    q = Question.objects.create(question='Prefix test')
    request = self.factory.get(self.url, {'term': 'prefix', **{'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'}})
    request.user = self.superuser
    response = CustomIDView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], 'custom-' + str(q.pk))

def test_serialize_result_called_for_all_results(self):
    """serialize_result() is invoked for every object returned by the view."""

    class CalledSerializeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['called_for'] = obj.pk
            return data
    qs = [Question.objects.create(question=f'Q{i}') for i in range(3)]
    request = self.factory.get(self.url, {'term': 'Q', **{'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'}})
    request.user = self.superuser
    response = CalledSerializeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    returned_pks = {int(r['called_for']) for r in data['results']}
    expected_pks = {q.pk for q in qs}
    self.assertEqual(returned_pks, expected_pks)

def test_regression_serialize_result_override_prefix_id(self):
    """
    Overriding serialize_result should affect the 'id' value in the JSON.
    """

    class PrefixIdView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['id'] = 'X-' + base['id']
            return base
    q = Question.objects.create(question='Prefix Test')
    request = self.factory.get(self.url, {'term': 'prefix', 'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'})
    request.user = self.superuser
    response = PrefixIdView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], 'X-' + str(q.pk))

def test_regression_serialize_result_override_change_text(self):
    """serialize_result override can change the text shown in results."""

    class UpperTextView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['text'] = base['text'].upper()
            return base
    q = Question.objects.create(question='who is who')
    request = self.factory.get(self.url, {'term': 'who', 'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'})
    request.user = self.superuser
    response = UpperTextView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['text'], q.question.upper())

def test_regression_serialize_result_used_with_custom_to_field(self):
    """
    When a field defines a custom to_field (e.g., uuid), serialize_result is
    still invoked and receives the to_field_name that references the correct
    attribute.
    """

    class CustomToFieldView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'id': 'UID-' + str(getattr(obj, to_field_name)), 'text': str(obj)}
    q = Question.objects.create(question='UUID Test')
    request = self.factory.get(self.url, {'term': 'uuid', 'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question_with_to_field'})
    request.user = self.superuser
    response = CustomToFieldView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertTrue(data['results'][0]['id'].startswith('UID-'))

def test_regression_serialize_result_exception_propagates(self):
    """Exceptions raised in serialize_result should propagate (not be swallowed)."""

    class ExplodingView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            raise RuntimeError('boom')
    Question.objects.create(question='boom test')
    request = self.factory.get(self.url, {'term': 'boom', 'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'})
    request.user = self.superuser
    with self.assertRaises(RuntimeError):
        ExplodingView.as_view(**self.as_view_args)(request)

def test_regression_default_serialize_result_returns_id_and_text(self):
    """The default serialize_result returns 'id' and 'text' for an object."""
    q = Question.objects.create(question='Default serialize')
    request = self.factory.get(self.url, {'term': 'default', 'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'})
    request.user = self.superuser
    response = AutocompleteJsonView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIn('id', data['results'][0])
    self.assertIn('text', data['results'][0])
    self.assertEqual(data['results'][0]['id'], str(q.pk))
    self.assertEqual(data['results'][0]['text'], q.question)

def test_regression_serialize_result_preserves_ordering(self):
    """
    serialize_result should not affect queryset ordering. When overriding,
    results ordering (e.g., by posted date) remains intact.
    """

    class PostedView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['posted'] = str(obj.posted)
            return base
    Question.objects.create(question='Q1', posted=datetime.date(2021, 8, 9))
    Question.objects.create(question='Q2', posted=datetime.date(2021, 8, 7))
    request = self.factory.get(self.url, {'term': 'question', 'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'})
    request.user = self.superuser
    response = PostedView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    posted_dates = [d['posted'] for d in data['results']]
    self.assertEqual(posted_dates, sorted(posted_dates, reverse=True))

def test_regression_serialize_result_not_called_if_no_permission(self):
    """
    If the requesting user lacks permission, has_perm should short-circuit and
    serialize_result should never be called.
    """

    class AssertNotCalledView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            raise AssertionError('serialize_result should not be called when permission is denied')
    request = self.factory.get(self.url, {'term': 'is', **self.opts})
    request.user = self.user
    with self.assertRaises(PermissionDenied):
        AssertNotCalledView.as_view(**self.as_view_args)(request)

def test_regression_serialize_result_with_mti(self):
    """
    Ensure serialize_result works for MTI target models (Employee/WorkHour,
    Manager/Bonus cases) and receives the correct to_field.
    """

    class MTIView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['marker'] = 'mti'
            return base
    o = Employee.objects.create(name='Frida Kahlo', gender=2, code='painter', alive=False)
    opts = {'app_label': WorkHour._meta.app_label, 'model_name': WorkHour._meta.model_name, 'field_name': 'employee'}
    request = self.factory.get(self.url, {'term': 'frida', **opts})
    request.user = self.superuser
    response = MTIView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['text'], o.name)
    self.assertEqual(data['results'][0]['marker'], 'mti')

def test_regression_serialize_result_pagination_call_count(self):
    """
    serialize_result should be called only for objects on the requested page.
    """
    call_log = []

    class CountingView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            call_log.append(obj.pk)
            return super().serialize_result(obj, to_field_name)
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', 'page': '1', 'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question'})
    request.user = self.superuser
    call_log.clear()
    response = CountingView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(len(call_log), PAGINATOR_SIZE)
    self.assertEqual(len(data['results']), PAGINATOR_SIZE)

def test_regression_serialize_result_resolves_to_field_attname(self):
    """
    Ensure serialize_result receives the resolved to_field_name which is the
    attname of the target field (e.g. for related_questions custom pk).
    """

    class ToFieldInspectView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'id_field_used': to_field_name, 'text': str(obj)}
    q = Question.objects.create(question='ToField Test')
    opts = {'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'related_questions'}
    request = self.factory.get(self.url, {'term': 'tofield', **opts})
    request.user = self.superuser
    request = self.factory.get(self.url, {'term': 'is', 'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question_with_to_field'})
    request.user = self.superuser
    response = ToFieldInspectView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIsInstance(data['results'][0]['id_field_used'], str)

def test_serialize_result_adds_extra_field(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['extra'] = self.request.user.username
            return base
    Question.objects.create(question='Q1')
    request = self.factory.get(self.url, {'term': 'q', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIn('extra', data['results'][0])
    self.assertEqual(data['results'][0]['extra'], self.superuser.username)

def test_serialize_result_can_change_id_format(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'id': 'custom-%s' % getattr(obj, to_field_name), 'text': str(obj)}
    q = Question.objects.create(question='Unique')
    request = self.factory.get(self.url, {'term': 'uniq', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data, {'results': [{'id': 'custom-%s' % str(q.pk), 'text': q.question}], 'pagination': {'more': False}})

def test_serialize_result_with_custom_to_field_uuid(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'id': str(getattr(obj, to_field_name)), 'text': str(obj), 'used_to_field': to_field_name}
    q = Question.objects.create(question='HasUUID')
    opts = {'app_label': Answer._meta.app_label, 'model_name': Answer._meta.model_name, 'field_name': 'question_with_to_field'}
    request = self.factory.get(self.url, {'term': 'has', **opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], str(Question.objects.get(pk=q.pk).uuid))
    self.assertIn('used_to_field', data['results'][0])

def test_serialize_result_with_fk_pk_to_field(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'id': str(getattr(obj, to_field_name)), 'text': str(obj), 'note': 'fk-pk'}
    p = Parent.objects.create(name='Parent1')
    c = PKChild.objects.create(parent=p, name='ChildAnna')
    opts = {'app_label': Toy._meta.app_label, 'model_name': Toy._meta.model_name, 'field_name': 'child'}
    request = self.factory.get(self.url, {'term': 'Anna', **opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data, {'results': [{'id': str(c.pk), 'text': c.name, 'note': 'fk-pk'}], 'pagination': {'more': False}})

def test_serialize_result_handles_unicode_text(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['extra'] = 'café'
            return base
    q = Question.objects.create(question='café question')
    request = self.factory.get(self.url, {'term': 'café', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['text'], q.question)
    self.assertEqual(data['results'][0]['extra'], 'café')

def test_serialize_result_applies_on_second_page(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['page_marker'] = self.request.GET.get('page', '1')
            return base
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', 'page': '2', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    for r in data['results']:
        self.assertEqual(r['page_marker'], '2')

def test_serialize_result_can_use_admin_site_attribute(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['site_name'] = self.admin_site.name
            return base
    q = Question.objects.create(question='Meta')
    request = self.factory.get(self.url, {'term': 'meta', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['site_name'], site.name)

def test_serialize_result_respects_distinct_queries(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['extra'] = 'x'
            return base
    q1 = Question.objects.create(question='question 1')
    q2 = Question.objects.create(question='question 2')
    q2.related_questions.add(q1)
    q3 = Question.objects.create(question='question 3')
    q3.related_questions.add(q1)
    request = self.factory.get(self.url, {'term': 'question', **self.opts})
    request.user = self.superuser

    class DistinctQuestionAdmin(QuestionAdmin):
        search_fields = ['related_questions__question', 'question']
    with model_admin(Question, DistinctQuestionAdmin):
        response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(len(data['results']), 3)
    for item in data['results']:
        self.assertIn('extra', item)

def test_serialize_result_safe_fallback_when_str_is_not_used(self):

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'id': str(getattr(obj, to_field_name)), 'text': '[safe]'}
    q = Question.objects.create(question='UnsafeStr')
    request = self.factory.get(self.url, {'term': 'unsafe', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['text'], '[safe]')

import json
from django.core.exceptions import PermissionDenied
from django.test import override_settings
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from .models import Question, WorkHour, Employee, PKChild, Toy

def _attach_tests(cls):

    def test_serialize_result_override_invoked(self):
        """
        Overriding serialize_result() should be invoked for every object in the
        results. Track calls and ensure the number of calls matches the number
        of results.
        """

        class TrackView(AutocompleteJsonView):
            called = []

            def serialize_result(self, obj, to_field_name):
                self.__class__.called.append((obj.pk, to_field_name))
                return super().serialize_result(obj, to_field_name)
        q1 = Question.objects.create(question='Alpha question')
        q2 = Question.objects.create(question='Beta question')
        request = self.factory.get(self.url, {'term': 'question', **self.opts})
        request.user = self.superuser
        TrackView.called.clear()
        response = TrackView.as_view(**self.as_view_args)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(TrackView.called), 2)
        data = json.loads(response.content.decode('utf-8'))
        returned_ids = [int(r['id']) for r in data['results']]
        recorded_ids = [call[0] for call in TrackView.called]
        self.assertEqual(returned_ids, recorded_ids)

    def test_serialize_result_can_add_extra_key(self):
        """
        A subclass can augment the serialized result with extra keys and they
        should appear in the JSON response.
        """

        class ExtraKeyView(AutocompleteJsonView):

            def serialize_result(self, obj, to_field_name):
                base = super().serialize_result(obj, to_field_name)
                base['extra'] = f'extra-{obj.pk}'
                return base
        q = Question.objects.create(question='Unique question')
        request = self.factory.get(self.url, {'term': 'unique', **self.opts})
        request.user = self.superuser
        response = ExtraKeyView.as_view(**self.as_view_args)(request)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data['results']), 1)
        self.assertIn('extra', data['results'][0])
        self.assertEqual(data['results'][0]['extra'], f'extra-{q.pk}')

    def test_serialize_result_with_uuid_to_field(self):
        """
        When a related field defines a custom to_field (UUID), serialize_result
        should receive the resolved to_field_name and be able to use it.
        """

        class ToFieldView(AutocompleteJsonView):
            recorded_to_field = None
            recorded_value = None

            def serialize_result(self, obj, to_field_name):
                self.__class__.recorded_to_field = to_field_name
                self.__class__.recorded_value = getattr(obj, to_field_name)
                return super().serialize_result(obj, to_field_name)
        q = Question.objects.create(question='UUID question')
        opts = {'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question_with_to_field'}
        request = self.factory.get(self.url, {'term': 'uuid', **opts})
        request.user = self.superuser
        ToFieldView.recorded_to_field = None
        response = ToFieldView.as_view(**self.as_view_args)(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(str(ToFieldView.recorded_value), data['results'][0]['id'])

    def test_serialize_result_preserves_pagination_and_order(self):
        """
        Overriding serialize_result should not affect pagination or ordering.
        """

        class PassThroughView(AutocompleteJsonView):

            def serialize_result(self, obj, to_field_name):
                return super().serialize_result(obj, to_field_name)
        total = AutocompleteJsonView.paginate_by + 5
        Question.objects.bulk_create((Question(question=str(i)) for i in range(total)))
        request = self.factory.get(self.url, {'term': '', **self.opts})
        request.user = self.superuser
        response = PassThroughView.as_view(**self.as_view_args)(request)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data['results']), AutocompleteJsonView.paginate_by)
        self.assertTrue(data['pagination']['more'])
        request = self.factory.get(self.url, {'term': '', 'page': '2', **self.opts})
        request.user = self.superuser
        response = PassThroughView.as_view(**self.as_view_args)(request)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data['results']), total - AutocompleteJsonView.paginate_by)
        self.assertFalse(data['pagination']['more'])

    def test_serialize_result_called_with_correct_to_field_mti(self):
        """
        For MTI target models, serialize_result should be called with the
        correct to_field_name (primary key attname) and the id in the results
        should match the object's pk.
        """

        class MTIView(AutocompleteJsonView):
            recorded = []

            def serialize_result(self, obj, to_field_name):
                self.__class__.recorded.append((obj.pk, to_field_name))
                return super().serialize_result(obj, to_field_name)
        o = Employee.objects.create(name='MTI Person', gender=1, code='x', alive=True)
        opts = {'app_label': WorkHour._meta.app_label, 'model_name': WorkHour._meta.model_name, 'field_name': 'employee'}
        request = self.factory.get(self.url, {'term': 'MTI', **opts})
        request.user = self.superuser
        MTIView.recorded.clear()
        response = MTIView.as_view(**self.as_view_args)(request)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(MTIView.recorded[0][0], o.pk)
        self.assertEqual(data['results'][0]['id'], str(o.pk))

    def test_serialize_result_not_called_when_permission_denied(self):
        """
        If the user lacks permission, process_request/has_perm should raise
        PermissionDenied before serialize_result is called.
        """

        class SideEffectView(AutocompleteJsonView):
            called = False

            def serialize_result(self, obj, to_field_name):
                self.__class__.called = True
                return super().serialize_result(obj, to_field_name)
        q = Question.objects.create(question='Secret question')
        request = self.factory.get(self.url, {'term': 'secret', **self.opts})
        request.user = self.user
        SideEffectView.called = False
        with self.assertRaises(PermissionDenied):
            SideEffectView.as_view(**self.as_view_args)(request)
        self.assertFalse(SideEffectView.called)

    def test_serialize_result_with_fk_pk_field(self):
        """
        For a foreign key that uses the target model's PK, the to_field_name
        should resolve to the PK attname and the serialized id should use
        that value.
        """
        parent = PKChild.objects.create(parent=None, name='ParentName')
        c = PKChild.objects.create(parent=None, name='Anna')
        t = Toy.objects.create(child=c, name='Toy for Anna')
        opts = {'app_label': Toy._meta.app_label, 'model_name': Toy._meta.model_name, 'field_name': 'child'}

        class FKView(AutocompleteJsonView):
            recorded = None

            def serialize_result(self, obj, to_field_name):
                self.__class__.recorded = getattr(obj, to_field_name)
                return super().serialize_result(obj, to_field_name)
        request = self.factory.get(self.url, {'term': 'anna', **opts})
        request.user = self.superuser
        FKView.recorded = None
        response = FKView.as_view(**self.as_view_args)(request)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['results'][0]['id'], str(c.pk))
        self.assertEqual(str(FKView.recorded), data['results'][0]['id'])

    def test_serialize_result_can_modify_text(self):
        """
        Overriding serialize_result can modify the 'text' value (display
        label) and that modified value should be returned to the client.
        """

        class UpperTextView(AutocompleteJsonView):

            def serialize_result(self, obj, to_field_name):
                base = super().serialize_result(obj, to_field_name)
                base['text'] = base['text'].upper()
                return base
        q = Question.objects.create(question='Who am I?')
        request = self.factory.get(self.url, {'term': 'who', **self.opts})
        request.user = self.superuser
        response = UpperTextView.as_view(**self.as_view_args)(request)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['results'][0]['text'], q.question.upper())

    def test_serialize_result_preserves_ordering_by_field(self):
        """
        When serialize_result is overridden but does not change ordering,
        the ordering produced by ModelAdmin (for example ordering by posted)
        should be preserved in the results.
        """

        class PreserveOrderView(AutocompleteJsonView):
            recorded_ids = []

            def serialize_result(self, obj, to_field_name):
                self.__class__.recorded_ids.append(obj.pk)
                return super().serialize_result(obj, to_field_name)
        Question.objects.create(question='Q1', posted='2021-08-09')
        Question.objects.create(question='Q2', posted='2021-08-07')
        request = self.factory.get(self.url, {'term': 'question', **self.opts})
        request.user = self.superuser
        PreserveOrderView.recorded_ids.clear()
        response = PreserveOrderView.as_view(**self.as_view_args)(request)
        data = json.loads(response.content.decode('utf-8'))
        returned_ids = [int(r['id']) for r in data['results']]
        self.assertEqual(PreserveOrderView.recorded_ids, returned_ids)
    for name, func in list(locals().items()):
        if name.startswith('test_'):
            setattr(cls, name, func)
_attach_tests(AutocompleteJsonViewTests)

def test_serialize_result_adds_extra_key_override(self):
    """
    Overriding serialize_result should allow adding extra keys to the result.
    """

    class AddExtraFieldView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            base = super().serialize_result(obj, to_field_name)
            base['extra'] = 'X'
            return base
    Question.objects.create(question='Only one')
    request = self.factory.get(self.url, {'term': 'only', **self.opts})
    request.user = self.superuser
    response = AddExtraFieldView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIn('extra', data['results'][0])
    self.assertEqual(data['results'][0]['extra'], 'X')

def test_serialize_result_called_for_each_object(self):
    """
    serialize_result should be called once per returned object.
    """
    called = []

    class CountingView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            called.append(obj.pk)
            return super().serialize_result(obj, to_field_name)
    Question.objects.bulk_create((Question(question=f'Q{i}') for i in range(3)))
    request = self.factory.get(self.url, {'term': 'q', **self.opts})
    request.user = self.superuser
    response = CountingView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(called), 3)

def test_serialize_result_receives_custom_to_field(self):
    """
    When the field defines a custom to_field (question_with_to_field), the
    to_field_name passed to serialize_result should reflect the resolved attname.
    """
    seen = []

    class CaptureToFieldView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            seen.append(to_field_name)
            return super().serialize_result(obj, to_field_name)
    Question.objects.create(question='Has uuid')
    opts = {'app_label': Question._meta.app_label, 'model_name': Question._meta.model_name, 'field_name': 'question_with_to_field'}
    request = self.factory.get(self.url, {'term': 'has', **opts})
    request.user = self.superuser
    response = CaptureToFieldView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    expected = Question._meta.get_field('uuid').attname
    self.assertTrue(seen)
    self.assertEqual(seen[0], expected)

def test_serialize_result_on_mti_models(self):
    """
    serialize_result should be used for MTI target models (WorkHour -> Employee).
    """

    class ExtraMTIView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            res = super().serialize_result(obj, to_field_name)
            res['marker'] = 'mtitest'
            return res
    emp = Employee.objects.create(name='Frida Kahlo', gender=2, code='painter', alive=False)
    opts = {'app_label': WorkHour._meta.app_label, 'model_name': WorkHour._meta.model_name, 'field_name': 'employee'}
    request = self.factory.get(self.url, {'term': 'frida', **opts})
    request.user = self.superuser
    response = ExtraMTIView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['marker'], 'mtitest')

def test_serialize_result_on_fk_pk(self):
    """
    serialize_result should be used for FK-to-custom-pk situations (Toy -> PKChild).
    """

    class FKPKView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            r = super().serialize_result(obj, to_field_name)
            r['label'] = str(obj)
            return r
    p = Parent.objects.create(name='Bertie')
    c = PKChild.objects.create(parent=p, name='Anna')
    opts = {'app_label': Toy._meta.app_label, 'model_name': Toy._meta.model_name, 'field_name': 'child'}
    request = self.factory.get(self.url, {'term': 'anna', **opts})
    request.user = self.superuser
    response = FKPKView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['label'], str(c))

def test_serialize_result_respects_pagination(self):
    """
    serialize_result should only be called for the objects in the current page.
    """
    calls_page1 = []
    calls_page2 = []

    class CapturePageView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            if len(calls_page1) < PAGINATOR_SIZE:
                calls_page1.append(obj.pk)
            else:
                calls_page2.append(obj.pk)
            return super().serialize_result(obj, to_field_name)

    class PKOrderingQuestionAdmin(QuestionAdmin):
        ordering = ['pk']
    Question.objects.bulk_create((Question(question=str(i)) for i in range(PAGINATOR_SIZE + 5)))
    request = self.factory.get(self.url, {'term': '', **self.opts})
    request.user = self.superuser
    with model_admin(Question, PKOrderingQuestionAdmin):
        response = CapturePageView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(calls_page1), PAGINATOR_SIZE)
    request = self.factory.get(self.url, {'term': '', 'page': '2', **self.opts})
    request.user = self.superuser
    with model_admin(Question, PKOrderingQuestionAdmin):
        response = CapturePageView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(len(calls_page2) > 0)

def test_serialize_result_can_return_non_string_values(self):
    """
    serialize_result may return non-string values which should be preserved in JSON.
    """

    class NonStringView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'id': obj.pk, 'text': obj.question, 'num': 123}
    Question.objects.create(question='Numeric test')
    request = self.factory.get(self.url, {'term': 'numeric', **self.opts})
    request.user = self.superuser
    response = NonStringView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIsInstance(data['results'][0]['num'], int)
    self.assertEqual(data['results'][0]['num'], 123)

def test_serialize_result_exception_propagates(self):
    """
    If serialize_result raises an exception, it should propagate (resulting
    in an error) rather than being silently ignored.
    """

    class ErroringView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            raise ValueError('boom')
    Question.objects.create(question='Will error')
    request = self.factory.get(self.url, {'term': 'will', **self.opts})
    request.user = self.superuser
    with self.assertRaises(ValueError):
        ErroringView.as_view(**self.as_view_args)(request)

def test_serialize_result_called_with_model_instance(self):
    """
    serialize_result should receive actual model instances (not dicts or pks).
    """
    seen = []

    class TypeCheckView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            seen.append(isinstance(obj, Question))
            return super().serialize_result(obj, to_field_name)
    Question.objects.create(question='Type check')
    request = self.factory.get(self.url, {'term': 'type', **self.opts})
    request.user = self.superuser
    response = TypeCheckView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(all(seen))

def test_serialize_result_allows_arbitrary_shape(self):
    """
    serialize_result can return a completely different shape and it will be
    used as-is in the JSON results.
    """

    class ArbitraryShapeView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return {'foo': 'bar', 'pk': obj.pk}
    q = Question.objects.create(question='Shape')
    request = self.factory.get(self.url, {'term': 'shape', **self.opts})
    request.user = self.superuser
    response = ArbitraryShapeView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0], {'foo': 'bar', 'pk': q.pk})

def test_serialize_result_override_includes_extra_key(self):
    """Overriding serialize_result should include extra keys in results."""

    class CustomView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['extra'] = 'EXTRA-%s' % obj.pk
            return data
    Question.objects.create(question='Question 1')
    request = self.factory.get(self.url, {'term': 'question', **self.opts})
    request.user = self.superuser
    response = CustomView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIn('extra', data['results'][0])
    self.assertEqual(data['results'][0]['extra'], 'EXTRA-%s' % Question.objects.first().pk)

def test_serialize_result_called_for_each_item(self):
    """serialize_result is invoked for every returned object on the page."""
    called = []

    class CountingView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            called.append(obj.pk)
            return super().serialize_result(obj, to_field_name)
    Question.objects.bulk_create((Question(question=f'Q{i}') for i in range(3)))
    request = self.factory.get(self.url, {'term': 'q', **self.opts})
    request.user = self.superuser
    response = CountingView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(set(map(str, called)), set((r['id'] for r in json.loads(response.content.decode('utf-8'))['results'])))

def test_serialize_result_can_return_non_dict(self):
    """serialize_result may return non-dict JSON-serializable values and they appear in 'results'."""

    class StringView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            return 'OBJ-%s' % getattr(obj, to_field_name)
    Question.objects.create(question='Question 1')
    request = self.factory.get(self.url, {'term': 'question', **self.opts})
    request.user = self.superuser
    response = StringView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertTrue(all((isinstance(item, str) for item in data['results'])))
    self.assertIn('OBJ-', data['results'][0])

def test_serialize_result_text_override(self):
    """serialize_result can change the 'text' value emitted in the response."""

    class TextOverrideView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['text'] = 'OVERRIDE-%s' % data['text']
            return data
    Question.objects.create(question='Who am I?')
    request = self.factory.get(self.url, {'term': 'who', **self.opts})
    request.user = self.superuser
    response = TextOverrideView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertTrue(data['results'][0]['text'].startswith('OVERRIDE-'))

def test_serialize_result_respects_to_field_uuid(self):
    """Default serialize_result should use the resolved to_field (UUID) for id when configured."""
    q = Question.objects.create(question='Is this a question?')
    request = self.factory.get(self.url, {'term': 'is', **self.opts, 'field_name': 'question_with_to_field'})
    request.user = self.superuser
    response = AutocompleteJsonView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(data['results'][0]['id'], str(q.uuid))

def test_serialize_result_with_distinct_called_once_per_unique_object(self):
    """When get_search_results requests distinct(), serialize_result is still called once per distinct item."""
    called = []

    class DistinctCountingView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            called.append(obj.pk)
            return super().serialize_result(obj, to_field_name)
    q1 = Question.objects.create(question='q1')
    q2 = Question.objects.create(question='q2')
    q3 = Question.objects.create(question='q3')
    q2.related_questions.add(q1)
    q3.related_questions.add(q1)
    request = self.factory.get(self.url, {'term': 'q', **self.opts})
    request.user = self.superuser

    class DistinctQuestionAdmin(QuestionAdmin):
        search_fields = ['related_questions__question', 'question']
    with model_admin(Question, DistinctQuestionAdmin):
        response = DistinctCountingView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content.decode('utf-8'))
    self.assertEqual(len(called), len(data['results']))

def test_serialize_result_invoked_only_for_page_items(self):
    """serialize_result should only be invoked for items present on the requested page."""
    called = []

    class PageCountingView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            called.append(obj.pk)
            return super().serialize_result(obj, to_field_name)
    total = AutocompleteJsonView.paginate_by + 5
    Question.objects.bulk_create((Question(question=str(i)) for i in range(total)))
    request = self.factory.get(self.url, {'term': '', **self.opts})
    request.user = self.superuser
    response = PageCountingView.as_view(**self.as_view_args)(request)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(called), AutocompleteJsonView.paginate_by)

def test_serialize_result_returns_id_as_string_type(self):
    """The 'id' value returned by default serialize_result is a string."""
    q = Question.objects.create(question='Test typing')
    request = self.factory.get(self.url, {'term': 'test', **self.opts})
    request.user = self.superuser
    response = AutocompleteJsonView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIsInstance(data['results'][0]['id'], str)

def test_serialize_result_can_reference_related_fields(self):
    """Override serialize_result may reference related fields and include them in the output."""

    class RelatedView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['related_count'] = obj.related_questions.count()
            return data
    q1 = Question.objects.create(question='main')
    q2 = Question.objects.create(question='other')
    q2.related_questions.add(q1)
    request = self.factory.get(self.url, {'term': 'main', **self.opts})
    request.user = self.superuser
    response = RelatedView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIn('related_count', data['results'][0])
    self.assertEqual(data['results'][0]['related_count'], 1)

def test_serialize_result_preserves_pagination_structure(self):
    """Even with a custom serialize_result that returns extra data, the pagination metadata is preserved."""

    class ExtraPayloadView(AutocompleteJsonView):

        def serialize_result(self, obj, to_field_name):
            data = super().serialize_result(obj, to_field_name)
            data['extra'] = {'nested': True}
            return data
    Question.objects.bulk_create((Question(question=str(i)) for i in range(5)))
    request = self.factory.get(self.url, {'term': '', **self.opts})
    request.user = self.superuser
    response = ExtraPayloadView.as_view(**self.as_view_args)(request)
    data = json.loads(response.content.decode('utf-8'))
    self.assertIn('pagination', data)
    self.assertIn('more', data['pagination'])
    self.assertIsInstance(data['pagination']['more'], bool)