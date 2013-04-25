Augmented Trader
===============

Independent Python Project on Computational Investment

<ul>Main Functions
<li>Portfolio Optimization based on Yahoo Data Feed</li>
<li>Event Profiling</li>
<li>Automated order generation based on historical event feeds</li>
<li>Market Simulation with key performance parameters for portfolio (volitility, sharpe ratio, etc.)</li>
<li>Rolling statstics and Bollinger-band quantification</li>
</ul>

keywords: time-series | technical analysis | back-testing | numpy | pandas DF | QSTK | rolling statistics |

<h3>Sample Output and Demo</h3>

<div>Portfolio Optimizer</div>
<pre>
Start Date: January 1, 2011
End Date: December 31, 2011
Symbols: ['AAPL', 'GLD', 'GOOG', 'XOM']
Optimal Allocations: [0.4, 0.4, 0.0, 0.2]
Sharpe Ratio: 1.02828403099
Volatility (stdev of daily returns):  0.0101467067654
Average Daily Return:  0.000657261102001
Cumulative Return:  1.16487261965
</pre>

<div>Market Simulator</div>
<pre>
The final value of the portfolio using the sample file is -- 2011,12,20,1133860

Details of the Performance of the portfolio :

Data Range :  2011-01-10 16:00:00  to  2011-12-20 16:00:00

Sharpe Ratio of Fund : 1.21540462111
Sharpe Ratio of $SPX : 0.0183391412227

Total Return of Fund :  1.13386
Total Return of $SPX : 0.97759401457

Standard Deviation of Fund :  0.00717514512699
Standard Deviation of $SPX : 0.0149090969828

Average Daily Return of Fund :  0.000549352749569
Average Daily Return of $SPX : 1.72238432443e-05
</pre>
<img src="http://farm9.staticflickr.com/8259/8681834976_6cee953c8b_z.jpg" />

<div>Bollinger Bands</div>
<img src="http://farm9.staticflickr.com/8116/8681844036_a0029286df_z.jpg" />
<br />
<img src="http://farm9.staticflickr.com/8257/8681848582_7c39e78766_z.jpg" />

&copy;zhengshu@mit.edu
