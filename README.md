## Taxi-Driver
Taxi-driver is a simple project which uses Q-learning concepts to allow a taxi driver to learn the optimal way to pick up and drop off a passenger on different maps.

### Environment
The game takes place in a city that is shaped like a grid in which there are 2 types of cells:

Obstacles: cells not usable by the driver.
Free cells: cells where the driver can drive.
In each city, there are three special free cells that contain the taxi departure position, the passenger departure position, and the destination. The driver has to go to pick up the passenger and drop him off at his destination in an optimal way. At each step the taxi driver performs 1 of the 6 different actions:

Move to 1 of the 4 adjacent cells, the new cell must be free.
Pick up the passenger, this action is only legal if the taxi is in the passenger's starting position and the passenger has not been picked up yet.
Drop off the passenger, this action is only legal if the taxi is the passenger's destination cell, the execution of this action ends the game.

### Q-learning approach

The main idea behind the Q-learning concept is that we want the agent, in this case, the driver, to interact with the environment to learn to decide which action to take to maximize its expected reward. In order to do that at each step, feedback will be given to the agent in the form of a reward. More formally, at each step, the agent is in a specific state, in this case, the state is represented by its position and whether or not he has already picked up the passenger, and from each of these states, the driver can perform 6 different actions. For each combination, ![CodeCogsEqn (7)](https://user-images.githubusercontent.com/39414882/131535282-6971e21c-cd50-4cbe-9362-402cfa35e32f.gif) the driver knows the current expected total reward also called `Q_value` which is stored in `Q_table[state][action]`, these values are used and updated by the agent over and over again in order to increase their accuracy. In the beginning, the `Q_table` is initialized to 0, meaning that the driver has no idea about the effects of any action in any state, in this way the agent will start to move randomly and collect the first information about the environment, but after a while, he needs to exploit the information gathered, so for each state, the agent chooses the action to take based on which has the best-expected reward. We define the expected reward of a specific state ![CodeCogsEqn (5)](https://user-images.githubusercontent.com/39414882/131535088-f7560e41-7aeb-439f-84c5-1cd45375a497.gif) performing a specific action ![CodeCogsEqn (4)](https://user-images.githubusercontent.com/39414882/131535110-57aa9de0-751f-442f-a270-1af73fd8cc36.gif) at the step ![CodeCogsEqn (6)](https://user-images.githubusercontent.com/39414882/131535078-be60ed89-328b-49b4-b6f1-30b2abe6f7f7.gif)
 as: ![CodeCogsEqn](https://user-images.githubusercontent.com/39414882/131534552-8642bd9c-2d8b-4df0-ad95-24b96fcd8359.gif)  and we use Bellam's equation to update our `Q_values`: ![CodeCogsEqn (1)](https://user-images.githubusercontent.com/39414882/131534728-1b99d841-26c4-47dc-8531-543b521ba4f3.gif)  where ![CodeCogsEqn (2)](https://user-images.githubusercontent.com/39414882/131534795-89d48e15-54a9-4a2d-a829-230f1390b106.gif)
 is the learning rate and ![CodeCogsEqn (3)](https://user-images.githubusercontent.com/39414882/131534864-b5bb2529-20c8-4616-9436-aaef563ca019.gif)
 is the discount factor to give the next reward more or less importance. Now that we know how the agent uses and updates the `Q_table` to pick the action that is considered best at each step it's important to discuss the problem of exploring vs exploiting. Let's analyze the trade-off between exploring and exploiting. If we let the agent always randomly choose an action, it could eventually learn the `Q-table`, but the process will never be efficient. On the contrary, if we only choose an action based on the maximization of the `Q-value`, the agent will tend to always take the same route, overfitting the current environment setup. Furthermore, it will suffer from great variance as it will not be able to find the proper route in another environment setup. To prevent those two scenarios to occur and to try to find a trade-off, we add another hyperparameter epsilon ϵ, which is the probability with which we choose a random action instead of the one computed from the `Q-table`. Using the concepts explained the agent will be able to interact with the environment and build a solid knowledge of which is the best move for each state. Let's see how this approach is used in our case. The agent will simulate many episodes in each of them it will start from is departure position, complete each step using the ϵ strategy and the already computed `Q_values` until the passenger is picked up and dropped off at the correct position. The `Q_values` tend to improve at each episode ending up with an optimal choice policy for our agent.

In our case the following rewards are given to the agent:
- -10 points if the driver tries to complete an illegal action like driving on obstacles or picking up / dropping off the passenger in the wrong position.
- -1 point for each step, in this way the agent will try to minimize the number of steps.
- +20 points if the driver picks up or drops off the passenger in the correct location.


With the aim of maximizing its rewards, the agent will learn the optimal route for going to the starting position of the passenger and then go to its destination. Greater the number of episodes simulated and greater is the accuracy of the values in the `Q-table`


### Testing 

Let's see how the AI perform on a few maps, in each map the obstacles are grey cells, the departure cell of the taxi is blue, the departure point of the passengers is green and the destination of the passenger is red. 
#### Small Map
Let's start with a really small map(10 * 10), it only took 42 episodes to the AI to find the best route on this map.
<img width="749" alt="map" src="https://user-images.githubusercontent.com/39414882/131537672-dd966f08-9493-4ea3-8891-0bc037d4de0a.PNG">

This graph shows the number of steps required at each episode:

![steps_graph](https://user-images.githubusercontent.com/39414882/131537988-b103cfab-01be-4301-965f-4ec85ec6078b.png)

How you can see it's been trained for 150 episodes but it was able to get the optimal path much earlier than that.

The first few episodes are really random, this is the path found from the AI at the tenth attempt.


https://user-images.githubusercontent.com/39414882/131539785-31a9445c-8e44-41cf-bc5b-19a969b54919.mp4


While this is the solution found at episode 42.


https://user-images.githubusercontent.com/39414882/131539838-ae0e82a1-0cd9-4596-b755-a6123209b457.mp4


#### Medium Map with a Catch
This new map is a little bit bigger than the previous, but the idea behind it is that the big free space in the center of the city could slow the learning process. 

<img width="751" alt="map" src="https://user-images.githubusercontent.com/39414882/131540596-eafdeef1-7660-48e9-a56a-d6cee2c91164.PNG">

Let's take a look, once again, at the number of steps required:

![step_graph](https://user-images.githubusercontent.com/39414882/131540719-1a6b05fb-7244-4e71-9ffb-5cbf9b7c2c44.png)

We can see that this time the AI trained for 600 episodes and it was able to get the optimal route for the first time at the episode 526. The AI used many episodes before figuring out that all the free cells in the center of the map are completely  useless, indeed, at the 100th episode the agents was still making many random moves. 


https://user-images.githubusercontent.com/39414882/131541749-9ef90075-ee9a-459f-8c5f-ba3d463d9072.mp4

But in the end it was able to figure out the right path:


https://user-images.githubusercontent.com/39414882/131542051-dc459aef-9293-4502-bb0a-8692ff55e638.mp4

#### Large Map
This time the map is definitely bigger, it has 50 rows and 50 columns. Because of this the first few episodes, that are pretty much random, become really slow.

<img width="499" alt="map" src="https://user-images.githubusercontent.com/39414882/131543563-6c08a6a7-3468-41ee-91c6-eb7020b5e86d.PNG">

The AI was trained for 2000 episodes and was able to find the optimal route for the first time at the episode 1623.

![staps_graph](https://user-images.githubusercontent.com/39414882/131542509-93756c26-a6ac-4473-8e85-41733cf5bcd1.png)

As we can see the AI was still really "confused" also after 100 episodes:

https://user-images.githubusercontent.com/39414882/131543396-c3d88a4f-ba24-4c8d-831d-4aae1dd442dd.mp4

But in the end it was able to optimal the right path!

https://user-images.githubusercontent.com/39414882/131543443-2343c110-7b95-4b32-986b-54a05336f22d.mp4

