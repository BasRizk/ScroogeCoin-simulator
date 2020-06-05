# ScroogeCoin-simulator

## How to use

There are two modes: Normal Mode and _Debug Mode_. That is determined by the value of the boolean _DEBUG_MODE_. In normal mode, the system keeps generating transactions every some amount of delay that is determined byt the variable _delay_ where the value is in seconds. The system can be terminated by pressing _space_. In _Debug Mode_, A user can interact with the system by requesting a double spending attack (pressing _D_), requesting a verification attack (pressing _O_), or printing the Merkle Tree (pressing _M_). Here in debug mode the system does not proceed automatically. A user can press any of these keys at every step or press _Enter_ to proceed to the next step. Also _Space_ is used to terminate the system.

At every step, what happens is, a user generates a transaction. The transaction gets handled by Scrooge. Then the user might attempt to attack the system with a double spending attack by generating the same transaction but maybe to different user. That has 1:50 chance to happen or happens if the attack was requested in Debug Mode. Accordingly, Scrooge handle this transaction too and ignore it as it is a double spending attack. At every transaction, the recipient tries to confirm the incoming transaction before and after the transaction to show that the user does not confirm a transaction unless it is published in the blockchain. However that could be overridden by changing the _verify_ input from _True_ to _False_ so the user ignore the verification step, but that is not simulated in the current system.
After every step, all recipients check if their transactions were published and if so they confirm them.


### Tips
- Hold _Enter_ in _Debug Mode_ to keep generating transactions the same way as Normal Mode.
- _Debug Mode_ is recommened to Debug/Trace the system.
