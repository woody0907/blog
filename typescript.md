###高级类型
####交叉类型

    Person & Serializable & Loggable

####联合类型

    function(value:string, padding:string | number){
        ....
    }

####类型保护与区分类型
#####用户自定义的类型保护

    function isFish(pet:Fish|Bird) pet is Fish{
        return (<Fish>pet).swim !== undefined;
    }
    //parameterName is Type 这种形式 parameterName 必须来自当前函数签名里的一个参数名

#####typeof 类型保护
#####instanceof类型保护
instanceof类型保护是通过构造函数来细化类型的一种方式
#####可选参数和可选属性
使用了--strictNullChecks，可选参数会被自动地加上| undefined
####类型别名
类型别名会给一个类型起个新名字。 类型别名有时和接口很像，但是可以作用于原始值，联合类型，元组以及其它任何你需要手写的类型
    
    type Name = string;
    type NameResolver = () => string;
    type NameOrResolver = Name | NameResolver;

####索引类型
    
    function pluck(T,K extends keyof T)(o:T,names:K[]):T[K][]{
        return names.map(n=>o[n]);
    }

####映射类型

    type ReadOnly<T> = {
        readonly [P in keyof T] : T[P];
    }
    type Partial<T> = {
        [P in keyof T]?: T[P];
    }
    type PersonReadOnly = ReadOnly<Person>;
    tyep PersonPartial = Partial<Person>;

###迭代器和生成器
当一个对象实现了Symbol.iterator属性时，我们认为它是可迭代的
####for...of语句

    let someArray = [1,'String']
    for (let entry of someArray){
        console.log(entry);
    }

    // 区别：for...in迭代的是对象的键的列表

###模块
模块在其自身的作用域里执行，而不是在全局作用域里；这意味着定义在一个模块里的变量，函数，类等等在模块外部是不可见的，除非你明确地使用export形式之一导出它们。 相反，如果想使用其它模块导出的变量，函数，类，接口等的时候，你必须要导入它们，可以使用 import形式之一。
模块使用模块加载器去导入其它的模块。 在运行时，模块加载器的作用是在执行此模块代码前去查找并执行这个模块的所有依赖。 大家最熟知的JavaScript模块加载器是__服务于Node.js的CommonJS__和__服务于Web应用的Require.js__。

####导出
* 导出声明
```
  export interface StringValidator{

  }
```
* 导出语句
```js
export{ZipCodeValidator};
export{ZipCodeValidator as mainValue}
```
* 重新导出
```js
export{ZipCodeValidator as mainValue} from "./ZipCodeValidator"
export * from "./ZipCodeValidator"
```
####导入
```js
import {zip} from "";
import {zip as z} from "";
import * as x from "";
```

####模块声明通配符

```js
declare moudle "*!text"{

}

import fileContent from "./xyz.txt!text";

```

####命名空间
```js
namespace Validation{

}
```
####别名
```js
namespace Shapes {
    export namespace Polygons {
        export class Triangle { }
        export class Square { }
    }
}

import polygons = Shapes.Polygons;
let sq = new polygons.Square(); // Same as "new Shapes.Polygons.Square()"
```

###模块解析

####Node.js如何解析模块
为了理解TypeScript编译依照的解析步骤，先弄明白Node.js模块是非常重要的。 通常，在Node.js里导入是通过 require函数调用进行的。 Node.js会根据 require的是相对路径还是非相对路径做出不同的行为。

相对路径很简单。 例如，假设有一个文件路径为 /root/src/moduleA.js，包含了一个导入var x = require("./moduleB"); Node.js以下面的顺序解析这个导入：

    将/root/src/moduleB.js视为文件，检查是否存在。

    将/root/src/moduleB视为目录，检查是否它包含package.json文件并且其指定了一个"main"模块。 在我们的例子里，如果Node.js发现文件 /root/src/moduleB/package.json包含了{ "main": "lib/mainModule.js" }，那么Node.js会引用/root/src/moduleB/lib/mainModule.js。

    将/root/src/moduleB视为目录，检查它是否包含index.js文件。 这个文件会被隐式地当作那个文件夹下的"main"模块。


但是，非相对模块名的解析是个完全不同的过程。 Node会在一个特殊的文件夹 node_modules里查找你的模块。 node_modules可能与当前文件在同一级目录下，或者在上层目录里。 Node会向上级目录遍历，查找每个 node_modules直到它找到要加载的模块。

还是用上面例子，但假设/root/src/moduleA.js里使用的是非相对路径导入var x = require("moduleB");。 Node则会以下面的顺序去解析 moduleB，直到有一个匹配上。

    /root/src/node_modules/moduleB.js
    /root/src/node_modules/moduleB/package.json (如果指定了"main"属性)
    /root/src/node_modules/moduleB/index.js

    /root/node_modules/moduleB.js
    /root/node_modules/moduleB/package.json (如果指定了"main"属性)
    /root/node_modules/moduleB/index.js

    /node_modules/moduleB.js
    /node_modules/moduleB/package.json (如果指定了"main"属性)
    /node_modules/moduleB/index.js

注意Node.js在步骤（4）和（7）会向上跳一级目录

####TypeScript如何解析模块
TypeScript是模仿Node.js运行时的解析策略来在编译阶段定位模块定义文件。 因此，TypeScript在Node解析逻辑基础上增加了TypeScript源文件的扩展名（ .ts，.tsx和.d.ts）。 同时，TypeScript在 package.json里使用字段"types"来表示类似"main"的意义 - 编译器会使用它来找到要使用的"main"定义文件。

比如，有一个导入语句import { b } from "./moduleB"在/root/src/moduleA.ts里，会以下面的流程来定位"./moduleB"：

    /root/src/moduleB.ts
    /root/src/moduleB.tsx
    /root/src/moduleB.d.ts
    /root/src/moduleB/package.json (如果指定了"types"属性)
    /root/src/moduleB/index.ts
    /root/src/moduleB/index.tsx
    /root/src/moduleB/index.d.ts

回想一下Node.js先查找moduleB.js文件，然后是合适的package.json，再之后是index.js。

类似地，非相对的导入会遵循Node.js的解析逻辑，首先查找文件，然后是合适的文件夹。 因此 /root/src/moduleA.ts文件里的import { b } from "moduleB"会以下面的查找顺序解析：

    /root/src/node_modules/moduleB.ts
    /root/src/node_modules/moduleB.tsx
    /root/src/node_modules/moduleB.d.ts
    /root/src/node_modules/moduleB/package.json (如果指定了"types"属性)
    /root/src/node_modules/moduleB/index.ts
    /root/src/node_modules/moduleB/index.tsx
    /root/src/node_modules/moduleB/index.d.ts

    /root/node_modules/moduleB.ts
    /root/node_modules/moduleB.tsx
    /root/node_modules/moduleB.d.ts
    /root/node_modules/moduleB/package.json (如果指定了"types"属性)
    /root/node_modules/moduleB/index.ts
    /root/node_modules/moduleB/index.tsx
    /root/node_modules/moduleB/index.d.ts

    /node_modules/moduleB.ts
    /node_modules/moduleB.tsx
    /node_modules/moduleB.d.ts
    /node_modules/moduleB/package.json (如果指定了"types"属性)
    /node_modules/moduleB/index.ts
    /node_modules/moduleB/index.tsx
    /node_modules/moduleB/index.d.ts

不要被这里步骤的数量吓到 - TypeScript只是在步骤（8）和（15）向上跳了两次目录。 这并不比Node.js里的流程复杂。 

####附加的模块解析标记
#####baseurl
baseUrl的值由以下两者之一决定：

    命令行中baseUrl的值（如果给定的路径是相对的，那么将相对于当前路径进行计算）
    ‘tsconfig.json’里的baseUrl属性（如果给定的路径是相对的，那么将相对于‘tsconfig.json’路径进行计算）

注意相对模块的导入不会被设置的baseUrl所影响，因为它们总是相对于导入它们的文件。

#####路径映射

TypeScript编译器通过使用tsconfig.json文件里的"paths"来支持这样的声明映射。 下面是一个如何指定 jquery的"paths"的例子。

{
  "compilerOptions": {
    "baseUrl": ".", // This must be specified if "paths" is.
    "paths": {
      "jquery": ["node_modules/jquery/dist/jquery"] // 此处映射是相对于"baseUrl"
    }
  }
}

请注意"paths"是相对于"baseUrl"进行解析。 如果 "baseUrl"被设置成了除"."外的其它值，比如tsconfig.json所在的目录，那么映射必须要做相应的改变。 如果你在上例中设置了 "baseUrl": "./src"，那么jquery应该映射到"../node_modules/jquery/dist/jquery"。
#####利用rootDirs指定虚拟目录
可以使用"rootDirs"来告诉编译器。 "rootDirs"指定了一个roots列表，列表里的内容会在运行时被合并。 因此，针对这个例子， tsconfig.json如下：

    {
      "compilerOptions": {
        "rootDirs": [
          "src/views",
          "generated/templates/views"
        ]
      }
    }

####跟踪模块解析
如之前讨论，编译器在解析模块时可能访问当前文件夹外的文件。 这会导致很难诊断模块为什么没有被解析，或解析到了错误的位置。 通过 --traceResolution启用编译器的模块解析跟踪，它会告诉我们在模块解析过程中发生了什么。

假设我们有一个使用了typescript模块的简单应用。 app.ts里有一个这样的导入import * as ts from "typescript"。

    │   tsconfig.json
    ├───node_modules
    │   └───typescript
    │       └───lib
    │               typescript.d.ts
    └───src
            app.ts

    使用--traceResolution调用编译器。

    tsc --traceResolution
###声明合并
“声明合并”是指编译器将针对同一个名字的两个独立声明合并为单一声明。 合并后的声明同时拥有原先两个声明的特性。 任何数量的声明都可被合并；不局限于两个声明。 

TypeScript中的声明会创建以下三种实体之一：命名空间，类型或值。 创建命名空间的声明会新建一个命名空间，它包含了用（.）符号来访问时使用的名字。 创建类型的声明是：用声明的模型创建一个类型并绑定到给定的名字上。 最后，创建值的声明会创建在JavaScript输出中看到的值。

###JSX
JSX是一种嵌入式的类似XML的语法。 它可以被转换成合法的JavaScript，尽管转换的语义是依据不同的实现而定的。 JSX因 React框架而流行，但是也被其它应用所使用。 TypeScript支持内嵌，类型检查和将JSX直接编译为JavaScript。

想要使用JSX必须做两件事：

    给文件一个.tsx扩展名
    启用jsx选项

TypeScript具有三种JSX模式：preserve，react和react-native。

###三斜线指令
三斜线指令是包含单个XML标签的单行注释。 注释的内容会做为编译器指令使用。
三斜线指令仅可放在包含它的文件的最顶端。 一个三斜线指令的前面只能出现单行或多行注释，这包括其它的三斜线指令。 如果它们出现在一个语句或声明之后，那么它们会被当做普通的单行注释，并且不具有特殊的涵义。 


##项目配置
如果一个目录下存在一个tsconfig.json文件，那么它意味着这个目录是TypeScript项目的根目录。 tsconfig.json文件中指定了用来编译这个项目的根文件和编译选项。 一个项目可以通过以下方式之一来编译：
使用tsconfig.json

    不带任何输入文件的情况下调用tsc，编译器会从当前目录开始去查找tsconfig.json文件，逐级向上搜索父目录。
    不带任何输入文件的情况下调用tsc，且使用命令行参数--project（或-p）指定一个包含tsconfig.json文件的目录。

当命令行上指定了输入文件时，tsconfig.json文件会被忽略。

tsconfig.json文件可以利用extends属性从另一个配置文件里继承配置。





