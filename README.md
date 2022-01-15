# Bingo - PR & SPC - back end module

Exam project for "Programming" university course @ UniCampus Rome - Developed by Paolo Ruggirello & Simone Pio Caronia.
The back end module is developed in python using a framework called flask.

### All modules:
Bingo-core: https://github.com/PaoloRuggirello/bingo-core \
Bingo-BE: https://github.com/PaoloRuggirello/bingo-be \
Bingo-FE: https://github.com/spioc999/bingo_fe


### Building and run the project
You can find building and install instructions inside bingo-core>README.md file.

### Project Structure
The back end module is composed of 5 packages:
- controller: Contains endpoints called by fe module to perform operations
- dto: Contains Data transfer Objects used to communicate info between front end and back end
- helper: Contains methods useful for endpoints 
- lib_dist: Contains the last build of the bingo-core module
- repository: Contains methods that perform operation on db