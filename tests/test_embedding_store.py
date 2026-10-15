import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import httpx
from openai import BadRequestError

from mm import EmbeddingStore


class TestCase(unittest.TestCase):

    @staticmethod
    def get_token_limit_error():
        return BadRequestError(
            "Request exceeds token limit",
            response=httpx.Response(
                400,
                request=httpx.Request(
                    "POST", "https://api.openai.com/v1/embeddings"
                ),
            ),
            body={"code": "max_tokens_per_request"},
        )

    @patch.object(EmbeddingStore, "MAX_TOKENS_PER_REQUEST", 5)
    @patch("mm.ai.EmbeddingStore.tiktoken.encoding_for_model")
    @patch("mm.ai.EmbeddingStore.client.embeddings.create")
    def test_embedding_batches_respect_token_limit(
        self, create_embedding, encoding_for_model
    ):
        encoding = MagicMock()
        encoding.encode.side_effect = lambda text, **_: text.split()
        encoding_for_model.return_value = encoding
        create_embedding.side_effect = [
            SimpleNamespace(
                data=[
                    SimpleNamespace(embedding=[3.0, 4.0]),
                    SimpleNamespace(embedding=[0.0, 2.0]),
                ]
            ),
            SimpleNamespace(
                data=[SimpleNamespace(embedding=[5.0, 12.0])]
            ),
        ]

        matrix = EmbeddingStore.__get_embedding_matrix__(
            ["one two", "three four five", "six seven eight"]
        )

        self.assertEqual(create_embedding.call_count, 2)
        self.assertEqual(
            create_embedding.call_args_list[0].kwargs["input"],
            ["one two", "three four five"],
        )
        self.assertEqual(
            create_embedding.call_args_list[1].kwargs["input"],
            ["six seven eight"],
        )
        expected = [[0.6, 0.8], [0.0, 1.0], [5 / 13, 12 / 13]]
        for actual_row, expected_row in zip(matrix, expected):
            for actual, expected_value in zip(actual_row, expected_row):
                self.assertAlmostEqual(actual, expected_value)

    @patch("mm.ai.EmbeddingStore.tiktoken.encoding_for_model")
    @patch("mm.ai.EmbeddingStore.client.embeddings.create")
    def test_embedding_retries_server_token_limit(
        self, create_embedding, encoding_for_model
    ):
        encoding = MagicMock()
        encoding.encode.side_effect = lambda text, **_: text.split()
        encoding_for_model.return_value = encoding
        create_embedding.side_effect = [
            self.get_token_limit_error(),
            SimpleNamespace(
                data=[SimpleNamespace(embedding=[3.0, 4.0])]
            ),
            SimpleNamespace(
                data=[SimpleNamespace(embedding=[5.0, 12.0])]
            ),
        ]

        matrix = EmbeddingStore.__get_embedding_matrix__(
            ["one two", "three four"]
        )

        self.assertEqual(create_embedding.call_count, 3)
        self.assertEqual(
            create_embedding.call_args_list[1].kwargs["input"], ["one two"]
        )
        self.assertEqual(
            create_embedding.call_args_list[2].kwargs["input"],
            ["three four"],
        )
        self.assertAlmostEqual(matrix[0][0], 0.6)
        self.assertAlmostEqual(matrix[1][0], 5 / 13)

    def test_embedding(self):
        key_to_text = {
            "A1": "I am Nuwan.",
            "A2": "Nuwan is me.",
            "B": "The price of cheese is high.",
        }
        embedding_store = EmbeddingStore(
            emb_id="test_embedding_store", key_to_text=key_to_text
        )
        m = embedding_store.embedding_matrix

        self.assertEqual(len(m), 3)
        self.assertEqual(len(m[0]), 1536)
        self.assertAlmostEqual(m[0][0], -0.026, places=3)
