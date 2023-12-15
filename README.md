The following errors has been encountered and fixed:

1. TypeError: Can't instantiate abstract class Connection with abstract method **exit**

- solution: create an **exit** method in Connection class

2. Connection to database was not handled safely.

- Switched to context manager "with Connection() as connection"

3. Connected to sqlite3 database

4. Getting total hours from employee, required inputting start and end date, but we don't pass dates when making log() command.

5. Code repitiion - getting total hours from employee is twice, switched to using it only once and referring to it later.

6. Added error catchers if there is no hour rate.
