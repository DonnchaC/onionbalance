Use Cases
=========

There a many ways to use OnionBalance to increase the scalability, reliability and security of your onion service. The following are some examples of what is
possible.


Current Deployments
-------------------

**SKS Keyserver Pool**
  Kristian Fiskerstrand has set up a hidden service
  `keyserver pool <https://sks-keyservers.net/overview-of-pools.php#pool_tor>`_
  which connects users to one of the available hidden service key servers.



Other Examples
--------------

- A popular onion service with an overloaded web server or Tor process

  A service such as Facebook which gets a large number of users would like
  to distribute client requests across multiple servers as the load is too
  much for a single Tor instance to handle. They would also like to balance
  between instances when the 'encrypted services' proposal is implemented [2555].

- Redundancy and automatic failover

  A political activist would like to keep their web service accessible and
  secure in the event that the secret police seize some of their servers.
  Clients should ideally automatically fail-over to another online instances
  with minimal service disruption.

- Secure Onion Service Key storage

  An onion service operator would like to compartmentalize their permanent
  onion key in a secure location separate to their Tor process and other
  services. With this proposal permanent keys could be stored on an
  independent, isolated system.

Research
--------

`Ceysun Sucu <https://github.com/csucu>`_ has analysed OnionBalance and other
approaches to hidden service scaling in his masters thesis
`Tor\: Hidden Service Scaling <https://www.benthamsgaze.org/wp-content/uploads/2015/11/sucu-torscaling.pdf>`_. The thesis provides a good overview of current approaches. It is a recommended read for those
interested in higher performance hidden services.
