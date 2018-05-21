# Computational topology - group project:  Sensors

You are given a number of points on the sphere of radius 1.  You should view them as sensors
on the surface of the Earth.  The sensors are used to gather data and form a sensor network
with parameters _r_ and _R_:

 - each sensor gathers data from the surrounding area in the shape of a circle of radius _R_,
 - each sensor can communicate with other sensors which are at most _r_ away.

### Project goal
Determine _r_ and _R_, so that
1.  numbers _r_ and _R_ are as small as possible (that would decrease the cost of sensors),
2.  the sensor network is connected (i.e.  the Vietoris-Rips graph is connected),
3.  the sensor network covers the whole sphere (the Čech complex should be homotopy equivalent to the sphere, i.e.  the Euler characteristic of the Čech complex should be
that of a sphere).

Furthermore, once the parameters _r_ and _R_ are established, the program should return a list
of obsolete sensors, i.e.  sensors, whose removal would not change the desired properties 2.
and 3.  of the sensor network.


### Data
The input data is a set of points on the sphere of radius 1.


### Results
The result should be required parameter values _r_ and _R_.  Start with an estimatefor _r_ and _R_ and keep optimizing the values.
To generate the Čech complex you can use the MiniBall algorithm.

### Data generator

You should also produce a distribution of 50 points on the sphere with parameters _r_ and _R_ as small as possible.
