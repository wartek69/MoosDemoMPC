# MoosDemoMPC
A MPC controller integrated into MOOS-IVP.
The steering is done using a rate-of-turn (ROT) and not the rudder angle!

# Models
The mpc can make use of three different models.
A rotdot model, a blackbox model and a mathematical model.
The first one approximates one parameter of the mathematical model using ML. The second one approximates all the parameters of the mathematical model using ML.
It is clear the math model performes the best, followed by the rotdot model and then the Black box model.

# Simulations
In the state right now the rotdot model and the mathematical model perform the same on the given example with a prediction horizon of 120 and a heading weight of 5.
The black box model is not good enough and thus cannot follow the path with the tuning parameters above.
If we change the prediction horizon to 20 instead of 120 we can see that the path can be followed. There is one oscillation that appears in the first turn. The reason for that is that the model is not trained well enough and thus contains errors.
The reason that lowering the prediction horizon gives a better result for the black box model is because the model contains too much errors, so when we simulate longer the error increases and thus the actions we become from the simulations are biased.

# Conclusions
This PoC shows that it is of great importance to find a good model of a vessel to obtain good results. Even when the model is not perfect the controller can be tuned in such a way that a path following characte$
An interesting approach for obtaining a model could be to start from the mathematical model and using transfer learning improving that model for real vessels. For this approach it is necessary that there is enough qualitative data.
