若需要显示可视化程序，请直接运行 visualization.py 文件



以下是对于一些重要逻辑和参数的解释：

- operation: 对应的是一个回合内的六项操作顺序，指示正在进行的操作，具体如下：

  1-己方移动，2-敌方移动，3-己方发射导弹，4-己方导弹追踪，5-敌方发射导弹，6-敌方导弹追踪

- 在以上六项操作中，只有1、2、3、5需要输入参数，其余两项导弹追踪会自动进行，对应的函数分别是：

  1, 2-move()	3,5-launch()	4,6-trace()



对于剩下的代码，其中一部分重要函数有编写注释， 对于另外一些非法操作会有弹窗提示