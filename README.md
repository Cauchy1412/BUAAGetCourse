# BUAAGetCourse
用来蹲北航教务给课程扩容的名额，解放双手双眼

(换课请联系教务进行换课 小心截胡）


第一版grabcourse.py是用Selenium登陆 用requests选课

第二版xuanke.py参考了[北航教务一键评教版本](https://github.com/bearbattle/buaa-teacher-evaluation)将登陆部分更新 不再需要Selenium 仅使用requests 更方便使用

`username`和`password`即账号和密码

`type`是想选课的类型（一般专业课 核心专业课 核心通识课 一般专业课）

`course`为想选的课程编号

`rwh`的末尾默认为001  在相同课程编号有不同老师（应该只有核心专业课用到）想选同名课程的第n个则改为00n  

**grabcourse.py在2021年秋季学期测试过可正常使用**

**xuanke.py在2022年春季学期测试过可正常使用**
