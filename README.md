# Rule Engine
Computes a result by applying boolean logic equations up multiple columns of tabular data

##### Behavior
Please refer to the configuration of the spare-parts main module to see how this module is used.

##### Example
Assume a workshop message analysis based on three types of message codes. The analyis applies a 
sliding rolling mean on each of them. This is acchieved by pluging the rolling_mean metric into the spare-parts 
main app. 
We will derive an alarm state by combining this three results. To do the main application also plugs in the rule engine 
into its model pipeline right after the rolling-mean calculations. 

It's input are the three output columns names of the rolling_mean columns with a threshold (or upper and lower boundaries) for each of them.

The output is another column appended to the dataframe. It can be interpreted as an alarm / anomaly.


