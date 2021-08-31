### Taxi-Driver
Taxi-driver is a simple project which uses Q-learning's concepts to allow a  taxi driver to learn the optimal way to pick up and drop off a passenger in differents maps.

#### Enviroment
The game takes place in a city which shaped like a grid in which there are 2 type of cells.
- Obstacles: cells not usable by the driver.
- Free cells:  cells where the driver can drive.

In each city there are three special free cells which contain the taxi departure position, the passenger departure position and the destination. The driver has to go to pick up the passenger and drop him off at his destination in the optimal way.
At each step the taxi driver performs 1 of the 6 different actions:
- Move to 1 of the 4 adjacent cells, the new cell must be free.
- Pick up the passenger, this action is only legal  if the taxi is in the passenger's starting position and  the passenger has not been picked up yet.
- Drop off the passenger, this action is only legal if the taxi is the passenger's destination cell, the execution of this action ends the game.

#### Q-learning approach 
The main idea behind the Q-learning concept is that we want the agent, in this case the driver, to interact with the enviroment to learn to decide which action to take to maximise its expected reward. In order to do that at each step a feedback will be given to agent in the form of a reward. 
More formally, at each step the agent is in a specific state, in this case the state is represented by its positiion and whether or not he has already picked up the passenger, and from each of these states the driver can perform 6 different actions. For each combinations $(state, action)$ the driver knows the current expected total reward also called `Q_value`  which is stored in`Q_table[state][action]`, these values are used and updated by the agent over and over again in order to increase their accuracy. 
In the beginning the `Q_table` is initialized to 0, meaning that the driver has no idea about the effects of any action in any state, in this way the agent will start to move randomly and collect the first information about the enviroment, but after a while he needs to expollit the information gathered, so for each state the agents chooses the action to take based on which has the best expected reward and the respective `Q_value` is updated.
We define the expected reward of a specific state $s$ performing a specific action $a$ at the step $t$ as: $Q(s_t, a_t) = E[R_{t+1} +\gamma R_{t + 2} + \gamma ^ 2 R_{t + 3}...](s_t, a_t)$ and we use Bellam's equation to update our `Q\_values`: $Q(s_t, a_t) = Q(s_t, a_t) + \alpha[R_{t + 1} + \gamma max_a Q(s_{t+1}, a) - Q(s_t, a_t)]$ where $\alpha$ is the learning rate and $\gamma$ is the discount factor to give the next reward more or less importance.
Now that we know how the agent uses and updates the `Q_table` to pick the action that is considered best at each step it's important to discuss the problem of explore vs expolit.
Let's analyze the trade-off between exploring and exploiting. If we let the agent always randomly choose an action, it could eventually learn the  `Q-table`, but the process will never be efficient. On the contrary, if we only choose an action based on the maximization of the  `Q-value`, the agent will tend to always take the same route, overfitting the current environment setup. Furthermore it will suffer from great variance as it will not be able to find the proper route in another environment setup.
To prevent those two scenarios to occur and to try to find a trade-off, we add another hyperparameter epsilon  `ϵ`, which is the probability with which we choose a random action instead of the one computed from the  `Q-table`.
Using the concepts explained the agent will be able to interact with the enviroment and build a solid knowledge of which is the best move for each state. 
Let's see how this approach is used in our case. The agent will complete many episodes in each of them it will start from is departure position, complete each step using the `ϵ` strategy and the already computed `Q_values` until the passenger is picked up and dropped off at the correct position. The `Q_values` tend to improve at each episode ending up with a optimal choice policy for out agent. 
In our case the following rewards are given to the agent:
- -10 points if the driver tries to complete an illegal action like driving on obstacles or picking up / dropping off the passengere in wrong position.
- -1 point for each step, in this way the agent will try to minimize the number of steps.
- +20 points if the driver picks up or drops off the passenger in the correct location. 


