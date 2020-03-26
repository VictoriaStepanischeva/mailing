from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mailing.apps.emessages.tests.mixins import SetUpEmessageMixin
from mailing.apps.users.tests.mixins import SetUpUserMixin
from mailing.apps.emessages.models import Recipient


class EmessageInboxTestCase(SetUpEmessageMixin, SetUpUserMixin, APITestCase):
    """Class for testing operations with inbox messages."""

    def setUp(self):
        self.url = reverse('inbox-list')
        self.jwt_url = reverse('token_obtain_pair')
        self.sender = self._create_user(
            email='test@test.test', password='111', is_active=True)
        self.first_recipient = self._create_user(
            email='recipient@1.com', password='222', is_active=True)
        self.second_recipient = self._create_user(
            email='recipient@2.com', password='333', is_active=True)
        self.recipients = [
            self.sender,
            self.first_recipient,
            self.second_recipient
        ]
        self.emessage = self._create_emessage(sender=self.sender)
        self.emessage.recipients.add(self.sender)
        self.emessage.recipients.add(self.first_recipient)
        self.emessage.recipients.add(self.second_recipient)

    def testFetchListAnonymous(self):
        """Checks getting API by AnonymousUser."""
        r = self.client.get(self.url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, r.status_code)

    def testFetchListInboxMessages(self):
        """Checks data in inbox message."""
        self.client.force_authenticate(user=self.sender)
        r = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

        expected_data = {
            'id': self.emessage.pk,
            'sender': self.sender.pk,
            'recipients': [recipient.pk for recipient in self.recipients],
            'text_message': None,
            'has_read': False,
        }
        self.assertEqual(len(r.data['results']), 1)
        self.assertEqual(dict(r.data['results'][0]), expected_data)

    def testFetchListSeveralInboxMessages(self):
        """Checks list of user inbox messages."""
        # creating another message for self.sender
        another_emessage = self._create_emessage(sender=self.first_recipient)
        another_emessage.recipients.add(self.sender)
        self.client.force_authenticate(user=self.sender)
        r = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)
        self.assertEqual(len(r.data['results']), 2)

    def testFetchInboxMessage(self):
        """Checks fetching specific inbox message."""
        url = reverse('inbox-detail', kwargs={'pk': self.emessage.pk})
        self.client.force_authenticate(user=self.sender)
        r = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

        expected_data = {
            'id': self.emessage.pk,
            'sender': self.sender.pk,
            'recipients': [recipient.pk for recipient in self.recipients],
            'text_message': None,
            'has_read': False,
        }
        self.assertEqual(r.data, expected_data)

    def testDeleteInboxMessage(self):
        """Checks marking inbox message as is_deleted for recipient."""
        url = reverse('inbox-detail', kwargs={'pk': self.emessage.pk})
        self.client.force_authenticate(user=self.sender)
        r = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, r.status_code)

        recipient = Recipient.objects.filter(
            emessage=self.emessage, user=self.sender).first()
        self.assertTrue(recipient.is_deleted)

    def testReadInboxMessage(self):
        """Checks marking inbox message as has_read."""
        url = reverse('inbox-read', kwargs={'pk': self.emessage.pk})
        self.client.force_authenticate(user=self.sender)
        r = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

        self.assertTrue(r.data['has_read'])

    def testUnReadInboxMessage(self):
        """Checks marking inbox message as unread."""
        url = reverse('inbox-unread', kwargs={'pk': self.emessage.pk})
        self.client.force_authenticate(user=self.sender)
        r = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

        self.assertFalse(r.data['has_read'])


class EmessageSentTestCase(SetUpEmessageMixin, SetUpUserMixin, APITestCase):
    """Class for testing operations with sent messages."""

    def setUp(self):
        self.url = reverse('sent-list')
        self.sender = self._create_user(
            email='test@test.test', password='111', is_active=True)
        self.first_recipient = self._create_user(
            email='recipient@1.com', password='222', is_active=True)
        self.second_recipient = self._create_user(
            email='recipient@2.com', password='333', is_active=True)
        self.recipients = [
            self.first_recipient,
            self.second_recipient
        ]
        self.emessage = self._create_emessage(sender=self.sender)
        self.emessage.recipients.add(self.first_recipient)
        self.emessage.recipients.add(self.second_recipient)

    def testFetchListAnonymous(self):
        """Checks getting API by AnonymousUser."""
        r = self.client.get(self.url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, r.status_code)

    def testFetchListSentMessages(self):
        """Checks data in sent message."""
        self.client.force_authenticate(user=self.sender)
        r = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

        expected_data = {
            'id': self.emessage.pk,
            'sender': self.sender.pk,
            'recipients': [recipient.pk for recipient in self.recipients],
            'text_message': None,
            'has_read': False,
        }
        self.assertEqual(len(r.data['results']), 1)
        self.assertEqual(dict(r.data['results'][0]), expected_data)

    def testFetchListSeveralSentMessages(self):
        """Checks list of user inbox messages."""
        # creating another message from self.sender
        another_emessage = self._create_emessage(sender=self.sender)
        another_emessage.recipients.add(self.first_recipient)
        self.client.force_authenticate(user=self.sender)
        r = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)
        self.assertEqual(len(r.data['results']), 2)

    def testFetchSentMessage(self):
        """Checks fetching specific sent message."""
        url = reverse('sent-detail', kwargs={'pk': self.emessage.pk})
        self.client.force_authenticate(user=self.sender)
        r = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

        expected_data = {
            'id': self.emessage.pk,
            'sender': self.sender.pk,
            'recipients': [recipient.pk for recipient in self.recipients],
            'text_message': None,
            'has_read': False,
        }
        self.assertEqual(r.data, expected_data)

    def testDeleteSentMessage(self):
        """Checks marking sent message as is_deleted for sender."""
        url = reverse('sent-detail', kwargs={'pk': self.emessage.pk})
        self.client.force_authenticate(user=self.sender)
        r = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, r.status_code)

        self.emessage.refresh_from_db()
        self.assertTrue(self.emessage.is_deleted)


class EmessageCreateTestCase(SetUpEmessageMixin, SetUpUserMixin, APITestCase):
    """Class for testing creation of emessage."""

    def setUp(self):
        self.url = reverse('emessage-create')
        self.sender = self._create_user(
            email='test@test.test', password='111', is_active=True)
        self.first_recipient = self._create_user(
            email='recipient@1.com', password='222', is_active=True)
        self.second_recipient = self._create_user(
            email='recipient@2.com', password='333', is_active=True)

    def testFetchListAnonymous(self):
        """Checks posting by AnonymousUser."""
        r = self.client.post(self.url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, r.status_code)

    def testPostNeWEmessage(self):
        """Checks creating emessage."""
        text_message = "Test ping"
        post_data = {
            'recipients': [self.first_recipient.pk],
            'text_message': text_message,
        }

        self.client.force_authenticate(user=self.sender)
        r = self.client.post(self.url, data=post_data)
        self.assertEquals(status.HTTP_201_CREATED, r.status_code)

        self.assertTupleEqual(
            (r.data['sender'], r.data['recipients'], r.data['text_message']),
            (self.sender.pk, [self.first_recipient.pk], text_message)
        )

    def testPostNewmessageWithoutRecipients(self):
        """Checks creaing emessage without recipients."""
        text_message = "Test ping"
        post_data = {
            'recipients': [],
            'text_message': text_message,
        }

        self.client.force_authenticate(user=self.sender)
        r = self.client.post(self.url, data=post_data)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, r.status_code)

