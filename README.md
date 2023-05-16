# Schedule-optimization
Schedule-Optimization

Overview:

This project is an implementation of an optimization algorithm for scheduling the production of high-frequency spindles (HFSP) in a manufacturing plant. The algorithm is based on a genetic algorithm approach and is designed to minimize the production time and maximize machine utilization.
Usage

To use the HFSP scheduling algorithm, follow these steps:

   1-Prepare an Excel file sheet named 'example' in the standard format.
   2-Run the tScheduling.py script and provide the path to your Excel file as an input.
   3-The algorithm will output a weekly schedule in the form of a Gantt chart, which can be easily interpreted and used for decision-making.

Algorithm Description:

The algorithm is based on a coding method that arranges the work-pieces in a sequential queue, with the position of the work-pieces indicating the processing sequence of the first process. The subsequent stage is coded in non-descending order according to the processing completion time of work-pieces in the previous stage. The algorithm consists of three steps:

First Step:

For each operation of each work-piece, the algorithm calculates the start time, completion time, processing time, and current machine load for all available machines. The start time is calculated by comparing the completion time of the last operation of the work-piece with the completion time of the last operation processed by the machine. If there is a gap between the two times and the gap is greater than the processing time of the process, the process can be inserted into the gap, and the start time is the end time of the previous process in the gap. If the completion time of the last operation of the work-piece is greater than the completion time of the last operation processed by the machine, the start time is the completion time of the last operation of the work-piece.

Second Step:

The algorithm selects the machine for each operation based on the optimization principle of giving priority to the machine with the least completion time. If the completion times are the same, the algorithm selects the machine with the lowest current load. If the machine loads are also the same, the algorithm selects the machine at random.

Third Step

The algorithm checks whether all processes of all work-pieces have been machine selected. If all processes have been selected, the scheduling scheme is output. Otherwise, the algorithm returns to the first step and repeats the process.

Credits

This project is based on the work presented in the following site: https://programmer.group/613db68ec2dec.html. We developed a genetic algorithm for solving the HFSP problem. Our implementation follows the coding method based on work-piece arrangement, as described in the original work.

We hope that our implementation of the algorithm will be helpful in optimizing production schedules for manufacturing plants.
