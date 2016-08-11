# gradient-descent

This Python utility provides implementations of both [Linear](http://en.wikipedia.org/wiki/Linear_regression) and 
[Logistic Regression](http://en.wikipedia.org/wiki/Logistic_regression) using 
[Gradient Descent](http://en.wikipedia.org/wiki/Gradient_descent), these algorithms are commonly used in Machine Learning.

The utility analyses a set of data that you supply, known as the _training set_, which consists of multiple data items or 
_training examples_. Each training example must contain one or more input values, and one output value. The utility attempts 
to derive an equation (called the _hypothesis_) which defines the relationship between the input values and the output value. 
The hypothesis can then be used to predict what the output will be for new inputs, that were not part of the original training set.

For example, if you are interested in predicting house prices you might compile a training set using data from past property sales, 
using the selling price as the output value, and various attributes of the houses such as number of rooms, 
area, number of floors etc. as the input values.

### Training Data File Format

To use the utility with a training set, the data must be saved in a correctly formatted text file, with each line in the file 
containing the data for a single training example. A line must begin with the output value followed by a ':', the remainder 
of the line should consist of a comma-separated list of the input values for that training example. The number of input values 
must be the same for each line in the file - any lines containing more/fewer input values than the first line will be rejected. 
Lines beginning with a '#' symbol will be treated as comments and ignored.

An extract from the House Prices data file might look like this:

<pre>
# House Price Data
# line format is: &lt;price&gt;:&lt;room count&gt;,&lt;number of floors&gt;,&lt;area&gt;
235000:9,2,112
125500:4,1,90
400000:12,2,190
</pre>

### Helper Configuration

As well as supplying a training set, you will need to write a few lines of Python code to configure how the utility will run. 
It is recommended that you use the `Helper` class to do this, which will simplify the use of the utility by handling 
the wiring and instantiation of the other classes, and by providing reasonable defaults for many of the required configuration parameters.  

The Helper class has many configuration options, which are documented below. A simple invocation might look something like this:

<pre>
Helper('house_price_data.txt') \
    .with_linear_regression() \
    .with_alpha(0.1) \
    .with_iterations(30000) \
    .with_linear_terms() \
    .go()
</pre>

The Helper is configured using the following methods:

#### with_iterations

An integer value, defaulting to 1000. This determines the number of iterations of Gradient Descent that will be performed before the 
calculated hypothesis is displayed. Higher values will yield more accurate results, but will increase the required running time.

#### with_alpha

A numeric value, defaulting to 1. This method sets the _learning rate_ parameter used by Gradient Descent when updating the hypothesis 
after each iteration. Up to a point, higher values will cause the algorithm to converge on the optimal solution more quickly, however if 
the value is set too high then it will fail to converge at all, yielding successively larger errors on each iteration. Finding a good 
learning rate value is largely a matter of experimentation - enabling error checking, as detailed below, can assist with this process.

#### with_error_checking

A boolean value, defaulting to False. When set to True the utility will check the hypothesis error after each iteration, and abort if 
the error has increased. Setting this can be useful when attempting to determine a reasonable learning rate value for a new data set, 
however once this has been done error checking should be disabled in order to increase processing speed.

#### with_term

Adds a single term to the hypothesis. This method requires a string value (the name that will be used to refer to the new term) and a 
function object accepting a single parameter, which will be a list containing all the input values for a single training example. 
This method should be used to add custom, non-linear terms to the hypothesis:

<pre>
.with_term('w^2',    lambda l: l[0] * l[0])         # Square of the first input value
.with_term('log(n)', lambda l: math.log(l[3], 10))  # Logarithm (base 10) of the 4th input value
.with_term('a*b*c',  lambda l: l[0] * l[1] * l[2])  # Product of the first 3 input values
</pre>

#### with_linear_terms

Adds a series of linear terms to the hypothesis, one for each of the input parameters in the training set. The terms will be named 
automatically, 'x1' for the first input parameter, 'x2' for the second and so on.

#### with_regularisation_coefficient

An integer value, defaulting to '0'. Setting a non-zero regularisation coefficient will have the effect of producing a smoother, more 
general hypothesis, less prone to overfitting - as a consequence the hypothesis will yield larger errors on the training 
set, but may provide a better fit for new data.

#### with_linear_regression

Makes the utility use Linear Regression to derive the hypothesis

#### with_logistic_regression

Makes the utility use Logistic Regression to derive the hypothesis. Note that when using Logistic Regression the output values in the 
training set must be either '0' or '1'.

#### with_normalisation

A boolean value, defaulting to True. When normalisation is enabled, the utility will perform Feature Scaling and Mean Normalisation 
on the input data.

#### with_test_on_completion

Makes the utility run the final hypothesis against the training data after calculation has been completed. The displayed results 
should give a clear indication of how good the hypothesis is.

### Example: Linear Regression

Here the utility is used to derive an equation for calculating the Apparent Magnitude of a star from its Absolute Magnitude and its Distance. This is a slightly atypical application of machine learning because these quantities are already known to be related by a [mathematical formula](http://www.astro.cornell.edu/academics/courses/astro201/mag_absolute.htm), however it should serve as a useful test to prove that the utility is working correctly.

The training set contains approximately 1000 examples extracted from the [HYG Database](http://www.astronexus.com/hyg). The input data is contained in a text file called `star_data.txt` a sample from the file is shown below:  

<pre>
...
9.1:219.7802,2.39
9.27:47.9616,5.866
6.61:442.4779,-1.619
...
</pre>

The utility is executed using the command shown below. Note that in the names for the various terms, the letter 'D' has been used to represent the Distance value (the first input value) and 'M' represents the Absolute Magnitude (the second input value). In this example we have speculatively added a number of custom terms using M and D both individually and in combination with each other. Each of these terms may or may not be involved in the actual relationship between the inputs and the output - the utility will determine which of them are actually useful, and to what extent, as part of its processing.

<pre>
Helper('star_data.txt') \
    .with_linear_regression() \
    .with_alpha(1) \
    .with_iterations(30000) \
    .with_term('M',      lambda l : l[1]) \
    .with_term('M^2',    lambda l : l[1] * l[1]) \
    .with_term('D',      lambda l : l[0]) \
    .with_term('D^2',    lambda l : l[0] * l[0]) \
    .with_term('D*M',    lambda l : l[0] * l[1]) \
    .with_term('log(D)', lambda l : math.log(l[0], 10)) \
    .go()
</pre>

After 30,000 iterations the following hypothesis has been calculated:

<pre>
-------------------------------
Theta values:
-------------
      x0 =      -4.99921928
       D =       0.00000083
     D^2 =      -0.00000000
       M =       1.00003066
  log(D) =       4.99956287
     M^2 =      -0.00000644
     D*M =      -0.00000000

Completed 30000 iterations
-------------------------------
</pre>

The numbers shown against each of the terms are their coefficients in the resulting hypothesis equation. Notice that in addition to the 6 terms we added to the Helper, there is also a 7th term called 'x0'. This term is automatically added to the hypothesis by the utility, and is simply a constant term that does not depend on any of the input values.
This output can be interpreted to mean that the best hypothesis found by the utility (i.e. the best way to find the output from the inputs) is by using the equation:

<pre>
    output = -4.99921928 + (D * 0.00000083) + (-0.00000000 * D^2) + (1.00003066 * M) + (4.99956287 * log(D)) + (-0.00000644 * M^2) + (-0.00000000 * D * M)
</pre>

However four of these coefficients are very close to zero, so it is safe to assume these terms have little influence on the output value, and we can remove them:

<pre>
    output = -4.99921928 + (1.00003066 * M) + (4.99956287 * log(D))
</pre>

Each of the remaining coefficients are close to an integer value, so we can further simplify the equation by rounding them as follows: 

<pre>
    output = -5 + M + 5 * log(D)
</pre>

This equation matches [the one used by astronomers](http://www.astro.cornell.edu/academics/courses/astro201/mag_absolute.htm) to calculate magnitude values.
