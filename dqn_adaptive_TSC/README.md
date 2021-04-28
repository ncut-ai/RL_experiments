# Adaptive Traffic Signal Control Using DQN

## 1. SUMO仿真模型

## 2. 算法实现

### 2.1 参数设置

### 2.2 定义环境

初始化
```python
env.init(env_setting=env_setting)
```

获取当前状态
```python
current_state = env.get_current_state()
```

执行动作，得到新的状态和奖励
```python
next_state, reward = env.step(action=action)
```

恢复环境，准备开始
```python
env.reset()
```
关闭环境
```python
env.clear()
```
### 2.3 定义神经网络

```python
# Neural Net for Deep Q Learning

# Sequential() creates the foundation of the layers.
model = Sequential()

# Input Layer of state size(4) and Hidden Layer with 24 nodes
model.add(Dense(24, input_dim=self.state_size, activation='relu'))
# Hidden layer with 24 nodes
model.add(Dense(24, activation='relu'))
# Output Layer with # of actions: 2 nodes (left, right)
model.add(Dense(self.action_size, activation='linear'))

# Create the model based on the information above
model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
```

### 2.4 定义DQN

损失是预测值与实际目标值之差。损失函数定义如下:
$$
loss=(Target-Prediction)^2\\
Target = r+\gamma\max_{a'}\hat{Q}(s,a')\\
Prediction = Q(s,a)\\
loss = \bigg(r+\gamma\max_{a'}\hat{Q}(s,a')-Q(s,a)\bigg)^2
$$
首先，执行动作 *a*，并观察奖励 *r* 和新状态 *s‘*。然后，计算最大目标Q值，并考虑折扣因素。最后，加上当前奖励，得到目标值；减去当前的预测得到loss。平方值使较大的loss值变大，且将负值作为正值对待。

定义目标：

```python
target = reward + gamma * np.amax(model.predict(next_state))
```

Keras 在`fit()`函数中实现求差值、求平方值、按学习率建立神经网络模型等全部操作；该函数通过学习率缩小预测值和目标值之差。通过更新过程，Q值逐渐逼近真实Q值。损失会逐渐降低。

### 2.5 经验存储

在神经网络中，算法会以新的经验覆盖之前的经验。因此，就需要用之前的经验再次进行模型训练。在DQN中，经验包括的内容有当前状态、动作、奖励、下一时刻状态。经验存储格式如下：
```python
memory = [(state, action, reward, next_state, done)...]
```

存储经验的函数如下：
```python
def memorize(self, state, action, reward, next_state, done):
    self.memory.append((state, action, reward, next_state, done))
```

`done` 是Boolean值，表示状态是否为最终状态。

## 经验重放 Replay

函数`replay()`采用经验存储中的经验进行模型训练。首先，对存储的经验进行采样：
```python
minibatch = random.sample(self.memory, batch_size)
```
通常，随机采样大小`batch_size`设为32，即小样本`minibatch`量为32.
为了使Agent更好实现长期效果，不仅需要考虑即时奖励，还需要考虑将来的奖励。因此引入折损率($\gamma$)。

```python
# Sample minibatch from the memory
minibatch = random.sample(self.memory, batch_size)

# Extract informations from each memory
for state, action, reward, next_state, done in minibatch:

    # if done, make our target reward
    target = reward

    if not done:
      # predict the future discounted reward
      target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

    # make the agent to approximately map
    # the current state to future discounted reward
    # We'll call that target_f
    target_f = self.model.predict(state)
    target_f[0][action] = target

    # Train the Neural Net with the state and target_f
    self.model.fit(state, target_f, epochs=1, verbose=0)
```

## 动作选择 eps-greedy

初始时，Agent随机选择动作；随后以`epsilon`概率进行探索，以`1-epsilon`概率选择最大Q值的动作。

```python
def act(self, state):
    if np.random.rand() <= self.epsilon:
        # The agent acts randomly
        return env.action_space.sample()

    # Predict the reward value based on the given state
    act_values = self.model.predict(state)

    # Pick the action based on the predicted reward
    return np.argmax(act_values[0])
```

## Hyper Parameters

- `episodes` - a number of games we want the agent to play.
- `gamma` - aka decay or discount rate, to calculate the future discounted reward.
- `epsilon` - aka exploration rate, this is the rate in which an agent randomly decides its action rather than prediction.
- `epsilon_decay` - we want to decrease the number of explorations as it gets good at playing games.
- `epsilon_min` - we want the agent to explore at least this amount.
- `learning_rate` - Determines how much neural net learns in each iteration.

## DQN Agent实现

```python
# Deep Q-learning Agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
              target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
```

## 训练模型

```python
if __name__ == "__main__":

    # initialize gym environment and the agent
    env = env.init(env_setting)
    agent = DQNAgent(agent_setting)

    # Iterate the game
    for e in range(episodes):

        env.reset()
        done=false
        # reset state in the beginning of each game
        state = env.get_current_state()
        state = np.reshape(state, [1, 4])

        # time_t represents each frame of the game
        # Our goal is to keep the pole upright as long as possible until score of 500
        # the more time_t the more score
        for time_t in range(500):
            # turn this on if you want to render
            # env.render()

            # Decide action
            action = agent.act(state)

            # Advance the game to the next frame based on the action.
            # Reward is 1 for every frame the pole survived
            
            next_state, reward = env.step(action=action)
            next_state = np.reshape(next_state, [1, 4])

            # memorize the previous state, action, reward, and done
            agent.memorize(state, action, reward, next_state, done)

            # make next_state the new current state for the next frame.
            state = next_state

            # done becomes True when the game ends
            # ex) The agent drops the pole
            if done:
                # print the score and break out of the loop
                print("episode: {}/{}, score: {}".format(e, episodes, time_t))
                break
            
        # train the agent with the experience of the episode
        done=true
        agent.replay(32)
        env.clear()