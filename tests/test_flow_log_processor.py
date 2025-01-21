import unittest
import tempfile
import os
from collections import Counter

from flow_log_processor import FlowLogProcessor


class TestFlowLogProcessor(unittest.TestCase):
    def setUp(self):
        # Expected results
        self.expected_tag_counts = {
            "sv_P1": 2,
            "sv_P2": 2,
            "SV_P3": 1,
            "Untagged": 1,
        }
        self.expected_port_protocol_counts = {
            ("25", "tcp"): 1,
            ("443", "tcp"): 1,
            ("68", "udp"): 1,
            ("23", "tcp"): 1,
            ("80", "tcp"): 1,
            ("31", "udp"): 1,
        }


    def test_process_map_file(self):
        map_file_path = "data/sample_map_1.txt"
        processor = FlowLogProcessor(map_file_path)
        self.assertEqual(
            processor._FlowLogProcessor__tag_map,
            {
                ("25", "tcp"): "sv_P1",
                ("68", "udp"): "sv_P2",
                ("23", "tcp"): "sv_P1",
                ("31", "udp"): "SV_P3",
                ("443", "tcp"): "sv_P2",
            },
        )
        print("Passed")

    def test_process_flow_logs(self):
        map_file_path = "data/sample_map_1.txt"
        flow_log_path = "data/sample_fl_1.txt"
        processor = FlowLogProcessor(map_file_path)
        processor.process_flow_logs(flow_log_path)
        self.assertEqual(processor.tag_counts, Counter(self.expected_tag_counts))
        self.assertEqual(
            processor.protocol_port_counts, Counter(self.expected_port_protocol_counts)
        )
        print("Passed")

    def test_write_results(self):
        map_file_path = "data/sample_map_1.txt"
        flow_log_path = "data/sample_fl_1.txt"
        output_file_path = None
        processor = FlowLogProcessor(map_file_path)
        processor.process_flow_logs(flow_log_path)
        output_file_path = tempfile.NamedTemporaryFile(delete=False).name
        processor.write_results(output_file_path)

        with open(output_file_path, "r") as file:
            content = file.read()

        # Verify Tag Counts section
        self.assertIn("Tag Counts:", content)
        for tag, count in self.expected_tag_counts.items():
            self.assertIn(f"{tag:<15}{count:<10}", content)

        # Verify Port/Protocol Combination Counts section
        self.assertIn("Port/Protocol Combination Counts:", content)
        for (port, protocol), count in self.expected_port_protocol_counts.items():
            self.assertIn(f"{port:<10}{protocol:<10}{count:<10}", content)
        print("Passed")


if __name__ == "__main__":
    unittest.main()
