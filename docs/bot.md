> `web.Bot`与此文档均由[plap](https://github.com/wsxiaolin/plap)的作者[故事里的人](https://github.com/wsxiaolin)提供, 因此本文档虽然为js但与`web.Bot`的设计有异曲同工之妙
>
> <del>所以这就是我偷懒的理由?</del>

## 简介

物实脚本机器人是一个用于自动回复和处理消息的工具，内置了回复、读取信息、过滤消息、异步处理和任务队列等功能。该机器人能够高效地与用户互动，并根据特定的配置进行灵活的消息处理。

## 特性

- **自动回复**：根据接收到的消息内容自动生成回复。
- **历史消息读取**：可以选择是否读取历史消息。
- **任务队列**：支持异步处理消息，确保消息的有序处理。
- **自定义回调**：提供多种回调函数以便于扩展功能。

## 方法

### init

- 前两个参数为回复的位置，为物实 ID（对象序列号）和类型（User,Experiment,Discussion）
- 第三个参数为信息捕获策略
- 第四个参数为机器人预制类型

### run

调用run会处理一次消息，方法本身是异步的，但不会等到服务器响应，一次run在发送消息之后就结束了，监听消息队列是否完成，请使用回调函数finished

## 使用示例

```javascript

async function processFunction(msg, botInstance) {
  await new Promise(resolve => setTimeout(resolve, 5000)); // 模拟延迟
  return '这是机器人的回复。'; // 返回机器人的回复内容
}

const myBot = new Pl.Bot(
  "your_email@example.com",
  process.env.PASSWORD,
  processFunction, // 消息处理函数
  (i) => {
    console.log("捕获到的消息来自: " + i.Nickname); // 捕获消息后的回调
  },
  (i) => {
    console.log("成功回复的消息: " + i); // 成功回复后的回调
  },
  (list) => {
    console.log("所有任务完成，回复列表: ", list); // 完成任务队列后的回调
    process.exit(0); // 退出程序
  }
);

async function main() {
  // 初始化并登录
  await myBot.init("66fab3b39c503ff86ad94078", "Discussion", {
    ignoreReplyToOters: true, // 忽略回复他人的信息
    readHistory: false, // 是否读取开启前未回复的历史内容
    replyRequired: false, // 是否只读取回复机器人的内容
  });

  // 定时运行机器人
  setInterval(() => { myBot.run(); }, 1000);
}

main();
```

## 回调函数说明

- **`caught`**: 捕获到消息后调用的回调函数。此函数接受一个参数 `i`，表示捕获的消息对象，你可以在此处进行日志记录或其他处理。若返回-1则忽略本消息

- **`replied`**: 成功回复消息后调用的回调函数。此函数同样接受一个参数 `i`，表示被回复的消息内容，i.msg表示回复的内容。

- **`finnished`**: 在任务队列完成后调用的回调函数。此函数接受一个参数 `list`，表示已处理的消息列表。

## API 说明

### `Bot` 类

- **方法**:
  - `init`: 初始化并将Bot绑定到用户账号
  - `run`: 运行机器人以处理新消息

## 配置选项

- `is_ignore_reply_to_others`: 是否忽略对他人的回复（默认为 `true`）。
- `is_read_history`: 是否读取历史消息（默认为 `true`）。
- `is_reply_required`: 是否仅回复机器人的消息（默认为 `true`）。
