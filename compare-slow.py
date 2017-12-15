# Compare-slow.py is a tool to compare slow queries from the database week over week
# Authored by Carly Fujiyoshi and Gabriel Abinante

import json
import sys
from prettytable import PrettyTable, ALL

# Define our arrays for comparison
lastWeek = []
thisWeek = []
thisWeekFull = []
finalResults = []

# Grab json files from input args
with open(sys.argv[1], 'r') as f:
  data = f.read()
  parsed_json = json.loads(data)

def format_fingerprint(fingerprint_to_format, max_line_length):
  # Accumulated line length
  ACC_length = 0
  words = fingerprint_to_format.split(" ")
  formatted_fingerprint = ""
  for word in words:
      # If ACC_length + len(word) and a space is <= max_line_length
      if ACC_length + (len(word) + 1) <= max_line_length:
          # Append the word and a space
          formatted_fingerprint = formatted_fingerprint + word + " "
          # Length = length + length of word + length of space
          ACC_length = ACC_length + len(word) + 1
      else:
          # Append a line break, then the word and a space
          formatted_fingerprint = formatted_fingerprint + "\n" + word + " "
          # Reset counter of length to the length of a word and a space
          ACC_length = len(word) + 1
  return formatted_fingerprint

for each in parsed_json:
    item = []
    new_fingerprint = format_fingerprint(each['fingerprint'],70)
    item.append(new_fingerprint)
    item.append(each['metrics']['avg'])
    item.append(each['metrics']['sum'])
    thisWeekFull.append(item)

for each in parsed_json:
    fingerprints = []
    fingerprints.append(each['fingerprint'])
    thisWeek.append(fingerprints)

# Put all of this week's junk in another array
with open(sys.argv[2]) as f:
  data = f.read()
  parsed_json = json.loads(data)
  for each in parsed_json:
      fingerprints1 = []
      fingerprints1.append(each['fingerprint'])
      lastWeek.append(fingerprints1)

# Compare array
removed = 0
for x in thisWeek:
  if x in lastWeek:
    removed += 1
    thisWeek.remove(x)

for each in thisWeekFull:
  for fp in thisWeek:
    fp_formatted = format_fingerprint(fp[0], 70)
    if fp_formatted == each[0]:
        finalResults.append(each)
# Build table
table = PrettyTable(['Query Text', 'Average Execution Time', 'Total Execution Time'])
table.hrules = ALL
for each in finalResults:
  table.add_row([each[0], each[1], each[2]])

# Output table to file
output = open("Output.txt", "w")
output.write(str(table))
output.close()
