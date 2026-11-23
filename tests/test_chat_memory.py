"""Use local messages and stub models to exercise customer-service memory."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from projects.lingyu_chat.chat_service import ChatService
from projects.lingyu_chat.core.memory import Memory
from projects.lingyu_chat.core.protocol import ChatRequest
from projects.lingyu_chat.core.summary_manager import RECENT_WINDOW, SUMMARY_BATCH_SIZE


class MemoryTests(unittest.TestCase):
    def test_memory_instances_with_the_same_session_id_are_independent(self):
        first = Memory("shared-id")
        first.add_user_message("example message")
        first.update_key_facts({"order": "demo"})
        first.summary.update_summary("example summary")

        second = Memory("shared-id")
        self.assertEqual(second.get_messages(), [])
        self.assertEqual(second.get_key_facts(), {})
        self.assertEqual(second.summary.get_summary(), "")

    def test_summaries_bound_history_without_resummarizing_recent_messages(self):
        memory = Memory("sample")
        with patch.object(memory.summary, "generate_incremental_summary", return_value="summary") as summarize:
            for index in range(SUMMARY_BATCH_SIZE * 2):
                memory.add_user_message(str(index))
                self.assertLess(len(memory.get_messages()), RECENT_WINDOW + SUMMARY_BATCH_SIZE)

        first, second = summarize.call_args_list
        self.assertEqual([message.content for message in first.args[1]], list(map(str, range(SUMMARY_BATCH_SIZE))))
        self.assertEqual(
            [message.content for message in second.args[1]],
            list(map(str, range(SUMMARY_BATCH_SIZE, SUMMARY_BATCH_SIZE * 2))),
        )
        self.assertEqual(len(memory.get_recent_messages(RECENT_WINDOW)), RECENT_WINDOW)
        self.assertEqual([message.content for message in memory.prepare_memory_for_llm()], ["[摘要] summary"])

    def test_service_isolates_users_and_evicts_least_recently_used_sessions(self):
        with (
            patch("projects.lingyu_chat.chat_service.ChatTongyi"),
            patch("projects.lingyu_chat.chat_service.IntentRecognizer") as recognizer,
        ):
            recognize = recognizer.return_value.recognize
            recognize.return_value = SimpleNamespace(confidence=0.0)
            service = ChatService(api_key="offline-test", max_sessions=2)

        def send(user, session, message):
            service.handle(ChatRequest("offline-test", user, session, message, "trace"))
            return recognize.call_args.args[1]

        self.assertEqual(send("first", "shared", "first message"), "")
        self.assertEqual(send("second", "shared", "second message"), "")
        self.assertIn("first message", send("first", "shared", "follow-up"))
        send("first", "another", "another session")
        self.assertEqual(send("second", "shared", "evicted session"), "")
