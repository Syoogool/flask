## 记录学习flask中遇到的问题

### 1 蓝图
  - 错误描述：
  - 使用蓝图组织项目是出现：werkzeug.routing.BuildError: Could not build url for endpoint 'show_entries'. Did you mean 'front.show_entries' instead?
  - 原因： 不理解蓝图中 url_for()的用法
  - 解决： 在模板中使用url_for() 的传入参数前面加一个< . >

###  2  templates 位置
  -  我在蓝图下面设置了template_folder='templates/front',
    static_folder='static/front'  我以为对应查询的目录是蓝图的子目录，其实是根目录的templates  static的子目录下
