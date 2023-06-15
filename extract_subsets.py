import csv
import math

### EDIT BELOW
input_file_path = 'movies.csv'
max_rows_per_file = 100
### STOP

def divide_csv(input_file, max_rows_per_file):
    with open(input_file, 'r') as input_csv:
        reader = csv.reader(input_csv)
        header = next(reader)  # read and store the header row
        
        # get the total row count and calculate the number of files needed
        row_count = sum(1 for _ in reader)
        file_count = math.ceil(row_count / max_rows_per_file)
        
        input_csv.seek(0)  # reset the file pointer to the beginning of the file
        next(reader)  # skip the header row for further processing
        
        for file_index in range(file_count):
            subset_rows = [header]  # initialize the subset rows with the header row
            
            # read the rows for the current subset
            for _ in range(max_rows_per_file):
                try:
                    subset_rows.append(next(reader))
                except StopIteration:
                    break
            
            subset_filename = f"subset_{file_index+1}.csv"
            
            with open(subset_filename, 'w', newline='') as subset_csv:
                writer = csv.writer(subset_csv)
                writer.writerows(subset_rows)  # write subset rows to the subset CSV file
                
            print(f"Subset {file_index+1} created: {subset_filename}")

divide_csv(input_file_path, max_rows_per_file)
