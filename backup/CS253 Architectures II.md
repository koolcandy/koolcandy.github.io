## CS253 Architectures II

### Lecture 1: CPU

计算机信号分为**模拟信号**和**数字信号**

#### 计算机架构

计算机有两种主要类型: 

**冯诺伊曼架构**和**Harvard架构**

![img](https://s2.loli.net/2025/01/13/sJDwESPr8o4dnvm.png)

冯诺依曼结构的处理器使用**同一个存储器, 经由同一个总线传输**

> 现代高性能CPU芯片在设计上包含了哈佛和冯诺依曼结构的特点。特别是, “拆分缓存”这种改进型的哈佛架构版本是很常见的。  CPU的缓存分为指令缓存和数据缓存。CPU访问缓存时使用哈佛体系结构。然而当高速缓存未命中时, 数据从主存储器中检索, 却并不分为独立的指令和数据部分, 虽然它有独立的内存控制器用于访问RAM, ROM和 (NOR )闪存。 因此, 在一些情况下可以看到冯诺依曼架构, 比如当数据和代码通过相同的内存控制器时, 这种硬件通过哈佛架构在缓存访问或至少主内存访问方面提高了执行效率。 此外, 在写非缓存区之后, CPU经常拥有写缓存使CPU可以继续执行。当指令被CPU当作数据写入, 且软件必须确保在试图执行这些刚写入的指令之前, 高速缓存 (指令和数据 )和写缓存是同步的, 这时冯诺依曼结构的内存特点就出现了。

#### 8086的硬件组成

![img](https://s2.loli.net/2025/01/13/m2kdoTtbw8MYcWz.png)

**BIU: 总线接口单元**
BIU发送地址, 从内存中获取指令, 并对端口和内存进行读写操作

**EU: 执行单元**
EU指示BIU从哪里获取指令, 它解码指令并执行指令
EU包含ALU和控制电路

**指令周期 (*instruction cycle*)**就是 fetch-decode-execute 的过程通常一个指令大概占用 4 个指令周期, 所以一个 1GHz 的处理器, 一秒内大约可以执行 2.5 亿行汇编代码

#### ALU

8086 的 ALU 可以执行:

- **ADD**: 加法  
- **Subtract**: 减法  
- **AND**: 逻辑与  
- **OR**: 逻辑或  
- **XOR**: 逻辑异或  
- **increment**: 自增  
- **decrement**: 自减  
- **complement**: 取反  
- **shift 16-bit binary numbers**: 移位 (16位二进制数 )  

![img](https://s2.loli.net/2025/01/13/jqoGxpcAhRwQDuS.png)

左移右移的实现方法:

![img](https://s2.loli.net/2025/01/13/jq8DOK7XleVby6m.png)

---

### Lecture 2: Assembly Language (Ⅰ)

#### 寄存器们

**通用寄存器**

8086 有 8 个通用寄存器, 可以将它们视为 8 个变量, 某些指令可以成对使用 registers, 从而提供 16 位操作, 当用作寄存器对时, 它们被赋予集体名称 AX、BX、CX、DX

![img](https://s2.loli.net/2025/01/13/6XusCizPvyElda5.png)

**标志位寄存器**

8086 在特殊的 16 位标志寄存器中跟踪某些计算的结果

- **U: Undefined (未定义)**  
- **OF: Overflow flag (溢出标志)**  
- **DF: String direction flag (字符串方向标志)**  
- **IF: Interrupt enable flag (中断启用标志)**  
- **TF: Single step trap flag (单步陷阱标志)**  
- **SF: Sign flag (符号标志, 结果的最高有效位)**  
- **ZF: Zero flag, set if result=0 (零标志, 如果结果为零则设置)**  
- **AF: BCD Carry flag (BCD 进位标志)**  
- **PF: Parity flag (奇偶校验标志)**  
- **CF: Carry flag (进位标志)**  

![img](https://s2.loli.net/2025/01/13/gKDLaGo7bkx8ApV.png)

#### 8086的分段内存模型

因为8086的寄存器只有16位, 为了让它能访问20位的地址, 需要使用CS 寄存器给出代码段地址, IP 寄存器给出偏移距离, 然后计算出指令的内存地址位置

![img](https://s2.loli.net/2025/01/13/jVTmYHvgo5yWqn4.png)

类似的, 这些段寄存器也都是为了使用8086的分段内存模型

- **DS (Data Segment Register):** 数据段寄存器

  指向程序的数据所在的内存段, DS 寄存器存储程序数据段的起始地址访问数据时, 需要指定一个偏移量, 指明数据在数据段内的位置, 通过`DS:偏移量`配合工作

  **偏移量的来源:**

  - **直接寻址:** 偏移量可以是指令中直接给出的一个常量例如 mov ax, [0x1234], 这里 0x1234 是一个偏移量
  - **寄存器寻址:** 偏移量可以使用通用寄存器 (例如 BX, SI, DI) 例如 mov ax, [bx], 这里 bx 存储偏移量
  - **寄存器 + 常量: ** 偏移量可以是寄存器值 + 常量例如 mov ax, [bx+0x10], 这里 bx 存储偏移量, 0x10 是常量

- **SS (Stack Segment Register):** 堆栈段寄存器

  指向堆栈所在的内存段, SS 寄存器存储堆栈段的起始地址

  **SP 寄存器**指向当前栈顶的地址它始终指向栈中最后一个被压入 (pushed) 的值的位置

  **BP 寄存器**通常指向当前栈帧的基地址, 主要用途是: 

  - 在函数调用过程中, BP 作为访问函数局部变量、函数参数的基址
  - 方便函数内部访问栈上的数据
  - 可以在函数返回时恢复栈帧

- **ES (Extra Segment Register):** 附加段寄存器

  用于字符串操作的额外数据段, 通常作为目标段使用, 通过`ES:DI`配合工作

#### MASM 程序结构

**程序结构**

![img](https://s2.loli.net/2025/01/13/upM8tPTJZV7G6Ys.png)

**编译过程**

![img](https://s2.loli.net/2025/01/13/KgnFof1tA2mGOVy.png)

**运算符和操作数**

![img](https://s2.loli.net/2025/01/13/xihBSNqcRGupv5V.png)

这里的Operand也可以称作`立即数`

#### Hello, world !

```assembly
.MODEL medium
.STACK
.DATA

msg1 db "Hello, world.$"

.CODE
.STARTUP

mov ax,@data                    ; 将 ax 寄存器的值设置为 @data 段的值
mov ds,ax                       ; 将 DS 寄存器的值设置为 @data 段的值
lea bx,msg1                     ; 获得msg1的偏移地址, 在这个情况下(DS<<4+BX)就是实际的存储msg1的地址

back:
    mov dl,[bx]                 ; 间接寻址, 获取bx寄存器对应的内存地址的第一个值到dx寄存器
    cmp dl,'$'                  ; 将 dl 寄存器中的字符与字符 $ 进行比较
    jz done                     ; 如果 dl 寄存器中的字符和$相等 (即 ZF 标志位为 1 ), 则跳转到done执行

    mov ah,02h                  ; 设置 DOS 中断 21h 的功能号为 02h, 表示调用显示字符的功能
    int 21h                     ; 调用 DOS 中断 21h, 将 dl 寄存器中的字符显示在屏幕上

    inc bx                      ; 将 bx 寄存器的值加 1, 指向字符串 msg1 的下一个字符
    jmp back                    ; 无条件跳转到 back 标签处

done:
    nop                         ; 空操作指令

.EXIT

END
```

当然也可以更简单

```assembly
.MODEL small
.STACK
.DATA
    msg DB 'Hello, World!$'    ; 定义字符串，以$结尾
    
.CODE
.STARTUP

    mov ax, @data
    mov ds, ax

    mov ah, 09h               ; 打印字符串
    lea dx, msg
    int 21h

.EXIT

END
```

**常用 21h 功能号**

- **01h:** 从键盘读取一个字符, 并将字符存入 AL 寄存器
- **02h:** 在屏幕上输出 DL 寄存器中的字符
- **09h:** 在屏幕上输出以 DS:DX 指向的、以 $ 结尾的字符串
- **0Ah:** 从键盘读取一个字符串
- **3Ch:** 创建一个文件
- **3Dh:** 打开一个文件
- **3Eh:** 关闭一个文件
- **3Fh:** 从文件中读取数据
- **40h:** 向文件中写入数据
- **4Ch:** 退出程序

**一些重要ASCII码**

**0x0A: Line Feed,LF, 换行** 等价于`\n`

**0x0D: Carriage Return,CR,回车** 等价于`\r`

---

### Lecture 3: Assembly Language (Ⅱ)

#### 寻址模式

**立即寻址**
运算数以 **字面量** 形式写在指令里面, 如 `mov ax, 10`, 这里的运算数也称作 *立即数*

**寄存器寻址**
指运算数保存在某个通用寄存器当中, 如 `mov ax, bx`
寄存器的访问是在 CPU 内部的, 非常非常快, 不需要寻址

**直接寻址**
比如 `mov ax, Count`, 就把 data 段当中的变量 `Count` 作为操作数
实际上, 变量 `Count` 在汇编器的眼里, 只不过是对应数据所在的地址罢了所以相当于把 `Count` 所在地址的值赋给 `ax`
如果要指定其他的段, 可以写作 `mov ax, ES:Count`, 即表示在额外段上的内容

**寄存器间接寻址**
相对于直接寻址 (把偏移地址直接以字面量的形式写在指令当中 ), 寄存器间接寻址是 **把偏移地址存在寄存器 (通常是索引寄存器 BX, BP, SI 或 DI )当中**如果是 BP, 那对应的段就是栈段, 否则就是数据段
这种寻址方式的写法, 跟高级语言当中的数组比较类似: 

- `mov ax, [bx]` 表示 `ax = array[bx]`
- `mov [bx], ax` 表示 `array[bx] = ax`

#### 8086 指令格式

![img](https://s2.loli.net/2025/01/13/ENAvqQBwh7eMtfO.png)

**Byte 1: **

- **Opcode (操作码): ** 决定指令的动作 (如 MOV )
- **D (方向): ** 数据传输方向, 源到目标, 还是目标到源

**Byte 2: **

- **W (字/字节): ** 数据大小, 16 位字还是 8 位字节
- **Mod (寻址模式): ** 如何确定操作数地址
- **Reg (寄存器): ** 指示一个寄存器
- **R/M (寄存器/内存): ** 指示另一个操作数是寄存器还是内存

**Low Byte/High Byte: ** 可选, 如果指令需要, 用来存放立即数或内存地址偏移量

#### 8086寄存器编号

![img](https://s2.loli.net/2023/04/06/oshgKL6aU9YIAEW.png)

#### 8086寻址模式

![img](https://s2.loli.net/2025/01/13/cSqZUoIT2Of1tY4.png)

**Mod=00**:  **没有偏移量**, 或者仅仅是使用寄存器进行内存间接寻址

**Mod=01**:  **8 位偏移量** (d8),  需要额外的 1 个字节来存储偏移量

**Mod=10**:  **16 位偏移量** (d16),  需要额外的 2 个字节来存储偏移量

**Mod=11**:  **寄存器寻址**, 直接使用寄存器作为操作数, 不涉及内存访问

**例如**

`mov SP, BX` 的二进制指令是: 

| opcode | D           | W    | Mod            | Reg   | R/M   |
| ------ | ----------- | ---- | -------------- | ----- | ----- |
| 100010 | 1           | 1    | 11             | 100   | 011   |
| `mov`  | to register | word | 寄存器寻址模式 | to SP | to BX |

---

### Lecture 4: Assembly Language (Ⅲ)

#### 算数运算命令

| **指令** | **代码**     | **作用**                                             |
| -------- | ------------ | ---------------------------------------------------- |
| **ADD**  | `ADD AX, BX` | 加法运算, 将 AX 和 BX 相加, 结果存入 AX              |
| **ADC**  | `ADC AX, BX` | 带进位的加法运算, 将 AX, BX, CF 相加, 结果存入 AX    |
| **SUB**  | `SUB AX, BX` | 减法运算, 将 AX 减去 BX, 结果存入 AX                 |
| **MUL**  | `MUL BX`     | 无符号乘法, 将 AX 和 BX 相乘, 结果存入 DX:AX         |
| **IMUL** | `IMUL BX`    | 有符号乘法, 将 AX 和 BX 相乘, 结果存入 DX:AX         |
| **DIV**  | `DIV BX`     | 无符号除法, 将 DX:AX 除以 BX, 商存入 AX, 余数存入 DX |
| **IDIV** | `IDIV BX`    | 有符号除法, 将 DX:AX 除以 BX, 商存入 AX, 余数存入 DX |
| **INC**  | `INC AX`     | 自增运算, 将 AX 的值加 1                             |
| **DEC**  | `DEC AX`     | 自减运算, 将 AX 的值减 1                             |
| **NEG**  | `NEG AX`     | 取负运算, 将 AX 的值取负 (相当于 `0 - AX` )          |
| **CMP**  | `CMP AX, BX` | 比较运算, 比较 AX 和 BX 的值, 结果影响标志寄存器(ZF) |
| **CBW**  | `CBW`        | 将 AL 符号扩展到 AH (字节到字 )                      |
| **CWD**  | `CWD`        | 将 AX 符号扩展到 DX (字到双字 )                      |

> [!CAUTION]
>
> `DIV` 与 `IDIV`在除数是word(16bit)的时候, 被除数是 32 位的 `DX:AX`,`DX`的值可能会产生意想不到的结果
>
> `MUL` 与 `IMUL`在乘数是word(16bit)的时候, 结果是32位的, 低 16 位保存在 `AX` 里面, 高 16 位保存到 `DX` 里面, 导致`DX`寄存器的值被覆盖

#### 十进制算数

了解即可, 看不懂, 去死吧！[介绍](https://goo.su/Q3MVxu)

![img](https://s2.loli.net/2025/01/14/gFcZlVukbrEM7zt.png)

**AAA (加法后的ASCII调整)**
```assembly
mov al, '9'  ; AL = 39h ('9'的ASCII码)
add al, '8'  ; AL = 39h + 38h = 71h
aaa          ; 调整AL为09h, AH += 1 (AH = 01h)
; 结果: AL = 09h, AH = 01h (表示BCD格式的17)
```

**AAD (除法前的ASCII调整)**
```assembly
mov ax, 0507h  ; AH = 05h, AL = 07h (表示未压缩BCD的57)
aad            ; AX = 0037h (37的二进制形式)
mov bl, 6      ; BL = 6
div bl         ; AX / BL, AL = 6 (商), AH = 1 (余数)
; 结果: AL = 06h, AH = 01h
```

**AAM (乘法后的ASCII调整)**
```assembly
mov al, 9      ; AL = 09h
mov bl, 7      ; BL = 07h
mul bl         ; AX = AL * BL = 003Fh (63的二进制形式)
aam            ; AH = 06h, AL = 03h (表示未压缩BCD的63)
; 结果: AH = 06h, AL = 03h
```

**AAS (减法后的ASCII调整)**
```assembly
mov al, '3'  ; AL = 33h ('3'的ASCII码)
sub al, '9'  ; AL = 33h - 39h = FAh (借位发生)
aas          ; 调整AL为04h, AH -= 1 (AH = FFh)
; 结果: AL = 04h, AH = FFh (表示借位后的结果)
```

**DAA (加法后的十进制调整)**
```assembly
mov al, 59h  ; AL = 59h (59的压缩BCD格式)
add al, 27h  ; AL = 59h + 27h = 80h
daa          ; 调整AL为86h (86的压缩BCD格式)
; 结果: AL = 86h
```

**DAS (减法后的十进制调整)**
```assembly
mov al, 47h  ; AL = 47h (47的压缩BCD格式)
sub al, 59h  ; AL = 47h - 59h = EEh (借位发生)
das          ; 调整AL为88h (88的压缩BCD格式)
; 结果: AL = 88h
```

#### 逻辑指令

![img](https://s2.loli.net/2025/01/14/21jtb5mxlWLsIKk.png)

| 指令  | 示例               | 含义                            |
| ----- | ------------------ | ------------------------------- |
| `AND` | `AND A, B`         | 按位与                          |
| `OR`  | `OR A, B`          | 按位或                          |
| `XOR` | `XOR A, B`         | 异或                            |
| `BT`  | `BT Base, Offset`  | 指定地址的值赋给 CF             |
| `BTC` | `BTC Base, Offset` | 指定地址位的值赋给 CF, 该位取反 |
| `BTR` | `BTR Base, Offset` | 指定地址位的值赋给 CF, 该位设零 |
| `BTS` | `BTS Base, Offset` | 指定地址位的值赋给 CF, 该位设一 |
| `BSF` | `BSF A, B`         | B 最低的 1 是第几位, 赋给 A     |
| `BSR` | `BSR A, B`         | B 最高的 1 是第几位, 赋给 A     |

#### 逻辑偏移

![img](https://s2.loli.net/2025/01/17/SVDghbI2UTnLW8J.png)

| 指令 | 示例             | 含义                                                        |
| ---- | ---------------- | ----------------------------------------------------------- |
| SHL  | `SHL AX, 1`      | 将AX寄存器的内容逻辑左移1位, 空出的位用0填充                |
| SHR  | `SHR BX, 2`      | 将BX寄存器的内容逻辑右移2位, 空出的位用0填充                |
| SAL  | `SAL CX, 1`      | 将CX寄存器的内容算术左移1位, 空出的位用0填充 (与SHL相同 )   |
| SAR  | `SAR DX, 3`      | 将DX寄存器的内容算术右移3位, 空出的位用符号位填充           |
| ROL  | `ROL AL, 1`      | 将AL寄存器的内容循环左移1位, 移出的位重新填充到右侧         |
| ROR  | `ROR BL, 2`      | 将BL寄存器的内容循环右移2位, 移出的位重新填充到左侧         |
| RCL  | `RCL AX, 1`      | 将AX寄存器的内容带进位循环左移1位, 进位标志 (CF) 参与循环   |
| RCR  | `RCR BX, 1`      | 将BX寄存器的内容带进位循环右移1位, 进位标志 (CF) 参与循环   |
| SHLD | `SHLD AX, BX, 4` | 将AX和BX寄存器的内容一起逻辑左移4位, AX的高位由BX的低位填充 |
| SHRD | `SHRD CX, DX, 3` | 将CX和DX寄存器的内容一起逻辑右移3位, CX的低位由DX的高位填充 |

> [!NOTE]
>
> **逻辑右移 (SHR )用0填充空出的高位, 而算术右移 (SAR )用符号位填充空出的高位**

#### 标志位指令

| 指令  | 含义              |
| ----- | ----------------- |
| `CLC` | 进位标志置零      |
| `STC` | 进位标志设一      |
| `CMC` | 进位标志取反      |
| `CLD` | 方向标志置零      |
| `STD` | 方向标志设一      |
| `CLI` | IF 置零, 关闭中断 |
| `STI` | IF 设一, 打开中断 |

#### 分支控制

条件跳转是短跳转, 操作数是一个字节, 允许向后跳转 -128 或向前跳转 +127

无条件跳跃可以跳得更远, 可以直接地址跳转, 允许 +/-32K 的跳转, 甚至允许跳转到AX寄存器！

**常用的一些指令**

| 指令   | 含义             | flag             | 反指令 | 反含义               | 反 flag          |
| ------ | ---------------- | ---------------- | ------ | -------------------- | ---------------- |
| `JA`   | Above            | `ZF=0 and CF=0`  | `JNA`  | Not Above            | `ZF=1 or CF=1`   |
| `JAE`  | Above or Equal   | `CF=0`           | `JNAE` | Not Above or Equal   | `CF=1`           |
| `JB`   | Below            | `CF=1`           | `JNB`  | Not Below            | `CF=0`           |
| `JBE`  | Below or Equal   | `ZF=1 or CF=1`   | `JNBE` | Not Below or Equal   | `ZF=0 and CF=0`  |
| `JC`   | Carry            | `CF=1`           | `JNC`  | Not Carry            | `CF=0`           |
| `JCXZ` | CX is Zero       | `CX=0`           | -      | -                    | -                |
| `JE`   | Equal            | `ZF=1`           | `JNE`  | Not Equal            | `ZF=0`           |
| `JG`   | Greater          | `ZF=0 and SF=OF` | `JNG`  | Not Greater          | `ZF=1 or SF!=OF` |
| `JGE`  | Greater or Equal | `SF = OF`        | `JNGE` | Not Greater or Equal | `SF != OF`       |
| `JL`   | Less             | `SF != OF`       | `JNL`  | Not Less             | `SF = OF`        |
| `JLE`  | Less or Equal    | `ZF=1 or SF!=OF` | `JNLE` | Not Less or Equal    | `ZF=0 and SF=OF` |
| `JO`   | Overflow         | `OF=1`           | `JNO`  | No Overflow          | `OF=0`           |
| `JP`   | Parity           | `PF=1`           | `JNP`  | Not Parity           | `PF=0`           |
| `JPE`  | Parity is Even   | `PF=1`           | `JPO`  | Parity is Odd        | `PF=0`           |
| `JS`   | Signed           | `SF=1`           | `JNS`  | Not Signed           | `SF=0`           |
| `JZ`   | **Zero**         | `ZF=1`           | `JNZ`  | Not Zero             | `ZF=0`           |

#### 循环

主要有三种: 

- `LOOP`, 相当于

  ```c
  do {
      // 循环体代码
      CX--;
  } while (CX != 0);
  ```

- `LOOPZ`, 相当于

  ```c
  do {
      // 循环体代码
      CX--;
  } while (CX != 0 && ZF == 1);
  ```

- `LOOPNZ`, 相当于

  ```c
  do {
      // 循环体代码
      CX--;
  } while (CX != 0 && ZF == 0);
  ```

#### 短延迟

对于如下程序

```assembly
  mov cx, N  ; 消耗 4 时钟周期, 这里 N 是字面量, 但是取值还未确定
tag:
  nop        ; 消耗 3 时钟周期
  nop        ; 消耗 3 时钟周期
  loop tag   ; 消耗 17 个时钟周期, 退出循环时仅 5 个时钟周期
```

总延迟时间的计算公式为: $C = 4 + N \times 23 - 12$

假设需要延迟 1000 个时钟周期, 可以通过以下步骤计算循环次数 \( N \): 

$1000 = 4 + N \times 23 - 12$

解方程得到: 

$N = \frac{1000 - 4 + 12}{23} \approx 43.65$

因此, 设置 \( N = 44 \) 即可实现大约 1000 个时钟周期的延迟

#### 长延迟

考虑如下程序

```assembly
.STARTUP
mov ah,02
mov dl,'S'
int 021h

mov bx, 30000 ;4

back2: 
	mov cx, 30000 ;4
back1: 
	nop ;3
	loop back1

	dec bx
	jnz back2

	mov ah,02
	mov dl,'F'
	int 021h
EXIT
```

延迟计算公式为: 

$C_{T}=C_{0}+N(C_{BK}){-12}$

先计算内循环: 

$\begin{flalign*}
&C_T = C_0 + N(C_{_{BK}}) - 12 \\
&C_T = 4 + 3000(20) - 12 \\
&C_T = 599992
\end{flalign*}$

然后计算外循环: 

$\begin{flalign*}
&C_T = C_0 + N(C_{BK}) - 12 \\
&C_T = 4 + 30000(59992 + 2 + 16) - 12 \\
&C_T = 1.8 \times 10^{10} \text{ Clock cycles}
\end{flalign*}$

实际上程序只花了15s来运行, 计算出来的时钟频率是1200MHz, 是目标机器的时钟频率(300MHz)的4倍,原因是现代处理器使用 **指令并行** 技术

#### 打印数字的方法

基于栈的实现: 

```assembly
.MODEL medium
.STACK
.DATA
ten db 10
.CODE
.STARTUP
mov ax, 12345
call Print
.EXIT

Print:
    push bx        ; 函数调用, 储存原来寄存器的值, 固定操作
    push cx
    push dx
    mov cx, 5      ; 初始化循环计数器为5
    mov bx, 10000

again:
    mov dx, 0h     ; 除法前清空 dx
    div bx         ; dx:ax /= bx
    or al, 030h    ; 数字转 ASCII
    push dx        ; 保存余数
    mov dl, al     ; 传参给 21h 中断
    mov ah, 02h    ; 输出字符模式
    int 021h
    mov dx, 0h     ; 除法前清空 dx
    mov ax, bx     ; bx /= 10
    div ten
    mov bx, ax
    pop ax
    loop again     ; cx自动减1,不为0则跳转
    pop dx         ; 函数调用结束, 恢复原来寄存器的值, 固定操作
    pop cx
    pop bx
    ret

END
```

---

### Lecture 5: Assembly Language (Ⅳ)

#### 打印负数

```assembly
.MODEL medium
.STACK
.DATA
ten word 10
    .CODE
    .STARTUP
    mov ax, 32768
    call Print
    .EXIT
Print:
    push bx
    push cx
    push dx
    mov cx, 5
    mov bx, 10000
    test ax, 8000h
    jz Positive ; 如果是负数,要打印负号,然后取反加一
    push ax
    mov ah, 02h
    mov dl, '-' 
    int 021h
    pop ax
    not ax
    add ax, 1
    jmp Positive
Positive:
    mov dx, 0h
    div bx
    or al, 030h  
    push dx
    mov dl, al
    mov ah, 02h
    int 021h
    mov dx, 0h 
    mov ax, bx
    div ten
    mov bx, ax
    pop ax
    loop Positive
    pop dx
    pop cx
    pop bx
    ret
END
```

#### 字符串

字符串是一组用于描述文本的 ASCII 字符

- 以 NULL byte=0 字符结尾的字符串, `Charles Markham /0`
- 使用第一个字节设置长度的字符串, `/15 Charles Markham`

#### 字符串操作

`LEA`命令: 将有效地址加载到 SI 中, 例如: 

```assembly
msg1 db "Hello, world.$" ; 定义字符串

lea SI, msg1 ; 将 msg1 的地址加载到 SI 中, 这里 SI 寄存器将会存储 msg1 在内存中的起始地址
```

`MOVSB`命令: Move String Byte (移动字符串字节 ), 移动一个字节的数据, 将 DS: SI 指向的内存复制到 ES: DI 中指定的地址, 通常用于从源字符串复制一个字节到目标字符串, 执行 MOVSB 指令后, **SI** 和 **DI** 寄存器的值会自动递增或递减, 如果 DF (Direction Flag) 为 0, SI 和 DI 递增, 如果 DF 为 1, SI 和 DI 递减, 例如: 

```assembly
msg1 db "Hello$"  ; 源字符串
msg2 db "     $"  ; 目标字符串, 预留空间

lea SI, msg1      ; SI 指向 msg1
lea DI, msg2      ; DI 指向 msg2

mov cx, 5         ; 设置循环次数为5,  要复制的字节个数

cld               ; DF寄存器置0

rep movsb         ; 执行 5 次复制
```

`CMPSB`命令: Compare String Byte (比较字符串字节 ), 这条指令会比较 **SI** 寄存器指向的字节和 **DI** 寄存器指向的字节, 并设置相应的标志位 (如 ZF、SF 等 )。例如: 

```assembly
msg1 db "Hello$" ; 第一个字符串
msg2 db "Hello$" ; 第二个字符串

lea SI, msg1     ; SI 指向 msg1
lea DI, msg2     ; DI 指向 msg2

mov cx, 5        ; 设置循环次数为5,  要比较的字节个数

cld              ; DF寄存器置0

rep cmpsb        ; 比较字节
     
jz equal   

jmp not_equal    ; jump if it's not equal

equal:
  ; foo
not_equal:
  ; bar
```

> [!NOTE]
>
> 修饰符 `REP` 可以放在任何字符串指令的前面, 并重复指令 CX 次。Rep 代表重复字符串前缀。

`movsb`,`CMPSB` 是 CISC 的,以下维基百科上关于CISC的介绍: 

> **复杂指令集计算机** (英语: Complex Instruction Set Computer；[缩写](https://zh.wikipedia.org/wiki/縮寫): **CISC** )是一种[微处理器](https://zh.wikipedia.org/wiki/微處理器)[指令集架构](https://zh.wikipedia.org/wiki/指令集架構), 每个指令可执行若干低端操作, 诸如从[存储器](https://zh.wikipedia.org/wiki/電腦記憶體)读取、存储、和[计算](https://zh.wikipedia.org/wiki/計算)操作, 全部集于单一指令之中。与之相对的是[精简指令集](https://zh.wikipedia.org/wiki/精简指令集)。
>
> 复杂指令集的特点是指令数目多而复杂, 每条指令字长并不相等, 电脑必须加以判读, 并为此付出了性能的代价。
>
> 属于复杂指令集的处理器有[CDC 6600](https://zh.wikipedia.org/wiki/CDC_6600)、[System/360](https://zh.wikipedia.org/wiki/System/360)、[VAX](https://zh.wikipedia.org/wiki/VAX)、[PDP-11](https://zh.wikipedia.org/wiki/PDP-11)、[Motorola 68000](https://zh.wikipedia.org/wiki/Motorola_68000)家族、[x86](https://zh.wikipedia.org/wiki/X86)、[AMD Opteron](https://zh.wikipedia.org/wiki/AMD_Opteron)等。

#### CISC和RISC实现乘法

**RISC实现**

```assembly
.STARTUP

mov ax,0
mov dx,100         ;Multiply dl by bl result in ax.
mov bx,123
mov cx,8

back: rcr dx,1     ;move lsb dx into c
      jnc over
      add ax,bx
      
over: shl bx,1     ;multiply bx by 2

      loop back    ;repeat 8 times

call Print
.EXIT
```

**CISC实现**

```assembly
.STARTUP

mov dl,100    ;Multiply dl by bl result in ax.
mov al,123

mul dl        ;ax=dl*al

call Print

.EXIT
```

除法部分就是直接减, 不够了就回退, 略

#### 浮点数

浮点数通过**科学计数法**的形式表示实数, 通常分为三个部分: 

- **符号位 (Sign )**: 表示数的正负。
- **指数位 (Exponent )**: 表示数的规模 (即小数点的位置 )。
-  **尾数位 (Mantissa 或 Fraction )**: 表示数的精度。

![img](https://s2.loli.net/2025/01/17/qo9xS5yJDXslOGp.png)

浮点数的通用表示形式为: 

$\text{Value} = (-1)^{\text{Sign}} \times \text{Mantissa} \times 2^{\text{Exponent}}$

**规格化浮点数**

规格化浮点数是 IEEE 754 标准中最常见的表示形式, 其特点是尾数部分的最高位隐含为 `1` (即尾数的整数部分为 `1` )。

**规格化浮点数的表示**

**尾数 (Mantissa )**: 隐含前导 `1`, 实际存储的是小数部分。

**指数 (Exponent )**: 非全 `0` 且非全 `1` (单精度: 1 到 254, 双精度: 1 到 2046 )。

**公式**: 

$\text{Value} = (-1)^{\text{Sign}} \times 1.\text{Mantissa} \times 2^{\text{Exponent} - \text{Bias}}$

**示例**

单精度浮点数: 
- 符号位: `0` (正数 )

- 指数位: `10000001` (129, 偏移量 127, 实际指数为 2 )

- 尾数位: `10100000000000000000000` (隐含前导 `1`, 实际尾数为 `1.101` )

值: 

$\text{Value} = 1.101_2 \times 2^2 = 110.1_2 = 6.5_{10}$

---

**非规格化浮点数**
非规格化浮点数用于表示非常接近于零的数值, 其特点是尾数部分的最高位为 `0` (即尾数的整数部分为 `0` )。

**非规格化浮点数的表示**

**尾数 (Mantissa )**: 没有隐含前导 `1`, 实际存储的是小数部分。

**指数 (Exponent )**: 全 `0` (单精度: 0, 双精度: 0 )。

**公式**: 

$\text{Value} = (-1)^{\text{Sign}} \times 0.\text{Mantissa} \times 2^{1 - \text{Bias}}$

 **示例**

单精度浮点数: 
- 符号位: `0` (正数 )

- 指数位: `00000000` (0, 偏移量 127, 实际指数为 -126 )

- 尾数位: `00000000000000000000001` (没有隐含前导 `1`, 实际尾数为 `0.00000000000000000000001` )

值: 

$\text{Value} = 0.00000000000000000000001_2 \times 2^{-126} \approx 1.4 \times 10^{-45}$

[视频讲解](https://www.bilibili.com/video/BV1VK4y1f7o6/)

#### 浮点数的计算

浮点数做加减法运算遵循一个原则, 那就是**先对齐, 再计算**。

「对齐」指的是对齐指数位 e。两个浮点数相加时, 如果 e 不一样, 就要先把 e 对齐再做加法运算。如何对齐呢？对齐的原则就是把 e 都统一成其中较大的一个。

比如 0.5 与 0.125 相加, 这两个数表示成浮点数分别是$(-1)^0\times1.0\times2^{-1}$ 和 $(-1)^0\times1.0\times2^{-3}$, 由于 0.5 的指数大于 0.125 的指数, 所以要把 0.125 的指数统一成和 0.5 一样的 -1, 指数增大, 那么有效数位要右移, 因为 f 前面默认有个 1, 所以右移之后, 0.125 的有效数位变成了 0.01, 然后将 0.5 的有效数位与 0.125 的有效数位相加, 结果是 1.01, 最终表示成浮点数就是$(-1)^0\times1.01\times2^{-1}$。

#### 8087 协处理器

> 处理器都有CP了 (╯‵□′)╯︵┻━┻

8087 是一种 **数学协处理器**, 也被称为 **浮点处理器** 或 **数字数据处理器 (Numeric Data Processor, NDP)**。 它不是一个独立的中央处理器 (CPU), 而是被设计用来与 Intel 的 8086、8088 等 CPU 一起工作, 以加速浮点运算。

![img](https://s2.loli.net/2025/01/17/Nqe5dL6AnGW4b9l.png)

**状态字组**

![img](https://s2.loli.net/2025/01/17/9kFJtIMY6uq3oA7.png)

**控制字组**

![img](https://s2.loli.net/2025/01/17/Morvu9qm1d6ZICk.png)

**栈**

8087 还自带了一个栈, 栈当中每个元素都是 10 字节, 栈始终有 8 个位置。
每次压入新数据到栈当中, 栈底数据被覆盖, 就和移位运算差不多
在 MASM 汇编代码当中, `ST(0)` 始终表示栈顶, `ST(1~7)` 表示栈中其他元素。

![img](https://s2.loli.net/2025/01/17/cXJCY3xZ6r4gRNV.png)

**8087 指令**

- `FADD S1/D, S2` 表示把两个 S 进行加法运算, 结果存入 D (S1=D )。如果没有指定两个 S, 那么就相当于 `ST(0) += ST(1)`
- `FSUB S1/D, S2` 相当于执行 `S1 -= S2`
- `FSUBR S1/D, S2` 与上面相反, 相当于 `S1 = S2 - S1`
- 此外还有 `FMUL`, `FDIV`, `FMULP`, `FIMUL`, `FDIVR`, `FDIP`, `FIDIV` 等

---

### Lecture 6: Assembly Language (V)

#### 浮点数计算 —— 毕达哥拉斯问题

<img src="https://s2.loli.net/2025/01/18/yO3klJvp1MThsYD.png" alt="image-20250118下午94629825"  />

使用 FP 处理器  (8087 ) 执行上述计算

```assembly
.8087                                ; 告诉 MASM 协处理器存在
.MODEL medium
.STACK
.DATA

SX dd 5.0                            ; 定义短实数 (4 字节 ), 初始值为 5.0
SY dd 12.0                           ; 定义短实数 (4 字节 ), 初始值为 12.0
HY dd 0.0                            ; 定义短实数 (4 字节 ), 用于存储结果
cntrl dw 03FFh                       ; 定义控制字, 用于设置 8087 协处理器的状态
stat dw 0                            ; 定义状态字, 用于存储 FPU 的状态

.CODE
.STARTUP

FINIT                                ; 初始化 FPU, 将其设置为默认状态
FLDCW cntrl                          ; 加载控制字, 设置舍入模式为偶数, 并屏蔽中断

FLD SX                               ; 将 SX 压入 FPU 栈
FMUL ST, ST(0)                       ; 将栈顶元素与自身相乘, 结果存储在栈顶
FLD SY                               ; 将 SY 压入 FPU 栈
FMUL ST, ST(0)                       ; 将栈顶元素与自身相乘, 结果存储在栈顶
FADD                                 ; 将栈顶的两个数相加
FSQRT                                ; 计算栈顶元素的平方根
FSTSW stat                           ; 将 FPU 的状态字加载到 [stat]
mov ax, stat                         ; 将 [stat] 复制到 AX
and al, 0BFh                         ; 检查所有 6 个状态位
jnz pass                             ; 如果有任何位被设置, 则跳转到 pass
FSTP HY                              ; 将栈顶的结果存储到 HY
jmp print                            ; 跳转到打印函数

print:
    mov bx, OFFSET HY                ; 将 HY 的地址加载到 BX 寄存器
    mov ax, [bx+2]                   ; 将 HY+2 的值加载到 AX 寄存器
    mov cx, 16                       ; 设置循环次数为 16
    call print_num                  
    mov ax, [bx]                     ; 将 HY 的值加载到 AX 寄存器
    mov cx, 16
    call print_num
    jmp pass

print_num:
    push bx                          ; 存储 BX 寄存器
    rol ax, 1                        ; 将 AX 寄存器左移一位
    jc set                           ; 如果 ZF=1 , 则 DL='1'
    mov dl, '0'                      ; DL='0'
    jmp over

set:
    mov dl, '1'

over:
    push ax                          ; 存储 AX 寄存器
    mov ah, 02h
    int 21h
    pop ax                           ; 恢复 AX 寄存器
    loop print_num
    pop bx                           ; 恢复 BX 寄存器
    ret

pass: 
    nop

; 程序结束
mov ah, 4Ch        ; 设置 AH 为 4Ch (DOS 功能调用: 程序退出 )
int 21h

END
```

`HY`在内存中的排列: 

![img](https://s2.loli.net/2025/01/18/UHmLhaO6S5Bqesb.png)

> 汇编的内容终于结束了 ~\(≧▽≦)/~

------

### Lecture 7: Semiconductors

#### 能级

原子和固体能级的区别: 

![img](https://s2.loli.net/2025/01/19/m3t47LFRE5oKbPX.png)

> 在原子中, 电子围绕着原子核运动, 并占据着一定的能级。原子的能级结构则直接决定了原子的化学性质和物理性质。原子的能级结构又与能带的性质密切相关, 因此能带和原子能级是密切相关的。
>
> 能带是固体物质中电子能量的区间。在一个固体中, 电子不再局限于单个原子, 而是能够在整个固体中自由移动, 因此它们的能量是连续的, 可以形成一段能量区间。能带的性质则取决于原子间的相互作用、晶体结构等因素。

![img](https://s2.loli.net/2025/01/19/JuPEMSqH18OAnl6.png)

- 绝缘体需要大量的能量才能使电子进入导带
- 导体需要很少的能量
- 半导体需要大约1eV

#### P-type Silicon, N-type Silicon

P型硅掺入硼, 空穴导电

![img](https://s2.loli.net/2025/01/19/p4xkj8gN6bMmHPV.png)

N型硅掺入磷, 电子导电

![img](https://s2.loli.net/2025/01/19/JgZ4YMKTH6GRmku.png)

![img](https://s2.loli.net/2025/01/19/2mHBKhcOuLRwJ8U.png)

#### 二极管

在 P-type Silicon, N-type Silicon 硅的交汇处, 电子和空穴穿过结部移动并结合。这会产生一个称为耗尽区的非导电区域, 于是就会形成 PN 结

![img](https://s2.loli.net/2025/01/19/pmWTBIUyuhcnfQE.png)

正向偏置 PN 结二极管: 正极排斥空穴, 负极吸引电子, **耗尽区消失, 电流流过电路**

![img](https://s2.loli.net/2025/01/19/zNbQdSlADr8f5FW.png)

反向偏置 PN 结二极管: 正极端子吸引空穴, 负极端子排斥电子, **耗尽区变大, 没有电流流过电路**

![img](https://s2.loli.net/2025/01/19/KnLS6QTxwrVA4ED.png)

故电子的流动方向是 **N-type Silicon -> P-type Silicon**, 导电方向是 **P -> N**

**二极管的伏安曲线**

![img](https://s2.loli.net/2025/01/19/A1KgNmDIkcO52WG.png)

**二极管的用途**

- 整流: 将交流电转换为直流电
- 电路保护: 防止损坏过电压或极性错误
- 逻辑: 搭建逻辑门

---

### Lecture 8: Transistors and FETS

#### 结型晶体管

下图是一个NPN 类型的结型晶体管 (俗称三极管) , 由三部分构成发射极 (emitter) , 基极 (base) , 集电极 (collector) , 是一种用电流控制电流的半导体器件, 就像一个小阀门：

- **输入**：一个小电流 (基极电流, I<sub>B</sub>) 
- **输出**：一个大电流（集电极电流, I<sub>C</sub>) 

![img](https://s2.loli.net/2025/01/19/xFAEpb9w8lIi2jU.png)

**电流增益**

BJT的电流增益用符号 **β**（或 h<sub>FE</sub>) 表示, 公式是：

$\beta=\frac{I_C}{I_B}$

- **I<sub>C</sub>**：集电极电流（输出电流) 。

- **I<sub>B</sub>**：基极电流（输入电流) 。

- **β**：电流增益, 通常范围是 **20 到 200**, 甚至更高。

例如:

- 基极电流 I<sub>B</sub> = 1 mA。

- 电流增益 β = 100。

那么集电极电流 I<sub>C</sub> 就是：

$I_C=\beta\times I_B=100\times1\text{ mA}=100\text{ mA}$

**1 mA 的输入电流** 控制了 **100 mA 的输出电流**, 这就是电流增益的作用

**使用三极管实现NOR门**

当且仅当 I<sub>A</sub> = I<sub>B</sub> = 0 时, 此时三极管相当于一个大电阻。于是电流只能流向 Output, 若 I<sub>A</sub> + I<sub>B</sub> ≠ 0, 此时输出线被短路, 电流全部流向 I<sub>E</sub>

![img](https://s2.loli.net/2025/01/19/ZjXD8wz2sflk1mQ.png)

#### MOSFET

MOS FET由以下几部分组成：

- **栅极（Gate, G) **：金属层, 通过绝缘层（通常是二氧化硅) 与半导体隔离。
- **源极（Source, S) **：电流的入口。
- **漏极（Drain, D) **：电流的出口。
- **衬底（Body, B) **：通常是硅材料, 与源极或漏极连接。

![img](https://s2.loli.net/2025/01/19/CvHbphekSDg5JRy.png)

更好的例子:

如图, 以下是一个**NMOS**, 这时候我们给这个结构通电. 就会有大量的电子被吸引到这片区域, 在填充空穴的同时还会多出很多自由电子, 达成平衡后, 在这片区域的下方也会因为扩散作用产生新的耗尽层, 这个区域叫做**N沟道**, 电路就被导通了, 这个时候我们就得到了一个电压控制的开关

![img](https://s2.loli.net/2025/01/19/H4j15LMIwV6UeWT.png)

这部分比较抽象了, 建议看这个[视频](https://www.bilibili.com/video/BV1nL411x7jH/)

#### CMOS

- 输入高电平时, NMOS 导通, PMOS 截止, 输出低电平
- 输入低电平时, PMOS 导通, NMOS 截止, 输出高电平

![img](https://s2.loli.net/2025/01/19/xBEcbQXG4RDseWP.png)

#### 硅的制造

应该不重要, 略

---

### Lecture 9: Digital I/O

#### I/O

8086 微处理器使用 20 位地址总线进行内存读写，并支持 16 位的 I/O 地址空间, 为了实现内存和 I/O 操作的区分，CPU 通过一条额外的控制线来选择是进行内存访问还是 I/O 访问

**I/O 地址空间**

- I/O 空间中的位置被称为端口
- 8086 的 I/O 地址空间为 16 位，可以映射为 64K 的 8 位端口 （字节） 或 32K 的 16 位端口 （字）
- 与控制内存相比，控制 I/O 端口的指令数量较少
- 某些硬件设备 （如屏幕） 被映射到内存空间，而不是 I/O 空间

**常见的 I/O 地址**

| **地址**  | **名称**               | **方向** | **用途**                                                     |
| --------- | ---------------------- | :------- | :----------------------------------------------------------- |
| **0x378** | Parallel Printer Latch | 输出     | 并行打印机数据端口，通常用于 LPT1 (Line Printer 1) , 向打印机发送数据 |
| **0x37A** | Printer Control Latch  | 输出     | 并行打印机控制端口，通常用于 LPT1, 控制打印机的操作 （如初始化，选择打印机等） |
| **0x379** | Printer Status         | 输入     | 并行打印机状态端口，通常用于 LPT1, 读取打印机的状态信息 （如是否忙碌，是否有纸等） |
| **0x3D9** | VDU Colour Register    | 输出     | 视频显示单元 (VDU) 颜色寄存器，用于设置 DOS 文本模式下的边框颜色 |
| **0x278** | Parallel Printer Latch | 输出     | 并行打印机数据端口，通常用于 LPT2 (Line Printer 2) , 向打印机发送数据 |

**总线共享**

由于 8086 硬件引脚的局限性，内存总线和数据总线共享相同的引脚, 因此，需要一条额外的控制线来区分是访问内存还是 I/O 数据

**内存访问周期**

8086 需要 **4 个时钟周期**来完成一次内存访问：

1. **第 1 个周期**：发送地址
2. **第 2-3 个周期**：等待内存响应和数据传输
3. **第 4 个周期**：结束周期, 

#### Z80A CPU 架构

相比 8086, Z80A 的数据总线和地址总线是分开的

![img](https://s2.loli.net/2025/01/19/PXrtv54x8d3UAD2.png)

一个 **AND 门** 作为地址解码器，当 16 个输入与设备地址匹配时输出 **真**, 否则输出 **假**, 两根控制线 （绿色，紫色） 指示是否对该设备进行操作

![img](https://s2.loli.net/2025/01/19/oKC2ryEbsckfAG1.jpg)

三个值 （地址匹配结果和两根控制线） 通过 **AND 门** 组合成一个控制信号，传递给 **三态缓冲器** （具有三种输出状态：高电平 (1) , 低电平 (0) , 高阻态 (High-Z)  , 三态缓冲器根据控制信号决定将输入直接传输到输出，还是切换断开连接

![img](https://s2.loli.net/2023/05/23/QC4m9yvVDl1XNYr.png)

对于输出型号，就是三态缓冲器换成了 D 触发器

![img](https://s2.loli.net/2025/01/19/5QW1Opjd7wDyT6U.jpg)

#### 汇编的 I/O

**OUT 指令**

**OUT** 指令用于将数据从 CPU 的寄存器 （通常是累加器，如 `AL`, `AX` 或 `EAX`) 写入指定的 I/O 端口

```assembly
OUT port, acc
```

- **port**：I/O 端口地址
- **acc**：累加器 (`AL`, `AX` 或 `EAX`) , 存储要写入的数据

**两种模式**

- **立即数模式**：
  端口地址直接指定为立即数 (0-255) , 只能访问 256 个端口

   ```assembly
  OUT AL, 30h  ; 将 AL 中的数据写入端口 30h
   ```

- **DX 寄存器模式**：
  端口地址存储在 `DX` 寄存器中，可以访问 64K 个端口 (0-65535)

  ```assembly
  OUT DX, AX   ; 将 AX 中的数据写入 DX 指定的端口
  ```

**IN 指令**

**IN** 指令用于从指定的 I/O 端口读取数据到 CPU 的寄存器 （通常是累加器，如 `AL`, `AX` 或 `EAX`)

```assembly
IN acc, port
```

- **acc**：累加器 (`AL`, `AX` 或 `EAX`) , 用于存储从端口读取的数据
- **port**：I/O 端口地址

**两种模式**

- **立即数模式**：
  端口地址直接指定为立即数 (0-255) , 只能访问 256 个端口

  ```assembly
  IN AL, 30h  ; 从端口 30h 读取 8 位数据到 AL
  ```

- **DX 寄存器模式**：
  端口地址存储在 `DX` 寄存器中，可以访问 64K 个端口 (0-65535)

  ```assembly
  IN AX, DX   ; 从 DX 指定的端口读取 16 位数据到 AX
  ```

> [!NOTE]
>
> **IOPL** (I/O Privilege Level, I/O 特权级） 是 x86 架构中用于控制 **I/O 端口访问权限** 的机制, 它存储在 **EFLAGS 寄存器** 的第 12 和 13 位，定义了执行 I/O 指令 （如 `IN`, `OUT`) 所需的最低特权级
>
> IOPL 是一个 2 位的值，取值范围为 0 到 3：
>
> - **当 CPL ≤ IOPL 时**：程序可以直接执行 I/O 指令 （如 `IN`, `OUT`)
> - **当 CPL > IOPL 时**：程序无法直接执行 I/O 指令, 如果尝试执行，会触发 **一般保护异常** (General Protection Fault, #GP)

#### 中断

想象一个场景：CPU 需要从 HDD 读取数据，但等待 HDD 响应需要时间 （例如移动磁头和旋转盘片，通常是毫秒级） , 如果 CPU 采用轮询方案，会造成大量计算资源的浪费, 此时，可以考虑使用中断机制, 当 HDD 就绪时，它会发出中断信号，CPU 从低功耗模式恢复，然后进行数据访问操作

**中断优先级：** 中断服务例程可以嵌套，编号越小的 ISR 优先级越高

**当中断发生的时候：**

1. 暂停主程序的执行
2. 调用一个服务中断的程序，称为**中断处理程序 (interrupt handler)**
3. 将控制权返回到主程序

**8086 的三种中断类型：**

- **硬件中断**: 外部信号施加到处理器的 INTR （中断） 引脚或 NMI （非可屏蔽中断） 引脚时引起的中断
- **异常中断**: 由内部错误触发，例如除以零，通常用于打印错误信息
- **软件中断**: 由执行汇编语言 INT 指令引起, 简单来说，就是调用 BIOS 中的一个函数

#### **时间片轮询调度 VS 抢占式调度**

**时间片轮询调度  (Time Slice Scheduling)**：

- 操作系统按固定时间片（如 20ms）轮流执行任务, 
- CPU 主动轮询硬件，适合简单多任务系统，但可能浪费资源, 

**抢占式调度 (Pre-emptive Scheduling)**：

- 高优先级任务可以中断低优先级任务，确保重要任务优先执行, 
- 硬件通过中断通知 CPU，响应速度快，适合实时系统, 

#### 中断向量表

**中断向量表 (Interrupt Vector Table, IVT) **是计算机系统中用于管理和处理中断的关键数据结构, 它包含了**中断服务例程 (Interrupt Service Routine, ISR) **的入口地址, 当中断发生时，CPU 会根据中断号在中断向量表中查找相应的入口地址，并跳转到该地址执行中断处理程序

中断向量表通常位于 RAM 的**前 1024 字节** （地址范围：0000:0000 到 0000:03FF) , 每个中断向量由 4 个字节组成，其中 **2 个字节用于代码段 (CS) **, 另外 **2 个字节用于指令指针 (IP) **

假设中断号为 `0x21`：

- 中断向量表的位置为：`0x0000:0x0084` (`0x21 * 4 = 0x84`)
- 如果 `0x0084` 处存储的值为 `0x1234:0x5678`, 则中断处理程序的入口地址为 `0x1234:0x5678`

**中断向量表**

![img](https://s2.loli.net/2025/01/20/TXYK9F5cGUJI2a1.jpg)

#### 中断控制器

8259A 是一种优先级中断控制器, 当设备的 IRQ 线被触发时，中断编号会通过 PC 总线传输, 系统随后查找中断向量表，并跳转到相应的向量地址执行中断处理程序, 

8259A #1 负责处理中断 0~7，而 8259A #2 负责处理中断 8~15, 从芯片（8259A #2）通过 IRQ2 引脚连接到主芯片（8259A #1）, 

8259A #1 的基址为 20H，8259A #2 的基址为 A0H, 

具体中断映射如下：

- **8259A #1:** IRQ0 = INT 08H, IRQ1 = INT 09H, …, IRQ7 = INT 0FH
- **8259A #2:** IRQ8 = INT 70H, IRQ9 = INT 71H, …, IRQ15 = INT 77H

![img](https://s2.loli.net/2025/01/20/6EnZtBbpJmSFOA7.png)

下表从 **INT 8** 开始排序

| **IRQ** | **Description**        | **IRQ** | **Description**          |
| ------- | ---------------------- | ------- | ------------------------ |
| 0       | Timer Tick             | 8       | Real-Time Clock (RTC)    |
| 1       | Keyboard               | 9       | Available (Legacy: IRQ2) |
| 2       | Second 8259A           | 10      | Available                |
| 3       | COM2 (Serial Port 2)   | 11      | Available                |
| 4       | COM1 (Serial Port 1)   | 12      | PS/2 Mouse               |
| 5       | Sound Card / LPT2      | 13      | Math Coprocessor         |
| 6       | Floppy Disk Controller | 14      | Primary IDE Controller   |
| 7       | LPT1 (Parallel Port)   | 15      | Secondary IDE Controller |

> [!NOTE]
>
> INT 0-7 不受 8259 控制，用于处理 **异常** 和 **硬件中断**

#### CPU 处理中断的流程

1. **中断触发：** 外部设备或内部异常触发中断请求（IRQ），将中断信号发送到 CPU, 

2. **中断响应：** CPU 在当前指令执行完成后检测到中断请求，并发出中断响应信号（INTA）, 

3. **保存现场：** CPU 将当前程序状态（包括程序计数器 PC、标志寄存器 FLAGS 等）压入栈中，以便中断处理完成后恢复执行, 

4. **获取中断向量：** CPU 从中断控制器（如 8259A）获取中断号，并根据中断号查找中断向量表（IVT），找到对应的中断服务例程（ISR）入口地址, 

5. **跳转到 ISR:** CPU 跳转到中断服务例程的入口地址，开始执行中断处理程序, 

6. **执行中断处理：** CPU 运行中断服务例程，完成设备或异常的具体处理逻辑, 

7. **恢复现场：** 中断处理完成后，CPU 从栈中恢复之前保存的程序状态（包括 PC 和 FLAGS）, 

8. **返回原程序：** CPU 继续执行被中断的程序，从断点处恢复运行, 

#### 8259 操作命令词

**端口 21H** 是 **8259A 可编程中断控制器（PIC）** 的 **中断屏蔽寄存器（IMR）** 的端口地址, 向该端口写入数据可以设置或清除中断屏蔽位，从而控制哪些中断请求（IRQ）被允许或禁止, 值 **137（89H）** 的二进制形式为 **10001001**，表示屏蔽 IRQ 7, 3, 1

![image-20250120下午35508105](https://s2.loli.net/2025/01/20/iEPpwNxROh4GHc6.png)

```assembly
mov al,137
mov dx,21h		b   ; 中断屏蔽寄存器 (IMR) 的端口地址
out dx,AL
```

#### 中断后重置

当调用中断时，中断控制器会记录该中断的活动状态及其优先级。在中断处理完成后，必须通知控制器中断已结束。这是通过在 **IRET** 指令之前，向中断控制器发送一个 **非特定的中断结束（EOI，End of Interrupt）** 命令来实现的。

```assembly
EOI:
    mov al, 20h      ; EOI 命令
    out 20h, al      ; 发送到 8259A 的主控制器
```

#### 自定义 ISR

**自定义 ISR** 是程序员自己编写的中断处理程序，用于替代默认的 ISR, 比如 int 08h，每隔 50ms 左右就会自动执行一次， 可以用这个来实现计数器

```assembly
.MODEL small
.STACK 100h
.DATA
    msg DB '食我压路机啦！！！！$'
    tick_count DW 0
    
.CODE
start:
    mov ax, @data
    mov ds, ax

    ; 保存原始中断向量
    cli
    mov ax, 3508h           
    int 21h
    mov old_int8_offset, bx
    mov old_int8_segment, es

    ; 设置新的中断向量
    push ds
    mov ax, 2508h           
    mov dx, offset new_int8
    push cs
    pop ds
    int 21h
    pop ds
    sti

wait_loop:
    cmp tick_count, 126
    jl wait_loop

    ; 显示消息
    mov ah, 09h
    lea dx, msg
    int 21h

    ; 恢复原始中断向量
    cli
    push ds
    mov ax, 2508h
    mov dx, old_int8_offset
    mov ds, old_int8_segment
    int 21h
    pop ds
    sti

    ; 退出程序
    mov ax, 4c00h
    int 21h

new_int8 PROC FAR
    pushf
    call dword ptr cs:old_int8_offset
    inc tick_count
    iret
new_int8 ENDP

old_int8_offset DW ?
old_int8_segment DW ?

END start
```

#### 直接访问屏幕内存

DOS 屏幕左上角的起始地址为 B800:0000, 每个显示位置占用 2 字节内存，DOS 屏幕宽度为 80 个字符，高度为 25 行，整个屏幕可显示 2000 个字符，共占用 4000 字节内存

![img](https://s2.loli.net/2025/01/20/6aKeHzGnytwgx3Q.png)

**属性字节** (Attribute Byte) 的结构分为两部分：

- **背景色 (Background) **：
  - **位 7**：F (Flash) , 控制字符是否闪烁
  - **位 6-4**：R (Red) , G (Green) , B (Blue) , 控制背景颜色

- **前景色 (Foreground) **：
  - **位 3**：I (Intensity) , 控制前景色的亮度 （高亮或普通）
  - **位 2-0**：R (Red) , G (Green) , B (Blue) , 控制前景颜色

![img](https://s2.loli.net/2025/01/20/4ypTE8rYaFnU523.jpg)

#### TSR

**TSR（Terminate and Stay Resident）** 是一种在 DOS 系统中使用的程序类型，能够在主程序结束后继续驻留在内存中，以便在需要时快速调用。它通常用于实现后台任务或快速访问功能，比如弹出式计算器、剪贴板工具或系统监控程序。

```assembly
; 伪代码：检测热键 Ctrl+Alt+X
check_hotkey:
    mov ah, 02h       ; 读取键盘状态
    int 16h           ; 调用 BIOS 键盘中断
    and al, 00001111b ; 检查 Ctrl 和 Alt 键
    cmp al, 00001100b ; Ctrl+Alt 是否按下
    jne no_hotkey     ; 如果不是，跳过

    ; 检测 X 键
    mov ah, 00h       ; 读取键盘输入
    int 16h
    cmp al, 'x'       ; 是否是 X 键
    je hotkey_pressed ; 如果是，跳转到热键处理程序
no_hotkey:
    ret
hotkey_pressed:
    ; 执行 TSR 程序的功能
    ret
```

---

### Lecture10: MASM Code for Interrupts

