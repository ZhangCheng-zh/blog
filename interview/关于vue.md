## 如何聊vue
* 声明式
* 响应式
* 组件系统
    * 组件的复用
    * 组件间通信
* computed和watched
* 样式绑定
* 生命周期管理
    * beforeCreated
    * created
    * beforeMounted
    * mounted
    * beforeDestory
    * destory


## 聊vue核心-响应式原理
当一个普通的JavaScript对象传给Vue实例的data选项，Vue将遍历此对象所有
的属性，并使用Object.defineProperty将这些属性全部转为getter/setter。

