* <h1>完成状态</h1>
	* 设计完problem、status、register、login界面 --2013.4.29
	* 添加自定义404 Not Found --2013.4.30
	* 添加session,支持register，login，logout，profile，problemset，修改了url --2013.5.1
	* 添加了problemset和problem的操作，主要是获取题目ID，然后在/static/中读取problem。--2013.5.2
	* 题目的html存不存储到数据库里面，因为现在不知道怎么解决编码问题。一些超过了128的字符集在数据库中存储就变成乱码了。--2013.5.2
	* 添加codeforces的提交，不过每次只能处理一个提交。在数据库里面，用status_hash这个哈希值来确定一个提交在数据库里的对应项。--2013.5.4

* <h1> 约定 </h1>
	* 语言的名称第一个字母大写，后面都是用小写

* <h1>OJ功能</h1>
	* 题目列表
		* 在建立OJ的时候缓存所有爬到的题目，以后只需要更新没有在缓存的题目即可
		* 添加题目时先在缓存中查询题目是否存在，如果不存在就去网站上爬
		* 修改后的题目有题目名称、题目的算法标签、题目来源
	* 比赛 
		* 比赛分为private和public
		* 每一场比赛有1-26道题 
	* 用户的比赛  
		* 可以查询每个用户自己建立的比赛
	* 所有比赛 
		* 可以查询所有用户建立的比赛
	* 提交状态
		* 对于每一个用户都有一个OJ的status
		* 用户可以看到提交当且仅当满足一下条件
			* 超级用户 
			* 源码提交者
			* 源码提交的OJ所属者
		* 状态列表 
			* 提交ID，每一个OJ独立，从1开始算
			* 提交源码的用户ID
			* 提交时间
			* 返回状态 
				* Accepted
				* Wrong Answer
				* Time Limit Exceeded
				* Run Time Error
				* Pending -- submit code and wait for robot to get final status

* 用户 
	* root - 拥有OJ的所有权限
	* 注册信息
		* 帐号 
			* 只能包含数字，字母，下划线，@
		* 密码
			* 不能有空格
			* 仅在数据库中保存HASH后的字符串
		* 邮件
			* 用来找回密码
	* 每个用户都有一个OJ，地址格式为URL/USER_HANDLE，一般用户的权限有
		* 添加题目
		* 修改题目的算法TAG
		* 下载自己的所有源码
	* 每个用户都有自己的PROBLEM_SOLVE_RECORD，题目名为题目来源OJ加题号


* <h1>HTML部分</h1>
	* form提交数据
		* 在form> </form>里面用name标记一下输入的东西，以及定义action，然后submit数据就可以提交到指定地址
	* 模态对话框
		* 参看submit那一段代码就可以了
<<<<<<< HEAD
	* session
		* 用来维持服务器和用户之间的链接状态
		* 如果30分钟内用户没有动作则session失效
		* webpy在debug情况下不能正确使用session，所以要在startup时关掉debug
		* session在新tab中可以维持状态，在新窗口中就是不同的session了
=======
	*
>>>>>>> 2fb779b34fa78e12ddcfe22218a5accaa4da718f
