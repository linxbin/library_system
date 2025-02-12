# Library System

Library System 是一个简单的图书管理系统，支持用户注册、登录、借阅和归还图书等功能。该项目使用 Python 编写，并使用 JSON 文件进行数据存储。

## 功能

- 用户注册和登录
- 用户借阅和归还图书
- 管理员管理图书和用户
- 数据持久化存储到 JSON 文件

## 安装

### 先决条件

- Python 3.8+

### 克隆仓库

```bash
git clone https://github.com/yourusername/library_system.git
cd library_system
```

## 使用

### 运行项目

```bash
python main.py
```

### 用户操作

- 注册：在主菜单选择注册选项，输入用户名和密码进行注册。
- 登录：在主菜单选择登录选项，输入用户名和密码进行登录。
- 借阅图书：登录后选择借阅图书选项，输入图书 ISBN 进行借阅。
- 归还图书：登录后选择归还图书选项，输入图书 ISBN 进行归还。

### 管理员操作

- 管理图书：登录管理员账号后，可以添加、删除和编辑图书信息。
- 管理用户：登录管理员账号后，可以查看用户列表和重置用户密码。

## 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建你的分支 (`git checkout -b feature/your-feature`)
3. 提交你的修改 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建一个新的 Pull Request

## 许可证

该项目使用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
