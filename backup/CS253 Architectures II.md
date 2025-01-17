## CS253 Architectures II

### Lecture 1: CPU

计算机信号分为**模拟信号**和**数字信号**

#### 计算机架构

计算机有两种主要类型：

**冯诺伊曼架构**和**Harvard架构**

![image-20250113150019146](https://s2.loli.net/2025/01/13/sJDwESPr8o4dnvm.png)

冯诺依曼结构的处理器使用**同一个存储器，经由同一个总线传输**

> 现代高性能CPU芯片在设计上包含了哈佛和冯诺依曼结构的特点。特别是，“拆分缓存”这种改进型的哈佛架构版本是很常见的。  CPU的缓存分为指令缓存和数据缓存。CPU访问缓存时使用哈佛体系结构。然而当高速缓存未命中时，数据从主存储器中检索，却并不分为独立的指令和数据部分，虽然它有独立的内存控制器用于访问RAM，ROM和（NOR）闪存。 因此，在一些情况下可以看到冯诺依曼架构，比如当数据和代码通过相同的内存控制器时，这种硬件通过哈佛架构在缓存访问或至少主内存访问方面提高了执行效率。 此外，在写非缓存区之后，CPU经常拥有写缓存使CPU可以继续执行。当指令被CPU当作数据写入，且软件必须确保在试图执行这些刚写入的指令之前，高速缓存（指令和数据）和写缓存是同步的，这时冯诺依曼结构的内存特点就出现了。

#### 8086的硬件组成

![image-20250113154827835](https://s2.loli.net/2025/01/13/m2kdoTtbw8MYcWz.png)

**BIU：总线接口单元**
BIU发送地址，从内存中获取指令，并对端口和内存进行读写操作

**EU：执行单元**
EU指示BIU从哪里获取指令，它解码指令并执行指令
EU包含ALU和控制电路

**指令周期 (*instruction cycle*)**就是 fetch-decode-execute 的过程通常一个指令大概占用 4 个指令周期，所以一个 1GHz 的处理器，一秒内大约可以执行 2.5 亿行汇编代码

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
- **shift 16-bit binary numbers**: 移位（16位二进制数）  

![image-20250113155637195](https://s2.loli.net/2025/01/13/jqoGxpcAhRwQDuS.png)

左移右移的实现方法:

![image-20250113160040331](https://s2.loli.net/2025/01/13/jq8DOK7XleVby6m.png)

---

### Lecture 2: Assembly Language (Ⅰ)

#### 寄存器们

**通用寄存器**

8086 有 8 个通用寄存器，可以将它们视为 8 个变量，某些指令可以成对使用 registers，从而提供 16 位操作，当用作寄存器对时，它们被赋予集体名称 AX、BX、CX、DX

![image-20250113160807554](https://s2.loli.net/2025/01/13/6XusCizPvyElda5.png)

**标志位寄存器**

8086 在特殊的 16 位标志寄存器中跟踪某些计算的结果

- **U: Undefined (未定义)**  
- **OF: Overflow flag (溢出标志)**  
- **DF: String direction flag (字符串方向标志)**  
- **IF: Interrupt enable flag (中断启用标志)**  
- **TF: Single step trap flag (单步陷阱标志)**  
- **SF: Sign flag (符号标志，结果的最高有效位)**  
- **ZF: Zero flag, set if result=0 (零标志，如果结果为零则设置)**  
- **AF: BCD Carry flag (BCD 进位标志)**  
- **PF: Parity flag (奇偶校验标志)**  
- **CF: Carry flag (进位标志)**  

![image-20250113164111767](https://s2.loli.net/2025/01/13/gKDLaGo7bkx8ApV.png)

#### 8086的分段内存模型

因为8086的寄存器只有16位，为了让它能访问20位的地址，需要使用CS 寄存器给出代码段地址，IP 寄存器给出偏移距离，然后计算出指令的内存地址位置

![image-20250113165505161](https://s2.loli.net/2025/01/13/jVTmYHvgo5yWqn4.png)

类似的，这些段寄存器也都是为了使用8086的分段内存模型

- **DS (Data Segment Register):** 数据段寄存器

  指向程序的数据所在的内存段，DS 寄存器存储程序数据段的起始地址访问数据时，需要指定一个偏移量，指明数据在数据段内的位置，通过`DS:偏移量`配合工作

  **偏移量的来源:**

  - **直接寻址:** 偏移量可以是指令中直接给出的一个常量例如 mov ax, [0x1234]，这里 0x1234 是一个偏移量
  - **寄存器寻址:** 偏移量可以使用通用寄存器 (例如 BX, SI, DI) 例如 mov ax, [bx]，这里 bx 存储偏移量
  - **寄存器 + 常量：** 偏移量可以是寄存器值 + 常量例如 mov ax, [bx+0x10]，这里 bx 存储偏移量，0x10 是常量

- **SS (Stack Segment Register):** 堆栈段寄存器

  指向堆栈所在的内存段，SS 寄存器存储堆栈段的起始地址

  **SP 寄存器**指向当前栈顶的地址它始终指向栈中最后一个被压入 (pushed) 的值的位置

  **BP 寄存器**通常指向当前栈帧的基地址，主要用途是：

  - 在函数调用过程中，BP 作为访问函数局部变量、函数参数的基址
  - 方便函数内部访问栈上的数据
  - 可以在函数返回时恢复栈帧

- **ES (Extra Segment Register):** 附加段寄存器

  用于字符串操作的额外数据段，通常作为目标段使用，通过`ES:DI`配合工作

#### MASM 程序结构

**程序结构**

![image-20250113174933390](https://s2.loli.net/2025/01/13/upM8tPTJZV7G6Ys.png)

**编译过程**

![image-20250113175235627](https://s2.loli.net/2025/01/13/KgnFof1tA2mGOVy.png)

**运算符和操作数**

![image-20250113175349702](https://s2.loli.net/2025/01/13/xihBSNqcRGupv5V.png)

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
lea bx,msg1                     ; 获得msg1的偏移地址，在这个情况下(DS<<4+BX)就是实际的存储msg1的地址

back:
    mov dl,[bx]                 ; 间接寻址，获取bx寄存器对应的内存地址的第一个值到dx寄存器
    cmp dl,'$'                  ; 将 dl 寄存器中的字符与字符 $ 进行比较
    jz done                     ; 如果 dl 寄存器中的字符和$相等（即 ZF 标志位为 1），则跳转到done执行

    mov ah,02h                  ; 设置 DOS 中断 21h 的功能号为 02h，表示调用显示字符的功能
    int 21h                     ; 调用 DOS 中断 21h，将 dl 寄存器中的字符显示在屏幕上

    inc bx                      ; 将 bx 寄存器的值加 1，指向字符串 msg1 的下一个字符
    jmp back                    ; 无条件跳转到 back 标签处

done:
    nop                         ; 空操作指令

.EXIT

END
```

**常用 21h 功能号**

- **01h:** 从键盘读取一个字符，并将字符存入 AL 寄存器
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
运算数以 **字面量** 形式写在指令里面，如 `mov ax, 10`，这里的运算数也称作 *立即数*

**寄存器寻址**
指运算数保存在某个通用寄存器当中，如 `mov ax, bx`
寄存器的访问是在 CPU 内部的，非常非常快，不需要寻址

**直接寻址**
比如 `mov ax, Count`，就把 data 段当中的变量 `Count` 作为操作数
实际上，变量 `Count` 在汇编器的眼里，只不过是对应数据所在的地址罢了所以相当于把 `Count` 所在地址的值赋给 `ax`
如果要指定其他的段，可以写作 `mov ax, ES:Count`，即表示在额外段上的内容

**寄存器间接寻址**
相对于直接寻址（把偏移地址直接以字面量的形式写在指令当中），寄存器间接寻址是 **把偏移地址存在寄存器（通常是索引寄存器 BX，BP，SI 或 DI）当中**如果是 BP，那对应的段就是栈段，否则就是数据段
这种寻址方式的写法，跟高级语言当中的数组比较类似：

- `mov ax, [bx]` 表示 `ax = array[bx]`
- `mov [bx], ax` 表示 `array[bx] = ax`

#### 8086 指令格式

![image-20250113220000605](https://s2.loli.net/2025/01/13/ENAvqQBwh7eMtfO.png)

**Byte 1：**

- **Opcode (操作码)：** 决定指令的动作（如 MOV）
- **D (方向)：** 数据传输方向，源到目标，还是目标到源

**Byte 2：**

- **W (字/字节)：** 数据大小，16 位字还是 8 位字节
- **Mod (寻址模式)：** 如何确定操作数地址
- **Reg (寄存器)：** 指示一个寄存器
- **R/M (寄存器/内存)：** 指示另一个操作数是寄存器还是内存

**Low Byte/High Byte：** 可选，如果指令需要，用来存放立即数或内存地址偏移量

#### 8086寄存器编号

![img](https://s2.loli.net/2023/04/06/oshgKL6aU9YIAEW.png)

#### 8086寻址模式

![image-20250113221258650](https://s2.loli.net/2025/01/13/cSqZUoIT2Of1tY4.png)

**Mod=00**： **没有偏移量**，或者仅仅是使用寄存器进行内存间接寻址

**Mod=01**： **8 位偏移量** (d8)， 需要额外的 1 个字节来存储偏移量

**Mod=10**： **16 位偏移量** (d16)， 需要额外的 2 个字节来存储偏移量

**Mod=11**： **寄存器寻址**，直接使用寄存器作为操作数，不涉及内存访问

**例如**

`mov SP, BX` 的二进制指令是：

| opcode | D           | W    | Mod            | Reg   | R/M   |
| ------ | ----------- | ---- | -------------- | ----- | ----- |
| 100010 | 1           | 1    | 11             | 100   | 011   |
| `mov`  | to register | word | 寄存器寻址模式 | to SP | to BX |

---

### Lecture 4: Assembly Language (Ⅲ)

#### 算数运算命令

| **指令** | **代码**     | **作用**                                             |
| -------- | ------------ | ---------------------------------------------------- |
| **ADD**  | `ADD AX, BX` | 加法运算，将 AX 和 BX 相加，结果存入 AX              |
| **ADC**  | `ADC AX, BX` | 带进位的加法运算，将 AX, BX, CF 相加，结果存入 AX    |
| **SUB**  | `SUB AX, BX` | 减法运算，将 AX 减去 BX，结果存入 AX                 |
| **MUL**  | `MUL BX`     | 无符号乘法，将 AX 和 BX 相乘，结果存入 DX:AX         |
| **IMUL** | `IMUL BX`    | 有符号乘法，将 AX 和 BX 相乘，结果存入 DX:AX         |
| **DIV**  | `DIV BX`     | 无符号除法，将 DX:AX 除以 BX，商存入 AX，余数存入 DX |
| **IDIV** | `IDIV BX`    | 有符号除法，将 DX:AX 除以 BX，商存入 AX，余数存入 DX |
| **INC**  | `INC AX`     | 自增运算，将 AX 的值加 1                             |
| **DEC**  | `DEC AX`     | 自减运算，将 AX 的值减 1                             |
| **NEG**  | `NEG AX`     | 取负运算，将 AX 的值取负（相当于 `0 - AX`）          |
| **CMP**  | `CMP AX, BX` | 比较运算，比较 AX 和 BX 的值，结果影响标志寄存器(ZF) |
| **CBW**  | `CBW`        | 将 AL 符号扩展到 AH（字节到字）                      |
| **CWD**  | `CWD`        | 将 AX 符号扩展到 DX（字到双字）                      |

> [!CAUTION]
>
> `DIV` 与 `IDIV`在除数是word(16bit)的时候，被除数是 32 位的 `DX:AX`,`DX`的值可能会产生意想不到的结果
>
> `MUL` 与 `IMUL`在乘数是word(16bit)的时候，结果是32位的，低 16 位保存在 `AX` 里面，高 16 位保存到 `DX` 里面，导致`DX`寄存器的值被覆盖

#### 十进制算数

了解即可，看不懂，去死吧！[介绍](https://goo.su/Q3MVxu)

![image-20250114140014523](https://s2.loli.net/2025/01/14/gFcZlVukbrEM7zt.png)

**AAA (加法后的ASCII调整)**
```assembly
mov al, '9'  ; AL = 39h ('9'的ASCII码)
add al, '8'  ; AL = 39h + 38h = 71h
aaa          ; 调整AL为09h，AH += 1 (AH = 01h)
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
aas          ; 调整AL为04h，AH -= 1 (AH = FFh)
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

![image-20250114192610412](https://s2.loli.net/2025/01/14/21jtb5mxlWLsIKk.png)

| 指令  | 示例               | 含义                            |
| ----- | ------------------ | ------------------------------- |
| `AND` | `AND A, B`         | 按位与                          |
| `OR`  | `OR A, B`          | 按位或                          |
| `XOR` | `XOR A, B`         | 异或                            |
| `BT`  | `BT Base, Offset`  | 指定地址的值赋给 CF             |
| `BTC` | `BTC Base, Offset` | 指定地址位的值赋给 CF，该位取反 |
| `BTR` | `BTR Base, Offset` | 指定地址位的值赋给 CF，该位设零 |
| `BTS` | `BTS Base, Offset` | 指定地址位的值赋给 CF，该位设一 |
| `BSF` | `BSF A, B`         | B 最低的 1 是第几位，赋给 A     |
| `BSR` | `BSR A, B`         | B 最高的 1 是第几位，赋给 A     |

#### 逻辑偏移

![image-20250114194130264](https://s2.loli.net/2025/01/17/SVDghbI2UTnLW8J.png)

| 指令 | 示例 | 含义 |
|------|------|------|
| SHL  | `SHL AX, 1` | 将AX寄存器的内容逻辑左移1位，空出的位用0填充 |
| SHR  | `SHR BX, 2` | 将BX寄存器的内容逻辑右移2位，空出的位用0填充 |
| SAL  | `SAL CX, 1` | 将CX寄存器的内容算术左移1位，空出的位用0填充（与SHL相同） |
| SAR  | `SAR DX, 3` | 将DX寄存器的内容算术右移3位，空出的位用符号位填充 |
| ROL  | `ROL AL, 1` | 将AL寄存器的内容循环左移1位，移出的位重新填充到右侧 |
| ROR  | `ROR BL, 2` | 将BL寄存器的内容循环右移2位，移出的位重新填充到左侧 |
| RCL  | `RCL AX, 1` | 将AX寄存器的内容带进位循环左移1位，进位标志 (CF) 参与循环 |
| RCR  | `RCR BX, 1` | 将BX寄存器的内容带进位循环右移1位，进位标志 (CF) 参与循环 |
| SHLD | `SHLD AX, BX, 4` | 将AX和BX寄存器的内容一起逻辑左移4位，AX的高位由BX的低位填充 |
| SHRD | `SHRD CX, DX, 3` | 将CX和DX寄存器的内容一起逻辑右移3位，CX的低位由DX的高位填充 |

> [!NOTE]
>
> **逻辑右移（SHR）用0填充空出的高位，而算术右移（SAR）用符号位填充空出的高位**

#### 标志位指令

| 指令  | 示例  | 含义              |
| ----- | ----- | ----------------- |
| `CLC` | `CLC` | 进位标志置零      |
| `STC` | `STC` | 进位标志设一      |
| `CMC` | `CMC` | 进位标志取反      |
| `CLD` | `CLD` | 方向标志置零      |
| `STD` | `STD` | 方向标志设一      |
| `CLI` | `CLI` | IF 置零，关闭中断 |
| `STI` | `STI` | IF 设一，打开中断 |

#### 分支控制

条件跳转是短跳转，操作数是一个字节，允许向后跳转 -128 或向前跳转 +127

无条件跳跃可以跳得更远，可以直接地址跳转，允许 +/-32K 的跳转，甚至允许跳转到AX寄存器！

**常用的一些指令**

| 指令   | 含义             | flag             | 反指令 | 反含义               | 反 flag          |
| ------ | ---------------- | ---------------- | ------ | -------------------- | ---------------- |
| `JA`   | Above            | `ZF=0 and CF=0`  | `JNA`  | Not Above            | `ZF=1 or CF=1`   |
| `JAE`  | Above or Equal   | `CF=0`           | `JNAE` | Not Above or Equal   | `CF=1`           |
| `JB`   | Below            | `CF=1`           | `JNB`  | Not Below            | `CF=0`           |
| `JBE`  | Below or Equal   | `ZF=1 or CF=1`   | `JNBE` | Not Below or Equal   | `ZF=0 and CF=0`  |
| `JC`   | **Carry**        | `CF=1`           | `JNC`  | **Not Carry**        | `CF=0`           |
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

主要有三种：

- `LOOP`，相当于

  ```c
  do {
      // 循环体代码
      CX--;
  } while (CX != 0);
  ```

- `LOOPZ`，相当于

  ```c
  do {
      // 循环体代码
      CX--;
  } while (CX != 0 && ZF == 1);
  ```

- `LOOPNZ`，相当于

  ```c
  do {
      // 循环体代码
      CX--;
  } while (CX != 0 && ZF == 0);
  ```

#### 短延迟

对于如下程序

```assembly
  mov cx, N  ; 消耗 4 时钟周期，这里 N 是字面量，但是取值还未确定
tag:
  nop        ; 消耗 3 时钟周期
  nop        ; 消耗 3 时钟周期
  loop tag   ; 消耗 17 个时钟周期，退出循环时仅 5 个时钟周期
```

总延迟时间的计算公式为：$$C = 4 + N \times 23 - 12$$

假设需要延迟 1000 个时钟周期，可以通过以下步骤计算循环次数 \( N \)：

$$1000 = 4 + N \times 23 - 12$$

解方程得到：

$$N = \frac{1000 - 4 + 12}{23} \approx 43.65$$

因此，设置 \( N = 44 \) 即可实现大约 1000 个时钟周期的延迟

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

延迟计算公式为：
$$
C_{T}=C_{0}+N(C_{BK}){-12}
$$
先计算内循环：
$$
C_T=C_0+N(C_{_{BK}}){-12}\\C_T=4+3000(20)-12\\C_T=599992
$$
然后计算外循环
$$
C_T=C_0+N(C_{_BK})-12\\C_T=4+30000(59992+2+16)-12\\C_T=1.8\times10^{10}\text{Clock cycles}
$$
实际上程序只花了15s来运行，计算出来的时钟频率是1200MHz，是目标机器的时钟频率(300MHz)的4倍,原因是现代处理器使用 **指令并行** 技术

#### 打印数字的方法

基于栈的实现：

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
    push bx        ; 函数调用，储存原来寄存器的值，固定操作
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
    pop dx         ; 函数调用结束，恢复原来寄存器的值，固定操作
    pop cx
    pop bx
    ret

END
```



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

- 以 NULL byte=0 字符结尾的字符串，`Charles Markham /0`
- 使用第一个字节设置长度的字符串，`/15 Charles Markham`

#### 字符串操作

`LEA`命令：将有效地址加载到 SI 中，例如：

```assembly
msg1 db "Hello, world.$" ; 定义字符串

lea SI, msg1 ; 将 msg1 的地址加载到 SI 中，这里 SI 寄存器将会存储 msg1 在内存中的起始地址
```

`MOVSB`命令：Move String Byte（移动字符串字节），移动一个字节的数据，将 DS：SI 指向的内存复制到 ES：DI 中指定的地址，通常用于从源字符串复制一个字节到目标字符串，执行 MOVSB 指令后，**SI** 和 **DI** 寄存器的值会自动递增或递减，如果 DF (Direction Flag) 为 0, SI 和 DI 递增，如果 DF 为 1, SI 和 DI 递减，例如：

```assembly
msg1 db "Hello$"  ; 源字符串
msg2 db "     $"  ; 目标字符串，预留空间

lea SI, msg1      ; SI 指向 msg1
lea DI, msg2      ; DI 指向 msg2

mov cx, 5         ; 设置循环次数为5， 要复制的字节个数

cld               ; DF寄存器置0

rep movsb         ; 执行 5 次复制
```

`CMPSB`命令：Compare String Byte（比较字符串字节），这条指令会比较 **SI** 寄存器指向的字节和 **DI** 寄存器指向的字节，并设置相应的标志位（如 ZF、SF 等）。例如：

```assembly
msg1 db "Hello$" ; 第一个字符串
msg2 db "Hello$" ; 第二个字符串

lea SI, msg1     ; SI 指向 msg1
lea DI, msg2     ; DI 指向 msg2

mov cx, 5        ; 设置循环次数为5， 要比较的字节个数

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
> 修饰符 `REP` 可以放在任何字符串指令的前面，并重复指令 CX 次。Rep 代表重复字符串前缀。

`movsb`,`CMPSB` 是 CISC 的,以下维基百科上关于CISC的介绍：

> **复杂指令集计算机**（英语：Complex Instruction Set Computer；[缩写](https://zh.wikipedia.org/wiki/縮寫)：**CISC**）是一种[微处理器](https://zh.wikipedia.org/wiki/微處理器)[指令集架构](https://zh.wikipedia.org/wiki/指令集架構)，每个指令可执行若干低端操作，诸如从[存储器](https://zh.wikipedia.org/wiki/電腦記憶體)读取、存储、和[计算](https://zh.wikipedia.org/wiki/計算)操作，全部集于单一指令之中。与之相对的是[精简指令集](https://zh.wikipedia.org/wiki/精简指令集)。
>
> 复杂指令集的特点是指令数目多而复杂，每条指令字长并不相等，电脑必须加以判读，并为此付出了性能的代价。
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

除法部分就是直接减，不够了就回退，略

#### 浮点数

浮点数通过**科学计数法**的形式表示实数，通常分为三个部分：

- **符号位（Sign）**：表示数的正负。
- **指数位（Exponent）**：表示数的规模（即小数点的位置）。
-  **尾数位（Mantissa 或 Fraction）**：表示数的精度。

![img](https://s2.loli.net/2025/01/17/qo9xS5yJDXslOGp.png)

浮点数的通用表示形式为：
$$
\text{Value} = (-1)^{\text{Sign}} \times \text{Mantissa} \times 2^{\text{Exponent}}
$$
**规格化浮点数**

规格化浮点数是 IEEE 754 标准中最常见的表示形式，其特点是尾数部分的最高位隐含为 `1`（即尾数的整数部分为 `1`）。

**规格化浮点数的表示**

- **尾数（Mantissa）**：隐含前导 `1`，实际存储的是小数部分。
- **指数（Exponent）**：非全 `0` 且非全 `1`（单精度：1 到 254，双精度：1 到 2046）。
- **公式**：
$$
  \text{Value} = (-1)^{\text{Sign}} \times 1.\text{Mantissa} \times 2^{\text{Exponent} - \text{Bias}}
$$

**示例**

单精度浮点数：
- 符号位：`0`（正数）

- 指数位：`10000001`（129，偏移量 127，实际指数为 2）

- 尾数位：`10100000000000000000000`（隐含前导 `1`，实际尾数为 `1.101`）

值：

$$
\text{Value} = 1.101_2 \times 2^2 = 110.1_2 = 6.5_{10}
$$

---

**非规格化浮点数**
非规格化浮点数用于表示非常接近于零的数值，其特点是尾数部分的最高位为 `0`（即尾数的整数部分为 `0`）。

**非规格化浮点数的表示**
- **尾数（Mantissa）**：没有隐含前导 `1`，实际存储的是小数部分。
- **指数（Exponent）**：全 `0`（单精度：0，双精度：0）。
- **公式**：
$$
\text{Value} = (-1)^{\text{Sign}} \times 0.\text{Mantissa} \times 2^{1 - \text{Bias}}
$$

 **示例**
- 单精度浮点数：
  - 符号位：`0`（正数）
  - 指数位：`00000000`（0，偏移量 127，实际指数为 -126）
  - 尾数位：`00000000000000000000001`（没有隐含前导 `1`，实际尾数为 `0.00000000000000000000001`）
  - 值：
$$
\text{Value} = 0.00000000000000000000001_2 \times 2^{-126} \approx 1.4 \times 10^{-45}
$$



[视频讲解](https://www.bilibili.com/video/BV1VK4y1f7o6/)

#### 浮点数的计算

浮点数做加减法运算遵循一个原则，那就是**先对齐，再计算**。

「对齐」指的是对齐指数位 e。两个浮点数相加时，如果 e 不一样，就要先把 e 对齐再做加法运算。如何对齐呢？对齐的原则就是把 e 都统一成其中较大的一个。

比如 0.5 与 0.125 相加，这两个数表示成浮点数分别是$$(-1)^0\times1.0\times2^{-1}$$ 和 $$(-1)^0\times1.0\times2^{-3}$$，由于 0.5 的指数大于 0.125 的指数，所以要把 0.125 的指数统一成和 0.5 一样的 -1，指数增大，那么有效数位要右移，因为 f 前面默认有个 1，所以右移之后，0.125 的有效数位变成了 0.01，然后将 0.5 的有效数位与 0.125 的有效数位相加，结果是 1.01，最终表示成浮点数就是$$(-1)^0\times1.01\times2^{-1}$$。

#### 8087 协处理器

> 处理器都有CP了 (╯‵□′)╯︵┻━┻

8087 是一种 **数学协处理器**，也被称为 **浮点处理器** 或 **数字数据处理器 (Numeric Data Processor, NDP)**。 它不是一个独立的中央处理器 (CPU)，而是被设计用来与 Intel 的 8086、8088 等 CPU 一起工作，以加速浮点运算。

![image-20250117下午40544444](https://s2.loli.net/2025/01/17/Nqe5dL6AnGW4b9l.png)

**状态字组**

![image-20250117下午40632589](https://s2.loli.net/2025/01/17/9kFJtIMY6uq3oA7.png)

**控制字组**

![image-20250117下午40754970](https://s2.loli.net/2025/01/17/Morvu9qm1d6ZICk.png)

**栈**

8087 还自带了一个栈，栈当中每个元素都是 10 字节，栈始终有 8 个位置。
每次压入新数据到栈当中，栈底数据被覆盖，就和移位运算差不多
在 MASM 汇编代码当中，`ST(0)` 始终表示栈顶，`ST(1~7)` 表示栈中其他元素。

![image-20250117下午41054852](https://s2.loli.net/2025/01/17/cXJCY3xZ6r4gRNV.png)

**8087 指令**

- `FADD S1/D, S2` 表示把两个 S 进行加法运算，结果存入 D（S1=D）。如果没有指定两个 S，那么就相当于 `ST(0) += ST(1)`
- `FSUB S1/D, S2` 相当于执行 `S1 -= S2`
- `FSUBR S1/D, S2` 与上面相反，相当于 `S1 = S2 - S1`
- 此外还有 `FMUL`，`FDIV`，`FMULP`，`FIMUL`，`FDIVR`，`FDIP`，`FIDIV` 等

---

