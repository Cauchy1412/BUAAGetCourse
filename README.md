# BUAAGetCourse
用来蹲北航教务给课程扩容的名额，解放双手双眼


第一版是用chromedriver登陆 用requests选课

第二版xuanke1.py参考了北航教务一键评教版本将登陆部分更新 不再需要chromedriver 更方便使用

`username`和`password`即账号和密码

`type`是想选课的类型（一般专业课 核心专业课 核心通识课 一般专业课）

`course`为想选的课程编号

`rwh`最后为001 正常都是001 似乎是相同课有不同老师（应该只有核心专业课用到）课程编号相同时有多门课则改为同名课程的第几个就是00几

