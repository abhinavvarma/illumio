# Flow Log Processor

A utility to parse Flow Log files and using a map, assigns tags based on dstport and protocol

## Assumptions
1. Assuming that the Flow Log files are delimited by space
2. Assuming that the protocol field in Flow Log file matches with the protocol field in map file.
3. Assuming headers will be present for both flow log file and map file, however order of the columns can vary.
4. Assuming dstport, protocol headers are present in both files.


## Run

Usage: 
```commandline
python flow_log_processor.py <map_file> <flow_log_file> <output_file>
```
