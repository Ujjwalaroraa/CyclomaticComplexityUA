# CyclomaticComplexityUA

Name: Ujjwal Arora

Student id :17311879

email id : arorau@tcd.ie

Dependencies: Python 2.7

The cyclomatic complexity gives a measure of the number of decision points in the program. Decision points are those from where the task execution can proceed in different directions.

It is a software metric which is used to measure the complexity of the source code. It measures the number of independent paths in a program.

I have explained cyclomatic complexity with the help of the Master Slave Program. In this, I have explained the effciency of work done when the number of slaves increases. As the number of slaves increase, the efficiency increases, similarly when we increase the nodes in the program, then the efficiency increases.

Steps included in the programs:

Masters side:

1.Master issues Workers with commit SHA's for a given repository and accepts the average CC of a commit from Worker.

2.Issues newly instantiated Workers with a URL to access commits.

3.Retrieves SHA's for every commit in my Internet Apps Chat Server repository.

4.Calculate and print the average cyclomatic complexity for the repository.


Slave side:

1.A Slave calculates the average CycComp for a given commit in a Github repository.

2.The Master issues each Slave with a repo URL upon instantiation, and a

3.commit SHA each time it asks for work. The Slave performs CC analysis on every file in the given commit and returns the average value to the Master.

4.The Slave asks for work forever until the list of commits has been exhausted.
