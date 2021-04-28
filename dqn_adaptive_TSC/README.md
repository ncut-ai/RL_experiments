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

One of the challenges for DQN is that neural network used in the algorithm tends to forget the previous experiences as it overwrites them with new experiences. So we need a list of previous experiences and observations to re-train the model with the previous experiences. We will call this array of experiences `memory` and use `memorize()` function to append state, action, reward, and next state to the memory.

In our example, the memory list will have a form of:

```python
memory = [(state, action, reward, next_state, done)...]
```

And memorize function will simply store states, actions and resulting rewards to the memory like below:

```python
def memorize(self, state, action, reward, next_state, done):
    self.memory.append((state, action, reward, next_state, done))
```

`done` is just a Boolean that indicates if the state is the final state.

## Replay

A method that trains the neural net with experiences in the `memory` is called `replay()`. First, we sample some experiences from the `memory` and call them `minibath`.

```python
minibatch = random.sample(self.memory, batch_size)
```

The above code will make `minibatch`, which is just a randomly sampled elements of the memories of size `batch_size`. We set the batch size as 32 for this example.

To make the agent perform well in long-term, we need to take into account not only the immediate rewards but also the future rewards we are going to get. In order to do this, we are going to have a ‘discount rate’ or ‘gamma’. This way the agent will learn to maximize the discounted future reward based on the given state.

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

