from collections import Counter

import sys


class FlowLogProcessor:
    def __init__(self, map_file: str):
        """
        Class that processes the Flow Log with the help of the map file.
        Provides the utilities that help in categorizing the flow logs
        with their respective tags.

        :param map_file: path to the map file
        """
        # {(port, protocol): tag}
        self.__tag_map = {}
        self.__process_map_file(map_file)
        self.tag_counts = Counter()
        self.protocol_port_counts = Counter()


    def __process_map_file(self, map_file_path):
        header_indexes = None
        with open(map_file_path, "r") as file:
            for line in file:
                if header_indexes is None:
                    header_indexes = self.__get_headers(line, delimiter=',')
                else:
                    record = line.strip().split(",")
                    dstport = self.__get_value(header_indexes, record, "dstport")
                    proto = self.__get_value(header_indexes, record, "protocol")
                    tag = self.__get_value(header_indexes, record, "tag")
                    self.__tag_map[(dstport.lower(), proto.lower())] = tag


    @staticmethod
    def __get_headers(line: str, delimiter:str=' ') -> dict[str, int]:
        header_indexes = {}
        headers = line.strip().split(delimiter)
        index = 0
        for header in headers:
            header_indexes[header] = index
            index += 1
        return header_indexes


    def process_flow_logs(self, file_path: str):
        # Resetting header indexes, to handle a new file
        if not self.__tag_map:
            raise ValueError("Tag map is not valid")
        header_indexes = None
        with open(file_path, "r") as file:
            for line in file:
                if header_indexes is None:
                    header_indexes = self.__get_headers(line)
                    if "version" not in header_indexes:
                        raise ValueError("Invalid header in the Flow Log file")
                else:
                    record = line.strip().split()
                    self.__process_flow_log(header_indexes, record)


    @staticmethod
    def __get_value(header_indexes, record, header_name):
        try:
            header_index = header_indexes[header_name]
        except KeyError:
            raise ValueError(f"Header {header_name} is not present in the headers")
        return record[header_index]


    def __process_flow_log(self, header_indexes, record):
        # parse each line in flow log
        # a function will take the line and return the tag
        dstport = self.__get_value(header_indexes, record, 'dstport')
        protocol = self.__get_value(header_indexes, record, 'protocol')
        tag = self.__tag_map.get((dstport, protocol), "Untagged")
        # hashmap should contain the keys representing tag and value as count per tag
        self.tag_counts[tag] += 1
        # hashmap should contain the keys representing port and protocol, and value as count
        self.protocol_port_counts[(dstport, protocol)] += 1

    def write_results(self, output_file: str):
        with open(output_file, "w") as file:
            file.write("Tag Counts:\n")
            file.write(f"{'Tag':<15}{'Count':<10}\n")
            for tag, count in self.tag_counts.items():
                file.write(f"{tag:<15}{count:<10}\n")
            file.write("\nPort/Protocol Combination Counts:\n")
            file.write(f"{'Port':<10}{'Protocol':<10}{'Count':<10}\n")
            for (port, protocol), count in self.protocol_port_counts.items():
                file.write(f"{port:<10}{protocol:<10}{count:<10}\n")


def main():
    """
    Main method for FlowLogProcessor.
    Accepts file paths for the map file, flow log file, and output file via console input.
    """
    if len(sys.argv) != 4:
        print("Usage: python flow_log_processor.py <map_file> <flow_log_file> <output_file>")
        sys.exit(1)

    map_file = sys.argv[1]
    flow_log_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        # Create an instance of FlowLogProcessor
        processor = FlowLogProcessor(map_file)

        # Process the flow log file
        processor.process_flow_logs(flow_log_file)

        # Write the results to the output file
        processor.write_results(output_file)

        print(f"Processing complete. Results written to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
