function Foo () {
    getName = function () { alert(1)};
    return this;
}

Foo.getName = function () {alert(2)};

Foo.prototype.getName = function () {alert(3)};

// 变量声明会提前到头部， 变量赋值不会提升到头部
var getName = function () {alert(4)};

// 函数声明也会提前到头部
function getName () {alert(5)};

