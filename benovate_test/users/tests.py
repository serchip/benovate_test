from django.test import TestCase
from django.contrib.auth import get_user_model

from shippets.test_case import TestCaseApiMixin

UserModel = get_user_model()


class BalanceTestCase(TestCaseApiMixin, TestCase):

    def setUp(self):
        UserModel.objects.create_user(username='test1', password='test1', INN=1, balance=100)
        UserModel.objects.create_user(username='test2', password='test2', INN=2, balance=200)
        UserModel.objects.create_user(username='test3', password='test3', INN=3, balance=300)
        UserModel.objects.create_user(username='test4', password='test4', INN=4, balance=400)

    def test_transfer_all_null(self):
        data = {
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors'], {
                                                      "dec_sum": [
                                                          "This field is required."
                                                      ],
                                                      "user_from": [
                                                          "This field is required."
                                                      ],
                                                      "users_to": [
                                                          "This field is required."
                                                      ]
                                                  })

    def test_transfer_user_from_null(self):
        data = {
            'user_from': 'not int'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['user_from'], ["'not int' value must be an integer."])

        data = {
            'user_from': '1212',
            'users_to': [1,2],
            'dec_sum': '1.1'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['non_field_errors'],
                         ['Укажите активного пользователя от которого перевод.'])

        data = {
            'user_from': '1',
            'users_to': [4, 2],
            'dec_sum': '1.1'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'Успешное сохранение!')

    def test_transfer_user_to_null(self):
        data = {
            'user_from': '1',
            'dec_sum': '1.1'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['users_to'], ["This field is required."])
        data = {
            'user_from': '1',
            'users_to': 'not list',
            'dec_sum': '1.1'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['users_to'], ["Expected a list of items but got type \"str\"."])
        data = {
            'user_from': '1',
            'users_to': [],
            'dec_sum': '1.1'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['non_field_errors'],
                         ['Выберите хотя бы одного пользователя которому перевод.'])
        data = {
            'user_from': '1',
            'users_to': [1, 2],
            'dec_sum': '1.1'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['non_field_errors'],
                         ['Укажите активных пользователей на которых будет перевод.'])
        data = {
            'user_from': '1',
            'users_to': [3, 2],
            'dec_sum': '1.1'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'Успешное сохранение!')

    def test_transfer_dec_sum_null(self):
        data = {
            'user_from': '1',
            'users_to': [3, 2],
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['dec_sum'], ["This field is required."])
        data = {
            'user_from': '1',
            'users_to': [3, 2],
            'dec_sum': ''
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['dec_sum'], ["A valid number is required."])
        data = {
            'user_from': '1',
            'users_to': [3, 2],
            'dec_sum': '111111'
        }
        response = self.post('balance:transfer', data=data)
        self.assertResponseCode(response, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['errors']['non_field_errors'],
                         ["Указанная сумма привышает допустимое значение ( 100.00 )"])
